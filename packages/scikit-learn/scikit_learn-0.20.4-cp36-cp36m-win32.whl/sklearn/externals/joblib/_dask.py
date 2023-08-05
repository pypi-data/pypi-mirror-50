from __future__ import print_function, division, absolute_import

import contextlib

from uuid import uuid4
import weakref

from .parallel import AutoBatchingMixin, ParallelBackendBase, BatchedCalls
from .parallel import parallel_backend

try:
    import distributed
except ImportError:
    distributed = None

if distributed is not None:
    from distributed.client import Client, _wait
    from distributed.utils import funcname, itemgetter
    from distributed import get_client, secede, rejoin
    from distributed.worker import thread_state
    from distributed.sizeof import sizeof
    from tornado import gen


def is_weakrefable(obj):
    try:
        weakref.ref(obj)
        return True
    except TypeError:
        return False


try:
    TimeoutError = TimeoutError
except NameError:
    # Python 2 backward compat
    class TimeoutError(OSError):
        pass


class _WeakKeyDictionary:
    """A variant of weakref.WeakKeyDictionary for unhashable objects.

    This datastructure is used to store futures for broadcasted data objects
    such as large numpy arrays or pandas dataframes that are not hashable and
    therefore cannot be used as keys of traditional python dicts.

    Futhermore using a dict with id(array) as key is not safe because the
    Python is likely to reuse id of recently collected arrays.
    """

    def __init__(self):
        self._data = {}

    def __getitem__(self, obj):
        ref, val = self._data[id(obj)]
        if ref() is not obj:
            # In case of a race condition with on_destroy.
            raise KeyError(obj)
        return val

    def __setitem__(self, obj, value):
        key = id(obj)
        try:
            ref, _ = self._data[key]
            if ref() is not obj:
                # In case of race condition with on_destroy.
                raise KeyError(obj)
        except KeyError:
            # Insert the new entry in the mapping along with a weakref
            # callback to automatically delete the entry from the mapping
            # as soon as the object used as key is garbage collected.
            def on_destroy(_):
                del self._data[key]
            ref = weakref.ref(obj, on_destroy)
        self._data[key] = ref, value

    def __len__(self):
        return len(self._data)

    def clear(self):
        self._data.clear()


def _funcname(x):
    try:
        if isinstance(x, BatchedCalls):
            x = x.items[0][0]
    except Exception:
        pass
    return funcname(x)


class Batch(object):
    def __init__(self, tasks):
        self.tasks = tasks

    def __call__(self, *data):
        results = []
        with parallel_backend('dask'):
            for func, args, kwargs in self.tasks:
                args = [a(data) if isinstance(a, itemgetter) else a
                        for a in args]
                kwargs = {k: v(data) if isinstance(v, itemgetter) else v
                          for (k, v) in kwargs.items()}
                results.append(func(*args, **kwargs))
        return results

    def __reduce__(self):
        return Batch, (self.tasks,)


def _joblib_probe_task():
    # Noop used by the joblib connector to probe when workers are ready.
    pass


class DaskDistributedBackend(ParallelBackendBase, AutoBatchingMixin):
    MIN_IDEAL_BATCH_DURATION = 0.2
    MAX_IDEAL_BATCH_DURATION = 1.0

    def __init__(self, scheduler_host=None, scatter=None,
                 client=None, loop=None, wait_for_workers_timeout=10,
                 **submit_kwargs):
        if distributed is None:
            msg = ("You are trying to use 'dask' as a joblib parallel backend "
                   "but dask is not installed. Please install dask "
                   "to fix this error.")
            raise ValueError(msg)

        if client is None:
            if scheduler_host:
                client = Client(scheduler_host, loop=loop,
                                set_as_default=False)
            else:
                try:
                    client = get_client()
                except ValueError:
                    msg = ("To use Joblib with Dask first create a Dask Client"
                           "\n\n"
                           "    from dask.distributed import Client\n"
                           "    client = Client()\n"
                           "or\n"
                           "    client = Client('scheduler-address:8786')")
                    raise ValueError(msg)

        self.client = client

        if scatter is not None and not isinstance(scatter, (list, tuple)):
            raise TypeError("scatter must be a list/tuple, got "
                            "`%s`" % type(scatter).__name__)

        if scatter is not None and len(scatter) > 0:
            # Keep a reference to the scattered data to keep the ids the same
            self._scatter = list(scatter)
            scattered = self.client.scatter(scatter, broadcast=True)
            self.data_futures = {id(x): f for x, f in zip(scatter, scattered)}
        else:
            self._scatter = []
            self.data_futures = {}
        self.task_futures = set()
        self.wait_for_workers_timeout = wait_for_workers_timeout
        self.submit_kwargs = submit_kwargs

    def __reduce__(self):
        return (DaskDistributedBackend, ())

    def get_nested_backend(self):
        return DaskDistributedBackend(client=self.client), -1

    def configure(self, n_jobs=1, parallel=None, **backend_args):
        return self.effective_n_jobs(n_jobs)

    def start_call(self):
        self.call_data_futures = _WeakKeyDictionary()

    def stop_call(self):
        # The explicit call to clear is required to break a cycling reference
        # to the futures.
        self.call_data_futures.clear()

    def effective_n_jobs(self, n_jobs):
        effective_n_jobs = sum(self.client.ncores().values())
        if effective_n_jobs != 0 or not self.wait_for_workers_timeout:
            return effective_n_jobs

        # If there is no worker, schedule a probe task to wait for the workers
        # to come up and be available. If the dask cluster is in adaptive mode
        # task might cause the cluster to provision some workers.
        try:
            self.client.submit(_joblib_probe_task).result(
                timeout=self.wait_for_workers_timeout)
        except gen.TimeoutError:
            error_msg = (
                "DaskDistributedBackend has no worker after {} seconds. "
                "Make sure that workers are started and can properly connect "
                "to the scheduler and increase the joblib/dask connection "
                "timeout with:\n\n"
                "parallel_backend('dask', wait_for_workers_timeout={})"
            ).format(self.wait_for_workers_timeout,
                     max(10, 2 * self.wait_for_workers_timeout))
            raise TimeoutError(error_msg)
        return sum(self.client.ncores().values())

    def _to_func_args(self, func):
        collected_futures = []
        itemgetters = dict()

        # Futures that are dynamically generated during a single call to
        # Parallel.__call__.
        call_data_futures = getattr(self, 'call_data_futures', None)

        def maybe_to_futures(args):
            for arg in args:
                arg_id = id(arg)
                if arg_id in itemgetters:
                    yield itemgetters[arg_id]
                    continue

                f = self.data_futures.get(arg_id, None)
                if f is None and call_data_futures is not None:
                    try:
                        f = call_data_futures[arg]
                    except KeyError:
                        if is_weakrefable(arg) and sizeof(arg) > 1e3:
                            # Automatically scatter large objects to some of
                            # the workers to avoid duplicated data transfers.
                            # Rely on automated inter-worker data stealing if
                            # more workers need to reuse this data
                            # concurrently.
                            [f] = self.client.scatter([arg])
                            call_data_futures[arg] = f

                if f is not None:
                    getter = itemgetter(len(collected_futures))
                    collected_futures.append(f)
                    itemgetters[arg_id] = getter
                    arg = getter
                yield arg

        tasks = []
        for f, args, kwargs in func.items:
            args = list(maybe_to_futures(args))
            kwargs = dict(zip(kwargs.keys(),
                              maybe_to_futures(kwargs.values())))
            tasks.append((f, args, kwargs))

        if not collected_futures:
            return func, ()
        return (Batch(tasks), collected_futures)

    def apply_async(self, func, callback=None):
        key = '%s-batch-%s' % (_funcname(func), uuid4().hex)
        func, args = self._to_func_args(func)

        future = self.client.submit(func, *args, key=key, **self.submit_kwargs)
        self.task_futures.add(future)

        @gen.coroutine
        def callback_wrapper():
            result = yield _wait([future])
            self.task_futures.remove(future)
            if callback is not None:
                callback(result)  # gets called in separate thread

        self.client.loop.add_callback(callback_wrapper)

        ref = weakref.ref(future)  # avoid reference cycle

        def get():
            return ref().result()

        future.get = get  # monkey patch to achieve AsyncResult API
        return future

    def abort_everything(self, ensure_ready=True):
        """ Tell the client to cancel any task submitted via this instance

        joblib.Parallel will never access those results
        """
        self.client.cancel(self.task_futures)
        self.task_futures.clear()

    @contextlib.contextmanager
    def retrieval_context(self):
        """Override ParallelBackendBase.retrieval_context to avoid deadlocks.

        This removes thread from the worker's thread pool (using 'secede').
        Seceding avoids deadlock in nested parallelism settings.
        """
        # See 'joblib.Parallel.__call__' and 'joblib.Parallel.retrieve' for how
        # this is used.
        if hasattr(thread_state, 'execution_state'):
            # we are in a worker. Secede to avoid deadlock.
            secede()

        yield

        if hasattr(thread_state, 'execution_state'):
            rejoin()

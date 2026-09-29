"""Run a method of an object over several processes without pickling the object.

A circuit is a deeply linked graph of nodes and is too deep to pickle for large
circuits. Instead the object is stored in a module global before the worker
processes are forked, so the workers inherit it. Only the small arguments and
results are sent between processes. This needs the ``fork`` start method.
"""
import multiprocessing
import warnings

_shared = None


def fork_available():
    """True if worker processes can be forked on this platform."""
    return "fork" in multiprocessing.get_all_start_methods()


def _call(method_name, args):
    return getattr(_shared, method_name)(*args)


def parallel_map(obj, method_name, jobs, num_proc):
    """``[obj.method_name(*job) for job in jobs]``, computed by ``num_proc`` processes.

    Falls back to a serial loop for one process, or with a warning where the
    ``fork`` start method does not exist. Arguments and results must be picklable.
    """
    global _shared
    if num_proc <= 1 or len(jobs) <= 1:
        return [getattr(obj, method_name)(*job) for job in jobs]
    if not fork_available():
        warnings.warn("Parallel runs need the 'fork' start method, running serially",
                      RuntimeWarning, stacklevel=2)
        return [getattr(obj, method_name)(*job) for job in jobs]

    _shared = obj
    try:
        with multiprocessing.get_context("fork").Pool(min(num_proc, len(jobs))) as pool:
            return pool.starmap(_call, [(method_name, job) for job in jobs])
    finally:
        _shared = None

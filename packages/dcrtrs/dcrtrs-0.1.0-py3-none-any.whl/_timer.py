from functools import wraps
from time import perf_counter


def timer(func):
    """Print the runtime of the decorated function"""

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        print('Finished {!r} in {:.4f} secs'.format(func.__name__, run_time))
        return value

    return wrapper_timer

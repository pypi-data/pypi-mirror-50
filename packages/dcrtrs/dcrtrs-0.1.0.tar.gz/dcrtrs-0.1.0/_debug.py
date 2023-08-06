from functools import wraps


def debug(func):
    """Print the function signature and return value"""

    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = ['{}={!r}'.format(k, v) for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print("Calling {}({})".format(func.__name__, signature))
        value = func(*args, **kwargs)
        print("{!r} returned {!r} of type - {}".format(func.__name__, value, type(value)))
        return value
    return wrapper_debug

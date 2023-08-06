import asyncio
from functools import wraps
from typing import Callable


def coroutine(f: Callable) -> Callable:
    """
    Wrap a function as a co-routine to support async-await allowing the to be called synchronously.

    :param f:
    :return:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

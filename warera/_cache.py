import asyncio
from collections import OrderedDict
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def async_memoize(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    """
    A simple unbounded async memoization decorator.
    Caches the results of the wrapped function based on its arguments.
    Automatically handles concurrent 'thundering herd' requests by returning
    the same Future to all waiters.
    """
    cache: OrderedDict[Any, asyncio.Future[R]] = OrderedDict()

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # Create a hashable key from args and kwargs.
        key: Any
        try:
            key = (args, frozenset(kwargs.items()))
        except TypeError:
            # If arguments are not hashable (e.g. lists), we convert them to strings.
            key = (str(args), str(kwargs))

        if key in cache:
            cache.move_to_end(key)
            return await cache[key]

        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        cache[key] = fut
        if len(cache) > 1000:
            cache.popitem(last=False)

        try:
            result = await func(*args, **kwargs)
            fut.set_result(result)
            return result
        except Exception as e:
            fut.set_exception(e)
            # Remove failed futures so they can be retried
            del cache[key]
            raise

    return wrapper

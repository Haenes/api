import json

from typing import AsyncGenerator, Callable

from redis.asyncio import ConnectionPool, Redis

from config import REDIS_USER, REDIS_PASSWORD, REDIS_EXPIRE_TIME
from .pagination import PaginatedResponse, NoItemsResponse


pool = ConnectionPool.from_url(
    f"redis://{REDIS_USER}:{REDIS_PASSWORD}@redis",
    decode_responses=True,
    max_connections=10
)


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    async with Redis.from_pool(pool) as client:
        yield client


async def cache_get_or_set(
    cache: Redis,
    key: str,
    func: Callable,
    *args_for_func
) -> PaginatedResponse | NoItemsResponse:
    """ Return value for a given key if exist or set key with a func result. """

    try:
        cache_result = json.loads(await cache.get(key))
    except TypeError:
        cache_result = None

    if cache_result is not None:
        return cache_result
    else:
        result = await func(*args_for_func)

        await cache.set(key, result.model_dump_json(), ex=REDIS_EXPIRE_TIME)
        return result


async def cache_delete_all(cache: Redis, pattern: str):
    """ Delete all keys that match pattern. """
    cache_keys = await cache.keys(pattern)

    for i in range(len(cache_keys)):
        await cache.delete(cache_keys[i])

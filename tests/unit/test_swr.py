import asyncio

import pytest

from warera._swr import SWRCache


@pytest.mark.asyncio
async def test_swr_cache_basic_fetch():
    cache = SWRCache()
    fetches = 0

    async def fetcher():
        nonlocal fetches
        fetches += 1
        await asyncio.sleep(0.01)
        return "data"

    # First fetch should block and return data
    res = await cache.get("key1", 10.0, fetcher)
    assert res == "data"
    assert fetches == 1

    # Second fetch should return immediately from cache
    res2 = await cache.get("key1", 10.0, fetcher)
    assert res2 == "data"
    assert fetches == 1


@pytest.mark.asyncio
async def test_swr_cache_stale_revalidate():
    cache = SWRCache()
    fetches = 0

    async def fetcher():
        nonlocal fetches
        fetches += 1
        await asyncio.sleep(0.05)
        return f"data_{fetches}"

    # Initial fetch
    res1 = await cache.get("key", 0.01, fetcher)
    assert res1 == "data_1"
    assert fetches == 1

    # Wait for TTL to expire
    await asyncio.sleep(0.02)

    # Next fetch should instantly return stale data, but trigger revalidate
    res2 = await cache.get("key", 0.01, fetcher)
    assert res2 == "data_1"  # Returns stale data instantly

    # Allow the background revalidation task to finish
    await asyncio.sleep(0.1)
    
    assert fetches == 2

    # Next fetch should return the newly revalidated data
    res3 = await cache.get("key", 0.01, fetcher)
    assert res3 == "data_2"


@pytest.mark.asyncio
async def test_swr_cache_concurrent_fetches():
    cache = SWRCache()
    fetches = 0

    async def fetcher():
        nonlocal fetches
        fetches += 1
        await asyncio.sleep(0.1)
        return "data"

    # Fire 5 concurrent requests for the same key
    results = await asyncio.gather(*(
        cache.get("key", 10.0, fetcher) for _ in range(5)
    ))

    # All should get the data, but fetcher should only be called ONCE
    for r in results:
        assert r == "data"
    assert fetches == 1

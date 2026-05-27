# Migrating to warera-client v0.2.0

Version `0.2.0` introduces a modernized Developer Experience (DX) focused on implicit performance and simpler syntax. We've introduced a global API module, a supercharged time-slicing pagination engine, and smart caching.

Here is what you need to know to upgrade your code from `0.1.x`.

## 1. Global API & Client Instantiation

You no longer need to manually instantiate and manage `WareraClient` unless you specifically want to manage multiple sessions. The `warera` module itself now acts as the client. 

**Before:**
```python
import asyncio
from warera import WareraClient

async def main():
    async with WareraClient() as client:
        user = await client.user.get_by_id("123")
```

**After:**
```python
import asyncio
import warera

async def main():
    user = await warera.user.get_by_id("123")
```

If you need to set an API key dynamically, you can use `warera.set_api_key("...")` (or `warera.sync.set_api_key("...")`), or simply set the `WARERA_API_KEY` environment variable.

*(Note: The old `WareraClient` context manager still exists and is fully supported if you prefer the classic approach).*

## 2. Smart Auto-Batching in `get_many()`

The `get_many()` methods on all resources (e.g., `user.get_many()`, `company.get_many()`) have been updated. They now use the `BatchSession` engine internally to split huge lists of IDs into compliant chunks of 50 procedures, fetching them all concurrently over the network. 

**Before:**
```python
users = await client.user.get_many(["1", "2", "3", ...], batch_size=50)
```

**After:**
```python
# Pass 10,000 IDs if you want, it will automatically chunk and fire concurrently.
users = await warera.user.get_many(["1", "2", "3", ...])
```

## 3. Supercharged Pagination

In `0.1.x`, we relied heavily on generator loops. In `0.2.0`, pagination has been modernized:

- **`auto_items=True`**: To yield single items across pages, simply pass `auto_items=True` to any paginated method. This replaces the old `paginate()` wrapper.
  *(Note: The old `paginate()` wrapper and `auto_paginate=True` parameter are now formally deprecated and will be removed in v0.2.1).*
- **`collect_all()`**: Completely rewritten. It now uses a **parallel time-slicing engine** with synthetic cursors. Instead of fetching pages sequentially, it splits the history into chunks and fetches them all concurrently, resulting in a >5x speedup for massive datasets!

**Usage:**
```python
# Async item generator
async for party in client.party.get_paginated(country_id="7", auto_items=True):
    print(party.name)

# Collect all items instantly in parallel
all_parties = await client.party.collect_all(country_id="7")
```

> [!WARNING]
> **Extreme Throughput Caution**: The `collect_all` and `get_many` engines default to an extreme concurrency of 500 to perfectly saturate the 500 req/min API rate limit. While the client safely protects against 429 errors and DDoS mitigation logic by jittering bursts, this concurrency can cause high memory usage on constrained environments (like AWS Lambdas) or hit OS File Descriptor limits if used concurrently with other network apps.
> You can globally dial down the concurrency limit by setting the `WARERA_MAX_CONCURRENCY` environment variable (e.g. `export WARERA_MAX_CONCURRENCY=50`).

## 4. Static Resources Caching

Static resources like `warera.game_config.get()` or `warera.country.find_by_name()` are now aggressively cached in-memory concurrently. You don't need to wrap these calls in your own cache loops anymore; the SDK does it for you.

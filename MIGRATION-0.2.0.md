# Migrating to warera-client v0.2.0

Version `0.2.0` introduces a completely modernized Developer Experience (DX) focused on implicit performance and simpler syntax. We've introduced a global API module, transparent auto-batching, and smart caching.

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

## 2. Transparent Auto-Batching

The `get_many()` methods on all resources (e.g., `user.get_many()`, `company.get_many()`) have been drastically simplified. You no longer need to pass `batch_size`. The client automatically batches and chunks your requests globally in a 10ms window.

**Before:**
```python
users = await client.user.get_many(["1", "2", "3"], batch_size=50)
```

**After:**
```python
users = await warera.user.get_many(["1", "2", "3"])
```

## 3. Supercharged Pagination

In `0.1.x`, `paginate()` and `collect_all()` were somewhat bloated sequential generators. In `0.2.0`, these wrappers have been **restored and massively supercharged** across all paginated resources!

- **`paginate()`**: Still an async generator, but now perfectly proxies the underlying API engine transparently.
- **`collect_all()`**: Completely rewritten. It now uses a **parallel time-slicing engine** with synthetic cursors. Instead of fetching pages sequentially, it splits the history into chunks and fetches them all concurrently, resulting in a >5x speedup for massive datasets!

**Usage:**
```python
# Async item generator
async for party in client.party.paginate(country_id="7"):
    print(party.name)

# Collect all items instantly in parallel
all_parties = await client.party.collect_all(country_id="7")
```

## 4. Static Resources Caching

Static resources like `warera.game_config.get()` or `warera.country.find_by_name()` are now aggressively cached in-memory concurrently. You don't need to wrap these calls in your own cache loops anymore; the SDK does it for you.

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

## 3. Simplified Pagination

The old `paginate()` and `collect_all()` async generator wrappers have been removed to reduce bloat. They have been replaced with a transparent `get_all()` method on supported resources (like `country`, `user`, etc.).

**Before:**
```python
all_parties = await client.party.collect_all(country_id="7")

async for party in client.party.paginate(country_id="7"):
    print(party.name)
```

**After:**
```python
# Just use the standard get_paginated manually, or get_all() if available
page = await warera.party.get_paginated(country_id="7")
for party in page.items:
    print(party.name)
```

## 4. Static Resources Caching

Static resources like `warera.game_config.get()` or `warera.country.find_by_name()` are now aggressively cached in-memory concurrently. You don't need to wrap these calls in your own cache loops anymore; the SDK does it for you.

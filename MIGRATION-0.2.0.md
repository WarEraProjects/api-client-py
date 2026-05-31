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
  *(Note: The old `paginate()` wrapper and `auto_paginate=True` parameter have been fully removed in 0.2.0).*
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
> **Extreme Throughput Caution**: The `collect_all` and `get_many` engines default to an extreme concurrency of `500` (and `time_slice_days=0.2`) to perfectly saturate the 500 req/min API rate limit. While the client safely protects against 429 errors and DDoS mitigation logic by jittering bursts, this concurrency can cause 502 Bad Gateway errors on the API side if querying heavy endpoints (like thousands of transactions), or hit OS File Descriptor limits locally.
> You can globally dial down the concurrency limit by setting the `WARERA_MAX_CONCURRENCY` environment variable (e.g. `export WARERA_MAX_CONCURRENCY=50`), or by overriding `concurrency=100` and `time_slice_days=1` directly in the `collect_all` method call.

## 4. Static Resources Caching (SWR)

Static resources like `warera.game_config.get()` or `warera.country.get_all()` are now cached using a highly optimized **Stale-While-Revalidate (SWR)** pattern. You don't need to wrap these calls in your own cache loops anymore; the SDK does it for you. It instantly serves stale data (if available) while firing a background task to refresh the cache seamlessly.

## 5. HTTP/2 and Network Optimizations

The client now defaults to HTTP/2. By keeping a single TCP connection alive and multiplexing requests, API round-trip times are significantly faster, dropping overhead massively compared to 0.1.x.

## 6. Tracing, Logging, and Observability

We've introduced complete visibility into the SDK's mechanics (conceptually mirroring tRPC's `httpBatchLink` and "Links" middleware):

- **Standard Logging**: You can now enable `logging.getLogger("warera").setLevel(logging.DEBUG)` to watch exactly when the engine queues procedures, flushes batches, hits cache (stale vs fresh), and automatically sleeps on rate limits.
- **Configurable Batch Delays**: `WareraClient` now accepts an `auto_batch_delay` (default: 5ms) allowing you to manually tune the batching collection window to your exact requirements.
- **Event Hooks**: `WareraClient` now exposes `event_hooks={"request": [...], "response": [...]}` which perfectly matches the functionality of tRPC Links, allowing you to inject Prometheus metrics, datadog loggers, or raw JSON debuggers on every network call.

## 7. HTTP Retry Engine with Exponential Backoff

To achieve 100% architectural parity with the TypeScript wrapper's `createRetryFetch`, we've implemented an advanced **HTTP Retry Engine** directly into the core `HttpSession`.

If a request fails due to a transient network error or specific API response codes (`408, 409, 425, 429, 500, 502, 503, 504`), the client will automatically retry the request up to `max_retries` times. It leverages **exponential backoff with uniform random jittering** to prevent thundering herd problems.
You can completely control this via the `WareraClient` configuration:
```python
client = warera.WareraClient(
    max_retries=3,
    initial_delay_ms=250,
    max_delay_ms=5000,
    backoff_multiplier=2.0,
    jitter=True,
    retryable_status_codes={408, 409, 425, 429, 500, 502, 503, 504}, # Customize which errors trigger a retry
    headers={"X-My-Proxy": "1"} # You can now also inject custom headers globally!
)
```

## 8. Strict Typings for `GameConfig`

Previously, static resources returned by `gameConfig.getGameConfig` were lazily mapped to `dict[str, Any]`. We've eliminated this to provide **strict static typings and IDE autocomplete support**!
Over 75 nested structures (e.g., `GameConfigBadges`, `UpgradeConfigBunkerLevel`, `ItemConcrete`) have been natively generated from the TypeScript `Responses.d.ts` definitions. 

```python
config = await warera.game_config.get()
print(config.badge.coffee.reward)  # Fully strictly typed and auto-completable!
```

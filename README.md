# Warera Python Client

[![PyPI version](https://badge.fury.io/py/warera-client.svg)](https://pypi.org/project/warera-client/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/warera-client?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=Downloads)](https://pepy.tech/projects/warera-client)

> A robust, fully-typed, async-first Python client for the [WarEra](https://warera.io) tRPC API (v0.25.0-beta).
> 
> **⚠️ Upgrading from v0.1.x?** Please read the [v0.2.0 Migration Guide](https://github.com/wareraprojects/api-client-py/wiki/Migration-Guide).
> 
```python
import warera

async def main():
    user   = await warera.user.get_by_id("12345")
    prices = await warera.item_trading.get_prices()
    gov    = await warera.government.get("7")
```

## Features

- **Full API coverage** — all endpoints across 32 resource namespaces.
- **Fully Typed** — Pydantic v2 models for *every* request and response.
- **Async-first** — built on `httpx.AsyncClient`; sync shim included.
- **Cursor pagination** — transparent `auto_items=True` generator and `collect_all()` time-slicing engine.
- **Batch requests** — `BatchSession` for multiple procedures in one HTTP round-trip; auto-chunked `get_many` for ID lists.
- **Smart batch splitting** — any batch larger than the server's hard limit of 50 is automatically split and fired concurrently; no manual chunking needed.
- **Adaptive rate limiting** — reads `ratelimit-remaining` / `ratelimit-reset` response headers and sleeps exactly as long as the server says.
- **Resilient** — automatic retry with exponential backoff on 429 and 5xx errors.
- **Optional auth** — `X-API-Key` gives higher rate limits; works anonymously too.

## Installation

```bash
pip install warera-client
```

Requires Python 3.10+.

---

## Quick Start

### Async (recommended)

```python
import asyncio
import warera

# The global module automatically reads WARERA_API_KEY from your environment.
# You can also manually set it via: warera.set_api_key("YOUR_KEY")

async def main():
    # Simple lookups
    user    = await warera.user.get_by_id("12345")
    country = await warera.country.find_by_name("Ukraine")
    gov     = await warera.government.get(country.id)
    prices  = await warera.item_trading.get_prices()

    print(user.username, country.name)
    print(f"Iron: {prices.get('iron').price}")

    # Paginated
    page = await warera.user.get_paginated(country_id=country.id, limit=50)
    for u in page.items:
        print(u.username)

asyncio.run(main())
```

### Sync

```python
import warera.sync

warera.sync.set_api_key("YOUR_KEY")

user    = warera.sync.user.get_by_id("12345")
prices  = warera.sync.item_trading.get_prices()
```

---

## Authentication

```python
# Option 1 - pass key directly
client = WareraClient(api_key="abc123")

# Option 2 - environment variable (recommended for scripts/CI)
# export WARERA_API_KEY=abc123
client = WareraClient()   # key picked up automatically

# Option 3 - no key (anonymous, lower rate limits)
client = WareraClient()
```

---

## Rate Limiting

> [!NOTE]
> The client dynamically reads the rate-limit headers the API attaches to **every** response (`ratelimit-limit`, `ratelimit-remaining`, `ratelimit-reset`).
> 
> When `ratelimit-remaining` reaches `0`, the client automatically sleeps for exactly `ratelimit-reset` seconds before the next request. No hardcoded delays, no guessing! If the server changes its policy, the client adapts automatically.

You can inspect the current quota at any time via `client.rate_limit_remaining` and
`client.rate_limit_total` (both return `None` until the first response is received):

```python
async with WareraClient(api_key="YOUR_KEY") as client:
    await client.user.get_by_id("1")
    print(client.rate_limit_remaining)  # e.g. 499
    print(client.rate_limit_total)      # e.g. 500
```

---

## All Resource Methods

For a complete, detailed list of all 32 resource namespaces, their signatures, and the returned Pydantic models, please refer to the **[API Reference Wiki](https://github.com/wareraprojects/api-client-py/wiki/API-Reference)**.

---

## Pagination

Every paginated endpoint exposes three calling patterns:

```python
# 1. Single page - manual cursor control
page = await client.battle.get_many(is_active=True, limit=20)
print(page.items)        # list[Battle]
print(page.next_cursor)  # str | None
print(page.has_more)     # bool

# 2. Async generator - yields items one by one across all pages
async for battle in client.battle.get_many(is_active=True, auto_items=True):
    print(battle.id)

# 3. Collect all pages into a flat list using the ultra-fast parallel time-slicing engine
all_battles = await client.battle.collect_all()
```

*(Note: The old `paginate()` wrapper and `auto_paginate=True` parameter have been fully removed in 0.2.0).*

---

## Batch Requests

> [!TIP]
> The server enforces a hard limit of **50 procedures per batch POST**. The client handles this automatically at every level:

| What you call | What happens |
|---|---|
| `client.batch()` with ≤ 50 items | One POST |
| `client.batch()` with > 50 items | Auto-split into ≤ 50-item chunks, fired concurrently |
| `client.company.get_many(200_ids)` | 4 × 50-item POSTs, results merged in order |
| `session._http.post_batch(120_procs, ...)` | Auto-split internally, 3 × concurrent POSTs |

You never need to think about the limit - just pass what you need.

### Mixed procedures

```python
async with client.batch() as batch:
    country_item = batch.add("country.getCountryById",    {"countryId": "7"})
    gov_item     = batch.add("government.getByCountryId", {"countryId": "7"})
    prices_item  = batch.add("itemTrading.getPrices",     {})
    dates_item   = batch.add("gameConfig.getDates",       {})

# After the block - all resolved in one POST:
country = country_item.result
gov     = gov_item.result
prices  = prices_item.result
dates   = dates_item.result
```

### Large batches

```python
# 200 company IDs → 4 concurrent POSTs of 50, results merged
companies = await client.company.get_many(list_of_200_ids)

# Same for any resource with get_many
users   = await client.user.get_many(user_ids)     # list[User]
regions = await client.region.get_many(region_ids)  # list[Region]
rounds  = await client.round.get_many(round_ids)    # list[Round]
mus     = await client.mu.get_many(mu_ids)          # list[MilitaryUnit]
```

### Partial failure handling

```python
async with client.batch() as batch:
    good = batch.add("country.getAllCountries", {})
    bad  = batch.add("company.getById", {"companyId": "nonexistent"})

print(good.ok)     # True
print(bad.ok)      # False
if not bad.ok:
    print(bad._error)  # WareraNotFoundError
```

### Wire format (for reference)

```
POST /trpc/proc0,proc1,...,proc49?batch=1
Content-Type: application/json
X-API-Key: <token>

{"0": {input0}, "1": {input1}, ..., "49": {input49}}
```

---

## Request Cancellation (AbortController)

If you trigger a massive `collect_all()` task but the user closes their browser or navigates away, you don't want the SDK to keep burning API rate limits on background requests. You can gracefully abort operations using a `CancellationScope`.

```python
from warera import CancellationScope

async def fetch_data(scope: CancellationScope):
    try:
        async with scope:
            # If scope.cancel() is called elsewhere, this instantly raises asyncio.CancelledError
            # Any HTTP request waiting in the 5ms batch queue is silently pruned before hitting the network!
            data = await client.user.collect_all()
    except asyncio.CancelledError:
        print("Operation was gracefully cancelled!")

# Elsewhere in your application:
# scope.cancel()
```

---

## Persistent SWR Caching

By default, the SDK uses an in-memory true-LRU `OrderedDict` to cache static endpoints like `gameConfig` using Stale-While-Revalidate semantics.

To persist this data across bot restarts or server crashes, you can configure the client to use the `SQLiteCacheBackend`.

```python
from warera.cache_backends import SQLiteCacheBackend

# Creates or connects to cache.db in the current directory
client = WareraClient(cache_backend=SQLiteCacheBackend("cache.db"))
```

---

## Request Priority

In complex applications, you may have background workers fetching millions of records while a user clicks a button that needs an instant response. To prevent the user's request from getting stuck behind 10,000 background jobs in the auto-batching queue, use `RequestPriority.HIGH`.

```python
from warera import RequestPriority

# This request jumps to the very front of the internal batching queue
# and will be dispatched in the next immediate physical HTTP POST (≤ 5ms)
critical_user = await client.user.get_by_id("123", priority=RequestPriority.HIGH)
```

---

## Error Handling

```python
from warera.exceptions import (
    WareraError,             # base - catch everything
    WareraUnauthorizedError, # 401 - bad/missing API key
    WareraForbiddenError,    # 403
    WareraNotFoundError,     # 404
    WareraRateLimitError,    # 429 - auto-retried; raised after all retries exhausted
                             #   .retry_after → float | None  (seconds from Retry-After header)
    WareraServerError,       # 5xx - auto-retried
    WareraValidationError,   # Pydantic parse failure
    WareraBatchError,        # one or more batch items failed
                             #   .errors  → dict[int, WareraError]
                             #   .results → dict[int, Any]
)

try:
    user = await client.user.get_by_id("99999")
except WareraNotFoundError:
    print("User not found")
except WareraRateLimitError as e:
    print(f"Still rate-limited after retries. Retry after: {e.retry_after}s")
except WareraError as e:
    print(f"API error: {e}")
```

---

## Configuration

```python
WareraClient(
    api_key: str | None = None,        # also reads WARERA_API_KEY env var
    base_url: str = "https://api2.warera.io/trpc",
    timeout: float = 30.0,             # HTTP request timeout in seconds
    max_retries: int = 3,              # retry attempts for 429 / 5xx errors
    initial_delay_ms: int = 250,       # initial retry delay in ms
    max_delay_ms: int = 5000,          # max retry delay in ms
    backoff_multiplier: float = 2.0,   # exponential backoff multiplier
    jitter: bool = True,               # add random jitter to delays
    batch_size: int = 50,              # max procedures per batch POST chunk
                                       # values above 50 are silently clamped
                                       # to the server's hard limit
    auto_batch_delay: float = 0.005,   # wait time in seconds to accumulate batch chunks
    event_hooks: dict | None = None,   # dict mapping 'request'/'response' to async hooks
    headers: dict | None = None,       # additional custom HTTP headers to send
    retryable_status_codes: set | None = None, # custom HTTP status codes to trigger retry
    on_retry: Callable | None = None,  # called before each retry sleep with a RetryInfo
)

# on_retry example — feed retries into your own logs/metrics:
def log_retry(info: warera.RetryInfo) -> None:
    print(f"retry #{info.attempt}: HTTP {info.status_code}, waiting {info.delay_s:.2f}s")

client = WareraClient(on_retry=log_retry)

# You can also configure the extreme maximum concurrency for massive bulk fetching operations 
# (defaults to 500 to perfectly match the API rate limit). Dial this down to 50 or 100 if you
# are running in constrained environments to save memory.
# export WARERA_MAX_CONCURRENCY=50
```

---

## Project Structure

```
warera/
├── __init__.py          # public API surface
├── client.py            # WareraClient
├── sync.py              # sync shim
├── exceptions.py        # error hierarchy
├── _enums.py            # all StrEnum classes from schema
├── _http.py             # httpx session, GET/POST, rate-limit headers, retry
├── _pagination.py       # paginate(), collect_all()
├── _batch.py            # BatchSession, BatchItem, fetch_many_by_ids
├── models/              # Pydantic response models (31 files)
└── resources/           # Resource classes (32 files)
```

---

## Development

```bash
git clone https://github.com/wareraprojects/api-client-py
cd api-client-py
pip install -e ".[dev]"

# Unit tests (no API key needed)
pytest tests/unit/ -v

# Integration tests (live API)
WARERA_API_KEY=your_key pytest tests/integration/ -v

# Lint + type check
ruff check warera/
mypy warera/
```

---

## License

MIT

---

## Credits

- **[WarEraProjects](https://github.com/wareraprojects)**: Massive credit to WarEraProjects team as well as all other contributors for the [TypeScript Wrapper](https://github.com/wareraprojects/trpc) which gave a foundational reference to work with on bringing the wrapper features into python.

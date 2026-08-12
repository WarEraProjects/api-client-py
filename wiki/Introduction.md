# Introduction to the API

Welcome to the **WarEra Python Client**! This library is a robust, type-safe wrapper over the WarEra tRPC API. 

This page explains how the library maps to the raw API and the architectural patterns used under the hood to ensure extreme performance.

## How it Maps to the API

If you look at the raw [WarEra tRPC schema](https://api2.warera.io/docs), endpoints are structured as `namespace.procedureName` (e.g., `country.getAllCountries`).

This client library maps those exactly 1-to-1:
- `country` becomes `client.country`
- `getAllCountries` becomes `.get_all_countries()` (or aliases like `.get_all()`)

```python
# Raw API Request
# POST /trpc/country.getCountryById
# Body: {"countryId": "7"}

# Python SDK Equivalent
country = await client.country.get_by_id("7")
```

All responses from the API are automatically parsed into strictly-typed [Pydantic](https://docs.pydantic.dev/) models. This means your editor will automatically autocomplete fields like `country.name` and warn you if you type something wrong!

## The Three Layers

The client is built on three distinct layers that work together to maximize performance:

1. **The HTTP Engine**: Handles connection pooling, transparent retries, exponential backoff, rate limit parsing, and SWR caching.
2. **The Auto-Batching Engine**: The most powerful part of the library. It captures your individual requests (like `get_by_id`) and invisibly combines them into massive `httpBatchLink` requests to minimize round-trip latency.
3. **The Resource Layer**: The user-facing classes (like `UserResource` or `CountryResource`) that expose strongly-typed methods and parse the raw JSON into Pydantic models.

## Global Module vs Explicit Client

For most scripts, you don't even need to instantiate a client! The library exposes a global connection pool directly on the `warera` module.

```python
import warera

# Uses the global connection pool implicitly!
user = await warera.user.get_by_id("123")
```

You only need to explicitly construct a `WareraClient` if you need to:
- Use multiple different API keys simultaneously
- Inject custom telemetry hooks
- Customize the underlying batching or HTTP parameters
- Use a persistent SQLite cache backend

## Sync vs Async

The WarEra API is highly asynchronous by nature. The library is built from the ground up using `asyncio` and `httpx`.

However, if you are working in a Jupyter notebook, a simple script, or a synchronous web framework like Django/Flask, we provide a thread-safe synchronous wrapper!

```python
# Synchronous usage!
from warera.sync import WareraClient

client = WareraClient(api_key="your_key")
user = client.user.get_by_id("123")
```

The sync wrapper works by spawning a daemon thread with an isolated event loop, ensuring it never interferes with your main thread while still providing the exact same extreme performance and auto-batching benefits.

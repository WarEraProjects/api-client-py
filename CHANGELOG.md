# Changelog

## [0.2.0] — 2026-05-27

### 🚀 Major Architectural Updates

- **Global API DX**: You no longer need to instantiate `WareraClient`. Just `import warera` and call methods globally (e.g. `await warera.user.get_by_id("123")`). The client will automatically pick up the `WARERA_API_KEY` environment variable.
- **Item-Level Auto Pagination**: `get_paginated` methods now support `auto_items=True`, which transparently yields individual items across pages instead of raw `CursorPage` objects. *(Note: The old `paginate()` wrapper and `auto_paginate=True` kwarg have been completely removed).*
- **Supercharged Parallel Fetching**: `collect_all()` methods have been completely rewritten to use a parallel time-slicing engine, fetching huge histories concurrently instead of sequentially. The default time slice size has been reduced to `0.2` days globally with a concurrency of `500` to maximize batching efficiency.
- **Internal Batching Engine Fixes**: The internal `BatchSession` engine is now highly resilient against race conditions under extreme concurrent loads.
- **Optimized JSON Serialization**: Replaced standard `.json()` decoding with high-speed `orjson` across the entire HTTP lifecycle, drastically cutting CPU overhead.
- **SWR In-Memory Caching**: Static resources (like `game_config.get()`, `country.get_all()`) are aggressively cached using a Stale-While-Revalidate pattern to eliminate redundant API calls across concurrent coroutines.
- **HTTP/2 Enabled by Default**: All network requests now natively multiplex over HTTP/2, significantly lowering connection overhead latency.
- **Tracing & Logging**: Added standard python `logging` under the `warera` namespace. When enabled, it outputs debug telemetry for batch queue sizes, cache hits/misses, and automatic rate-limit sleeps.
- **Configurable Auto-Batching Delay**: The internal batch delay is now exposed via `auto_batch_delay` (default: 5ms), matching tRPC's `httpBatchLink` configuration. 
- **Middleware Event Hooks**: Exposes native `httpx` event hooks (`event_hooks={"request": [...], "response": [...]}`), acting identically to tRPC Links for custom telemetry injection.
- **Connection Resilience**: Increased default `httpx` timeout from 10s to 30s to prevent premature read timeouts when the server processes massive batches.
- **HTTP Retry Engine**: Natively implements the TypeScript wrapper's `createRetryFetch` engine. Automatically intercepts HTTP errors (`408, 409, 425, 429, 500, 502, 503, 504`) and transient network issues with configurable exponential backoff and uniform random jitter to prevent thundering herd bottlenecks.
- **Strict GameConfig Typing**: Over 75+ nested structures inside `gameConfig.getGameConfig` have been strictly typed (e.g. `GameConfigBadges`, `UpgradeConfigBunkerLevel`). The Pydantic schemas were machine-generated directly from the official TS AST to provide absolute 100% architectural schema parity, dropping the unsafe `dict[str, Any]` typings entirely.

For full details on migrating your code from `v0.1.x`, see the [v0.2.0 Migration Guide](MIGRATION-0.2.0.md).

## [0.1.9] — 2026-05-26

### New endpoints (1:1 Parity with TypeScript Client)

**BattleLootSummary**
- `client.battle_loot_summary.get_by_battle_and_user(battle_id, user_id)`

**MercenaryContractAuction**
- `client.mercenary_contract_auction.get_paginated_auctions(...)`

**Tournament**
- `client.tournament.get_last_tournament()`
- `client.tournament.get_team_by_id(tournament_team_id)`
- `client.tournament.get_teams_by_tournament(tournament_id)`

### Synchronized Pydantic Models
Massive update to sync all existing models with the latest TRPC schema. Added all missing properties (fully backwards compatible).

## [0.1.8] — 2026-05-10
*(Previous release contents omitted for brevity)*

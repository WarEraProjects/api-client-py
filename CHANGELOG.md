# Changelog

## [0.2.0] — 2026-05-27

### 🚀 Major Architectural Updates

- **Global API DX**: You no longer need to instantiate `WareraClient`. Just `import warera` and call methods globally (e.g. `await warera.user.get_by_id("123")`). The client will automatically pick up the `WARERA_API_KEY` environment variable.
- **Item-Level Auto Pagination**: `get_paginated` methods now support `auto_items=True`, which transparently yields individual items across pages instead of raw `CursorPage` objects.
- **Supercharged Parallel Fetching**: `collect_all()` methods have been completely rewritten to use a parallel time-slicing engine, fetching huge histories concurrently instead of sequentially. The default time slice size has been reduced to `0.2` days globally with a concurrency of `500` to maximize batching efficiency.
- **Internal Batching Engine Fixes**: The internal `BatchSession` engine is now highly resilient against race conditions under extreme concurrent loads.
- **Optimized JSON Serialization**: Replaced standard `.json()` decoding with high-speed `orjson` across the entire HTTP lifecycle, drastically cutting CPU overhead.
- **In-Memory Concurrency Caching**: Static resources (like `game_config.get()`, `country.find_by_name()`, `item_trading.get_prices()`) are aggressively memoized to eliminate redundant API calls across concurrent coroutines.
- **Connection Resilience**: Increased default `httpx` timeout from 10s to 30s to prevent premature read timeouts when the server processes massive batches.

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

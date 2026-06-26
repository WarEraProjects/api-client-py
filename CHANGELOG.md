# Changelog

## [0.2.2] — 2026-06-26

This release patches several critical memory, concurrency, and parsing issues reported in the 3.1 Pro extended audit.

### 🐛 Bug Fixes & Structural Improvements
- **OOM Protection in `sync.py`:** Removed `nest_asyncio` and `loop.run_until_complete`. The synchronous wrapper now spawns a dedicated daemon thread running an isolated event loop. Coroutines are securely dispatched via `run_coroutine_threadsafe`, and async generators (`auto_items=True`) are properly streamed through a thread-safe `Queue` instead of blocking and materializing lists in memory.
- **Cache Memory Limits (`_cache.py`, `_swr.py`):** Added a hard LRU size cap (1000 items) to prevent unbounded memory growth in long-running processes.
- **Auto-batching InvalidStateError (`_http.py`):** The auto-batch fast path now safely checks `fut.done()` before attempting to `set_result`, preventing background tasks from crashing if the caller timed out.
- **Rate-limit Race Conditions (`_http.py`):** The rate-limit tracker now handles out-of-order network responses accurately, preventing false "window refresh" inflations.
- **Strict Dependency Declaration:** Explicitly use standard library `typing.ParamSpec` instead of `typing_extensions` for `_cache.py`.
- **Unhashable Caching (`_cache.py`):** `async_memoize` now safely stringifies unhashable arguments (like lists/dicts) to ensure SWR hits.
- **Robust JS Date Parsing (`_pagination.py`):** Changed the fragile hardcoded `[:24]` string slice to a robust `split(" GMT")[0]` when parsing `cursor` dates.
- **Silent Batch Errors (`_batch.py`):** `fetch_many_by_ids` now correctly distinguishes between missing items (404 Not Found) and real system faults (500s, Rate Limits). Genuine faults are re-raised.
- **URL Encoding:** Fixed implicit bytes-to-string encoding issues in `orjson.dumps()`.
- **Restored `collect_all`:** Removed the deprecation warnings from `collect_all` across all resources. It is highly optimized via `parallel_collect_all` and is fully supported.
- **Async Generator Leaks (`sync.py`):** Added `threading.Event()` and bounded backpressure to the internal thread-safe `Queue` in `_run_async_gen`. If a synchronous caller breaks early out of a paginated loop, the background asyncio thread is immediately cancelled, preventing a severe memory blowout where the thread would silently fetch and stash millions of ghost-records.
- **Hanging Futures in Batching (`_http.py`):** Fixed an edge-case in `_auto_batch_flush` where an inexplicably omitted response index from a batch payload (API anomaly) would cause the corresponding waiting `Future` to never resolve, deadlocking the calling coroutine.
- **Region `active_battle` Typing:** Replaced the loosely typed `dict[str, Any]` on the `Region.active_battle` field with the strict `Battle` Pydantic model for complete IDE autocomplete coverage.
- **Client Cancellation Deadlocks (`_http.py`):** The auto-batch flusher now catches `BaseException` to correctly handle `asyncio.CancelledError`, ensuring pending futures are cleanly excepted and preventing deadlocks during `client.aclose()`.
- **Orphaned Tasks & Daemon Thread Leaks (`sync.py`):** The synchronous generator consumer now explicitly cancels the background asyncio task when broken early. Furthermore, `atexit` is now used to register a graceful `shutdown()` hook that completely terminates the background loop and daemon thread upon process exit, stopping `ssl.SSLSocket` resource leaks.
- **SWR Cache Race Conditions (`_swr.py`):** Duplicate background tasks on simultaneous stale cache misses are now prevented by synchronously assigning the pending task to the `_inflight` dictionary immediately after `loop.create_task()`.
- **True LRU Eviction (`_swr.py`):** Upgraded `SWRCache` from standard dict to `collections.OrderedDict`, utilizing `move_to_end()` to ensure evictions eject the true least-recently-used items instead of the oldest inserted items.
- **Exception Masking in Batch Flush (`_batch.py`):** Added a global exception catch-all in `_flush_chunk`. Unhandled system exceptions (like `httpx.ConnectTimeout`) are now wrapped in `WareraError` and propagated to all unresolved `BatchItem`s gracefully, resolving the cryptic "BatchItem has not been resolved yet" errors.

## [0.2.1] — 2026-06-24

### 🗺️ New Resource: Alliance

- **`client.alliance`** is now a fully wired resource namespace (was missing in 0.2.0).
- **`alliance.get(alliance_id)`** — fetch a single alliance by ID.
- **`alliance.get_many(ids)`** — batch-fetch multiple alliances by ID list.
- **`alliance.get_paginated(...)`** — cursor-paginated alliance listing with full `auto_items=True` and `cursor_end`/`max_pages` support.
- **`alliance.collect_all()`** — convenience wrapper that falls through to `parallel_collect_all`.
- New `Alliance`, `AllianceRankings`, `AllianceRankingEntry`, `AllianceMemberCountry` models, all fully typed.

### 📦 Expanded Model Exports (models `__init__.py`)

Many models introduced in 0.2.0 were not re-exported from the package root. `warera/models/__init__.py` now exports all of them explicitly:

- `BattleLootSummary`, `BattleLootPoolItem`
- `MercenaryContractAuction`, `MercenaryContractAuctionBid`
- `Equipment`, `EquipmentSkills`
- `Tournament`, `TournamentMatch`, `TournamentRound`, `TournamentTeam`, `TournamentRegistered`
- `SearchResult` (companion to the already-exported `SearchResults`)
- `CountryRankings`, `CountryTaxes`, `CountryUnrest`, `CountryStrategicResources`, `CountryStrategicResourceMap`, `CountryStrategicBonuses`
- `Government`, `GovernmentDates`, `GovernmentMember`
- `MilitaryUnit`, `MuRoles`, `MuRankings`, `MuLeveling`, `MuActiveUpgradeLevels`
- `User` sub-models: `UserDates`, `UserLeveling`, `UserPreferences`, `UserRankings`, `UserSkills`, `UserStats`, `RankingDetail`, `SkillDetail`
- `ReprMixin`, `WareraModel` (for downstream subclassing)
- `AllianceMemberCountry`, `AllianceRankingEntry`, `AllianceRankings`



### 🔬 New `async_memoize` Decorator (`_cache.py`)

Added `warera._cache.async_memoize`, an unbounded async memoization decorator with thundering-herd protection (concurrent calls for the same key share the same `Future`). Used internally; not yet part of the public API surface.

### 🌍 `WARERA_MAX_CONCURRENCY` Environment Override

The parallel time-slicing engine in `_pagination.py` now reads `WARERA_MAX_CONCURRENCY` from the environment (default: `500`) so operators can tune peak concurrency without changing code:

```bash
export WARERA_MAX_CONCURRENCY=50   # gentler on rate limits
```

### 🐍 Jupyter / `nest_asyncio` Support in Sync Client

The sync shim (`warera.sync`) now detects when it is called from inside a running event loop (e.g. Jupyter or IPython) and applies `nest_asyncio` if installed, rather than raising a `RuntimeError`. `nest_asyncio` is optional — the shim degrades gracefully to `asyncio.run()` when the library is absent.

### 🧪 Test Suite Expansion

- `test_swr.py` — new dedicated tests for `SWRCache`: basic fetch, stale-while-revalidate background refresh, and concurrent thundering-herd deduplication.
- `test_user_parsing.py` — regression tests for `User.equipped_skin_keys` (dict, not list) and `User.finished_tours` (dict, not list), locking in the 0.2.0 schema fix.
- `test_enhancements.py` — model `__str__` / `__repr__` tests, `ReprMixin` coverage, `CursorPage` iteration and `len()`, `BaseResource.__str__`, `WareraClient.__str__`, and `BatchItem` lifecycle display.
- `test_custom_resources.py` — unit tests for newer resource namespaces: `Alliance`, `Party`, `Election`, `Donation`, `GameStat`, `MuMember`, `Work`, `WorkOffer`, `ItemTrading`, `Company`.

### Bug Fixes & Architecture Parity
- Add missing 32 sub-models to root namespace and `__all__`.
- Implement `invalidate_cache()` across cache-holding resources.
- Correctly bump internal `__version__` variable to `0.2.1`.
- Fix async generator leak in `_SyncResourceProxy` causing failures in synchronous mode with `auto_items=True`.
- Update deprecation message across pagination endpoints.
- Update `EventType.PEACE_AGREEMENT` to camelCase `peaceAgreement`.
- Add test gates to PyPI publishing workflow.
- Update `pyproject.toml` repository links.

## [0.2.0] — 2026-05-27

### ✅ Live-Verified Response Schemas

Every public endpoint was validated field-by-field against live production payloads. All response models are now drift-free — every field the API returns is strictly typed (IDE autocomplete everywhere, no silent `model_extra` data):

- **Fixed `.id` mapping bug**: 11 models (`Article`, `ArticleLite`, `Company`, `Event`, `MilitaryUnit`, `ItemPrice`, `TradingOrder`, `Round`, `SearchResult`, `Upgrade`, `WorkOffer`) re-declared `id` without the `_id` alias, so `.id` was always `None`. The alias now lives once on `WareraModel`, which also gained `version` (`__v`).
- **`Country`** fully retyped from live data: taxes, unrest, strategic resources (+ bonuses), rankings, allies/wars/defensive pacts, non-aggression map, development metrics, etc. (22 new fields).
- **`Region`** fully retyped: biome/climate/position/neighbors, resistance, deposits, upgradesV2 with construction history, etc. (23 new fields).
- **`Battle`** gained typed `attacker`/`defender` sides (`BattleSide` incl. money pool & bounty fields), `stats`, `rounds`, `rounds_to_win`, `type`, timestamps.
- **`Round`** rewritten to the real schema: per-side combat stats with typed `last_hits` (full `Hit` model with weapon/equipment objects) and `live` tick state.
- **`MilitaryUnit`**: typed `roles`, `rankings`, `leveling`, upgrade levels, invested money, mercenary reputation. **`User`**: combat skill modifiers (`ammo_percent`, ...), `preferences`, `orgs`, `epic` case rarity; `UserLite` now exposes the full `dates` object the API actually returns.
- **`Tournament`** no longer crashes on live data (fractional `team_size`, optional qualification flags) and gained match `predecessors`, `won_by`, possible-team ids.
- **`GameConfig`** updated with 60+ live fields: `alliance`, `loot`, `mercenaryContract` (incl. auction + reputation), `subSkinReward`, badge availabilities/cooldowns, law alliance actions, region liberation cooldowns, skill soft caps/overflow, and more.
- `Government.dates`, `PartyEthics.unethical`, `Event.countries`/`priority`, article `slug`/`is_public`, ranking entry `tier`/`user`/`mu`, equipment item stats — all typed.
- **Auth-only endpoints verified with a live API key**: `Transaction` retyped to the real schema (`money`, `quantity`, `seller_id`, `buyer_id`, `transaction_type`, typed `item` object on market transactions), `Upgrade` retyped (status, invested resources, dependant users, upgrade/downgrade timestamps), `TradingOrder.country` added.

### 🔐 Graceful Auth Handling

- **Context-aware 401 errors**: `WareraUnauthorizedError` now tells you *why* — "no API key is configured (set `WARERA_API_KEY` / `warera.set_api_key()`)\" vs "the configured API key was rejected". Inspect `err.api_key_configured` programmatically.
- **`validate_api_key()`**: new on both clients and module-level (`await warera.validate_api_key()`, sync `warera.sync.validate_api_key()`). Returns `True`/`False` without raising; network/server errors still propagate so an outage isn't mistaken for a bad key.
- **`set_api_key(key, validate=True)`** (sync module) validates the key against the server immediately and raises if rejected.
- New `WareraClient.has_api_key` property.
- **Clearer 403s**: `WareraForbiddenError` now explains that some endpoints (work stats, action logs) only return data for the key owner's own account.
- **`on_retry` callback** (parity with the TS wrapper's `onRetry`): `WareraClient(on_retry=fn)` invokes `fn(RetryInfo(attempt, delay_s, error, status_code))` before each retry sleep — ideal for custom metrics/alerting. Callback exceptions are logged and never break the retry loop. `RetryInfo` is exported from the package root.

### 🖨️ Full-Value Printing & Typed User Fields

- **`print(model)` now shows every field and value.** The old `__str__` override (`<User username>`) hid all data; models now use Pydantic's default rendering (`id='…' username='…' leveling=UserLeveling(level=10, …)`). The same applies to `CursorPage` and the plain helper classes (`CompanyProductionBonus`, `RecommendedRegion`, `WageRange`, `WageStats`, `PublicOrdersSummary`) via a new `ReprMixin` that renders every attribute.
- **`User.equipped_skin_keys` / `User.finished_tours` fixed for real-world payloads**: v0.1.x typed these as `list[str]` while the live API returns `dict[str, str]` and `dict[str, bool]`, which made `User.model_validate` raise and forced consumers to monkey-patch the raw response. The dict typings (already corrected in the 0.2 model sync) are now locked in with regression tests — any such monkey patches can be deleted.

### 🔎 Schema Parity Fixes (final 0.2.0 polish)

- **Restored production base URL**: the default `base_url` accidentally pointed at `https://apidev.warera.io/trpc` (a dev mirror) during the 0.2 refactor. It now correctly defaults to `https://api2.warera.io/trpc`, matching the official docs and the TypeScript client.
- **`EventType` enum completed**: added `allianceMemberJoined`, `allianceMemberLeft`, `allianceMemberExcluded`, `defensivePactFormed`, `defensivePactBroken` (now 26 values, in sync with the official OpenAPI spec).
- **`TransactionType` enum completed**: added `countryMoneyTransfer`.
- **New `MercenaryAuctionStatus` enum** (`active`, `won`, `expiredNoBids`, `expiredBattle`, `expiredRound`, `cancelled`, `terminated`) — `mercenary_contract_auction.get_paginated_auctions(status=...)` is now typo-safe.
- **`work_offer.get_paginated` gained the `level` filter** documented in the official spec.
- **Bug fix**: `mercenary_contract_auction.get_paginated_auctions(auto_items=True)` no longer drops an explicitly supplied initial `cursor`.

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

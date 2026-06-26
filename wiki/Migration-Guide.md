# Migration Guide

Welcome to the WarEra Python Client migration guide! Find your target version below to see what changes you need to make to upgrade.

---

## Migrating to v0.2.2

Version `0.2.2` introduces massive internal stability and memory-safety patches following a comprehensive architecture audit. The public API surface is completely backwards-compatible, but the underlying engines have changed.

### From v0.2.0 / v0.2.1
If you are upgrading from `0.2.0` or `0.2.1`, no code changes are required! Just bump your package version.
However, note the following behavioral improvements:
1. **OOM Memory Protection**: The background synchronous thread wrapper now utilizes backpressure on the generator queue. If you use `get_paginated(auto_items=True)` in synchronous mode over thousands of items, it will no longer bloat your RAM.
2. **Cache Safety**: `async_memoize` now enforces a strict 1000-item LRU cap, and properly hashes complex dictionary arguments to prevent cache collisions.
3. **Cursor Parsing**: JS Date string truncation was rebuilt robustly (`split(" GMT")[0]`) to prevent timezone parsing crashes on pagination endpoints.
4. **Batching Resilience**: The `InvalidStateError` race conditions in `_auto_batch_flush` were resolved, and rate-limit headers properly track out-of-order network responses.

### From v0.1.x
If you are upgrading from `0.1.x`, please read the **v0.2.0 Migration Guide** as there were massive breaking changes to the pagination engines, including the removal of `paginate()` and `auto_paginate=True` in favor of `get_paginated(auto_items=True)` and `collect_all()`.

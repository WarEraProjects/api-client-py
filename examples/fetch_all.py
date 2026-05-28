"""
warera-client benchmark / data fetch example.

Usage:
    # Interactive mode (prompts for API key and user ID):
    python examples/fetch_all.py

    # Full benchmark (non-interactive, requires API key):
    python examples/fetch_all.py --benchmark
    python examples/fetch_all.py --benchmark --api-key YOUR_KEY

    # Environment variable also works:
    WARERA_API_KEY=YOUR_KEY python examples/fetch_all.py --benchmark
"""

import argparse
import asyncio
import contextlib
import os
import time
import typing

import warera

# ── Timing & stats helpers ──────────────────────────────────────────────


class BenchmarkTimer:
    """Records named timing sections and per-section quota snapshots."""

    def __init__(self) -> None:
        self._sections: list[dict[str, typing.Any]] = []
        self._t0 = time.perf_counter()

    @contextlib.contextmanager
    def section(self, emoji: str, label: str) -> typing.Iterator["_SectionResult"]:
        """Context manager that records elapsed time and quota delta for a section."""
        t = time.perf_counter()
        result = _SectionResult()

        # Snapshot stats before the section runs
        client = warera.get_client()
        stats_before = dict(client.stats)

        yield result

        elapsed = time.perf_counter() - t
        stats_after = dict(client.stats)

        self._sections.append(
            {
                "emoji": emoji,
                "label": label,
                "count": result.count,
                "elapsed": elapsed,
                "http_reqs": (stats_after.get("total_http_requests") or 0)
                - (stats_before.get("total_http_requests") or 0),
                "procedures": (stats_after.get("total_procedures") or 0)
                - (stats_before.get("total_procedures") or 0),
                "window_refreshes": (stats_after.get("window_refreshes") or 0)
                - (stats_before.get("window_refreshes") or 0),
                "wait_secs": (stats_after.get("total_wait_seconds") or 0.0)
                - (stats_before.get("total_wait_seconds") or 0.0),
            }
        )

    @property
    def total_elapsed(self) -> float:
        return time.perf_counter() - self._t0

    def print_summary(self) -> None:
        """Print the formatted benchmark results table with full stats."""
        client = warera.get_client()
        s = client.stats

        # ── Phase breakdown table ──
        w = 72
        print()
        print(f"  ╔{'═' * w}╗")
        print(f"  ║  {'Benchmark Results':<{w - 3}}║")
        print(f"  ╠{'═' * w}╣")
        print(
            f"  ║  {'Phase':<20}│ {'Items':>8} │ {'Time':>8} │ {'Reqs':>6} │ {'Procs':>7} │ {'Waits':>5} ║"
        )
        print(f"  ║  {'─' * 20}┼{'─' * 10}┼{'─' * 10}┼{'─' * 8}┼{'─' * 9}┼{'─' * 7}║")

        for sec in self._sections:
            tag = f"{sec['emoji']} {sec['label']}"
            waits = sec["window_refreshes"]
            wait_str = f"{waits}" if waits > 0 else "—"
            print(
                f"  ║  {tag:<20}│ {sec['count']:>8,} │ "
                f"{sec['elapsed']:>7.3f}s │ {sec['http_reqs']:>6} │ "
                f"{sec['procedures']:>7} │ {wait_str:>5} ║"
            )

        print(f"  ║  {'─' * 20}┼{'─' * 10}┼{'─' * 10}┼{'─' * 8}┼{'─' * 9}┼{'─' * 7}║")
        total = self.total_elapsed
        total_reqs = s.get("total_http_requests") or 0
        total_procs = s.get("total_procedures") or 0
        total_waits = s.get("window_refreshes") or 0
        print(
            f"  ║  {'⏱️  Total':<20}│ {'':>8} │ "
            f"{total:>7.3f}s │ {total_reqs:>6} │ "
            f"{total_procs:>7} │ {total_waits:>5} ║"
        )
        print(f"  ╚{'═' * w}╝")

        # ── Detailed network / quota stats ──
        print()
        print(f"  ┌{'─' * w}┐")
        print(f"  │  {'Network & Quota Statistics':<{w - 3}}│")
        print(f"  ├{'─' * w}┤")

        print(f"  │  📡 HTTP Requests      : {total_reqs:>6}  (GET + batch POST){' ' * 20}│")
        print(
            f"  │  📦 tRPC Procedures    : {total_procs:>6}  (individual calls, incl. batched){' ' * 5}│"
        )

        # Batching efficiency
        if total_reqs > 0:
            batch_ratio = total_procs / total_reqs
            print(
                f"  │  ⚡ Batch Efficiency   : {batch_ratio:>6.1f}× (avg procedures per HTTP request){' ' * 4}│"
            )
        else:
            print(f"  │  ⚡ Batch Efficiency   :    N/A{' ' * 39}│")

        # Rate limit window info
        quota_per = s["quota_limit_per_window"]
        quota_rem = s["quota_remaining"]
        quota_used_cw = s["quota_used_current_window"]

        if quota_per is not None:
            print(f"  │  🪟 Window Size        : {quota_per:>6}  requests/window{' ' * 23}│")
        else:
            print(f"  │  🪟 Window Size        :    N/A{' ' * 39}│")

        if total_waits > 0:
            wait_time = s.get("total_wait_seconds") or 0.0
            print(
                f"  │  🔄 Window Refreshes   : {total_waits:>6}  ({wait_time:.1f}s spent waiting){' ' * (20 - len(f'{wait_time:.1f}'))}│"
            )
            # Total quota consumed across all windows is simply the total HTTP requests made,
            # as each HTTP request consumes exactly 1 quota token regardless of batching.
            print(
                f"  │  🔥 Total Quota Used   : {total_reqs:>6}  across {total_waits + 1} window(s){' ' * (18 - len(str(total_waits + 1)))}│"
            )
        else:
            print(f"  │  🔄 Window Refreshes   :      0  (stayed within single window){' ' * 7}│")

        if quota_used_cw is not None and quota_per is not None:
            pct = (quota_used_cw / quota_per) * 100
            bar_len = 20
            filled = int(bar_len * quota_used_cw / quota_per)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(
                f"  │  📊 Current Window     : {quota_used_cw:>6}/{quota_per} used ({pct:.0f}%) {bar}{' ' * (9 - len(str(quota_per)))}│"
            )

        if quota_rem is not None:
            print(
                f"  │  💚 Remaining          : {quota_rem:>6}  requests in current window{' ' * 12}│"
            )

        print(f"  └{'─' * w}┘")
        print()


class _SectionResult:
    """Mutable holder so the section context manager can capture item counts."""

    __slots__ = ("count",)

    def __init__(self) -> None:
        self.count = 0


def _elapsed(t0: float) -> str:
    return f"{time.perf_counter() - t0:.3f}s"


# ── User transaction fetch (interactive mode) ──────────────────────────


async def fetch_user_transactions(target: str) -> None:
    timer = BenchmarkTimer()
    user = None

    with timer.section("🔍", "User Lookup") as sec:
        # Try fetching as ID first
        with contextlib.suppress(warera.WareraError):
            user = await warera.user.get_by_id(target)

        if not user:
            print(f"  🔍 Searching for user '{target}'...")
            search_res = await warera.search.query(target)
            user_ids = [r.id for r in search_res.results if r.type == "user" and r.id]
            if not user_ids:
                print(f"  ❌ Could not find any user matching '{target}'.")
                return

            # Take the first matched user
            try:
                user = await warera.user.get_by_id(user_ids[0])
            except warera.WareraError:
                print(f"  ❌ Failed to fetch user profile for ID {user_ids[0]}")
                return
        sec.count = 1

    print(f"  ✅ Found user: {user.username} (ID: {user.id})")

    with timer.section("💸", "Transactions") as sec:
        print(f"\n  ⏳ Fetching all transactions for {user.username}...")
        # Use the highly optimized parallel transaction fetcher, passing the user's creation
        # date so it knows exactly how far back to slice time.
        txs = await warera.transaction.collect_all(
            user_id=user.id,
            limit=100,
            oldest_date=user.created_at or "",
            time_slice_days=0.05,
            concurrency=1000,
        )
        sec.count = len(txs)
        print(f"  ✅ Fetched {len(txs)} transactions in {_elapsed(timer._t0)}")

    timer.print_summary()


# ── Full benchmark (non-interactive) ───────────────────────────────────


async def run_benchmark() -> None:
    timer = BenchmarkTimer()

    # ── Phase 1: Countries ──
    with timer.section("🌍", "Countries") as sec:
        print("  ⏳ Fetching all countries...")
        countries = await warera.country.get_all()
        sec.count = len(countries)
        print(f"  ✅ {len(countries)} countries in {_elapsed(timer._t0)}")

    # ── Phase 2: All users across all countries ──
    with timer.section("👤", "Users") as sec:
        t0 = time.perf_counter()
        print("\n  ⏳ Fetching all users from every country...")
        all_users = await warera.user.collect_all(concurrency=20)
        sec.count = len(all_users)
        print(f"  ✅ {len(all_users)} users in {_elapsed(t0)}")

    # ── Phase 3: All companies (global paginated fetch) ──
    with timer.section("🏭", "Companies") as sec:
        t0 = time.perf_counter()
        print("\n  ⏳ Fetching all companies...")
        all_companies = await warera.company.collect_all()
        sec.count = len(all_companies)
        print(f"  ✅ {len(all_companies)} companies in {_elapsed(t0)}")

    timer.print_summary()

    # Clean up the global client session
    await warera.get_client().aclose()


# ── Main entry point ──────────────────────────────────────────────────


async def main() -> None:
    parser = argparse.ArgumentParser(description="warera-client benchmark / data fetch")
    parser.add_argument(
        "--api-key", default=None, help="API key (overrides WARERA_API_KEY env var)"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run full benchmark (non-interactive): Countries → Users → Companies",
    )
    args = parser.parse_args()

    print("\n┌──────────────────────────────────────────────────┐")
    print("│  warera-client · Full Data Fetch                 │")
    print("│  Countries → Users → Companies                  │")
    print("└──────────────────────────────────────────────────┘\n")

    # ── Resolve API key ──
    api_key = args.api_key or os.environ.get("WARERA_API_KEY")
    if api_key:
        print("  🔑 Using API key from", "CLI arg." if args.api_key else "WARERA_API_KEY env var.")
    elif not args.benchmark:
        api_key = input("  🔑 Enter API key (or press Enter for anonymous): ").strip() or None
        if api_key:
            print("  🔑 Using provided API key.")
        else:
            print("  ⚠️  No API key — running anonymously (lower rate limits).")
    else:
        print("  ⚠️  No API key — running anonymously (lower rate limits).")
    print()

    if api_key:
        warera.set_api_key(api_key)

    # ── Benchmark mode ──
    if args.benchmark:
        await run_benchmark()
        return

    # ── Interactive mode ──
    print("\n  ==================================================")
    target = input(
        "  👤 Enter a user ID/username for transactions (or press Enter for full massive fetch): "
    ).strip()
    print("  ==================================================\n")
    if target:
        await fetch_user_transactions(target)
        await warera.get_client().aclose()
        return

    # Full fetch (same as benchmark but interactive)
    await run_benchmark()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  ❌ Aborted by user.")

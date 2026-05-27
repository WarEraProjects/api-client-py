import asyncio
import os
import time

import warera


def _elapsed(t0: float) -> str:
    return f"{time.perf_counter() - t0:.1f}s"


async def main() -> None:
    print("\n┌──────────────────────────────────────────────────┐")
    print("│  warera-client · Full Data Fetch                 │")
    print("│  Countries → Users → Companies                  │")
    print("└──────────────────────────────────────────────────┘\n")

    # ── Resolve API key and set global configuration ──
    api_key = os.environ.get("WARERA_API_KEY")
    if api_key:
        print("  🔑 Using API key from WARERA_API_KEY env var.")
    else:
        api_key = input("  🔑 Enter API key (or press Enter for anonymous): ").strip() or None
        if api_key:
            print("  🔑 Using provided API key.")
        else:
            print("  ⚠️  No API key — running anonymously (lower rate limits).")
    print()

    if api_key:
        warera.set_api_key(api_key)

    # ── Phase 1: Countries (Cached automatically) ──
    t0 = time.perf_counter()
    print("  ⏳ Fetching all countries...")
    # This caches the result in memory automatically using @async_memoize
    countries = await warera.country.get_all()
    print(f"  ✅ {len(countries)} countries in {_elapsed(t0)}")

    # ── Phase 2: All users across all countries ──
    t0 = time.perf_counter()
    print("\n  ⏳ Fetching all users from every country...")
    # Get all users by querying every country ID
    # Because auto_paginate_pages is optimized, we can just use collect_all for each country
    all_users = []
    
    # We use a semaphore to avoid hitting the API with 180 concurrent pagination loops
    sem = asyncio.Semaphore(20)
    
    async def fetch_country_users(cid: str) -> None:
        async with sem:
            async for page in await warera.user.get_by_country(country_id=cid, limit=50, auto_paginate=True):
                all_users.extend(page.items)

    await asyncio.gather(*[fetch_country_users(c.id) for c in countries.values() if c.id])
    print(f"  ✅ {len(all_users)} users in {_elapsed(t0)}")

    # ── Phase 3: All companies (batched via native Auto-Batcher) ──
    t0 = time.perf_counter()
    print("\n  ⏳ Fetching companies for every user...")
    user_ids = [u.id for u in all_users if u.id]
    
    # We use the optimized collect_by_users which leverages native BatchSession internally
    all_companies = await warera.company.collect_by_users(user_ids)
    print(f"  ✅ {len(all_companies)} companies in {_elapsed(t0)}")

    # ── Final summary ──
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  Summary                                         ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  🌍 Countries : {len(countries):<32} ║")
    print(f"║  👤 Users     : {len(all_users):<32} ║")
    print(f"║  🏭 Companies : {len(all_companies):<32} ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    # Clean up the global client session
    await warera.get_client().aclose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  ❌ Aborted by user.")

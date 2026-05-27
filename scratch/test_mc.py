import asyncio
import time
import os
import sys
import warera

async def main():
    warera.set_api_key("wae_e94b43de3c36a7762815eaaf51a563a1d15d3824efddecaa562f31a6e60b53c6")
    print("Searching for MasterChief...")
    search_res = await warera.search.query("MasterChief")
    user_ids = [r.id for r in search_res.results if r.type == "user" and r.id]
    if not user_ids:
        print("Not found.")
        return
    user = await warera.user.get_by_id(user_ids[0])
    print(f"Found {user.username} (ID: {user.id})")
    
    t0 = time.perf_counter()
    txs = await warera.transaction.collect_all(
        user_id=user.id,
        limit=100,
        oldest_date=user.created_at,
        time_slice_days=0.05,
        concurrency=500,
    )
    t1 = time.perf_counter()
    print(f"Fetched {len(txs)} transactions in {t1 - t0:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())

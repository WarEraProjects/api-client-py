"""
Basic async usage example.
"""

import asyncio
import os

import warera


async def main() -> None:
    # Set the global API key.
    warera.set_api_key(os.environ.get("WARERA_API_KEY", ""))

    # --- Country lookups ---
    # get_all() is automatically cached in memory, so repeated calls are instant
    # and don't consume rate limit.
    all_countries = await warera.country.get_all()
    print(f"Total countries: {len(all_countries)}")

    india = await warera.country.find_by_name("India")
    if india and india.id:
        print(f"India ID: {india.id}")

        # --- Government ---
        gov = await warera.government.get(india.id)
        print(f"India Gov: {gov.model_dump() if gov else 'None'}")

    # --- Concurrent User fetching ---
    # To fetch multiple things concurrently, just use asyncio.gather!
    # The client's Auto-Batcher intercepts these requests, chunks them into
    # batches of 50, and sends them over the network in a single POST request.
    user_ids = ["1", "2", "3", "4", "5"]
    print(f"\nFetching {len(user_ids)} users concurrently...")

    users = await asyncio.gather(
        *[warera.user.get_by_id(uid) for uid in user_ids], return_exceptions=True
    )

    for uid, user in zip(user_ids, users, strict=True):
        if isinstance(user, BaseException):
            print(f"User {uid}: Error - {user}")
        else:
            print(f"User {uid}: {user.username if user else 'Not found'}")

    # Explicit cleanup of the global background tasks and HTTP connections
    await warera.get_client().aclose()


if __name__ == "__main__":
    asyncio.run(main())

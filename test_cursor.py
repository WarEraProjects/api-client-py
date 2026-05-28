import asyncio
from datetime import datetime, timedelta, timezone

import warera


async def inspect_cursor() -> None:
    warera.set_api_key("wae_e94b43de3c36a7762815eaaf51a563a1d15d3824efddecaa562f31a6e60b53c6")

    # 1. Fetch exactly the first page to get a baseline date
    page = await warera.transaction.get_paginated(user_id="690d6b03becd7485dbb33b05", limit=1)

    if not page.next_cursor:
        return

    date_part, id_part = page.next_cursor.split("|", 1)

    # Let's generate a date 60 days ago
    # We can format it as JS Date string: "Wed May 27 2026 05:41:00 GMT+0000 (Coordinated Universal Time)"
    # But wait, Python's strftime doesn't exactly match JS Date.toString().
    # Let's try ISO format instead, since the server might parse it.

    print("\nTrying ISO synthetic cursor...")
    iso_date = (datetime.now(timezone.utc) - timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    iso_cursor = f"{iso_date}|000000000000000000000000"

    try:
        page2 = await warera.transaction.get_paginated(
            user_id="690d6b03becd7485dbb33b05", limit=2, cursor=iso_cursor
        )
        print(f"ISO cursor success! Got {len(page2.items)} items.")
        for item in page2.items:
            print(f"  Item date: {item.created_at}")
    except Exception as e:
        print(f"ISO cursor failed: {e}")

    print("\nTrying JS string format synthetic cursor...")
    # Just manipulate the date string
    js_date = (datetime.now(timezone.utc) - timedelta(days=60)).strftime(
        "%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)"
    )
    js_cursor = f"{js_date}|000000000000000000000000"
    try:
        page3 = await warera.transaction.get_paginated(
            user_id="690d6b03becd7485dbb33b05", limit=2, cursor=js_cursor
        )
        print(f"JS cursor success! Got {len(page3.items)} items.")
        for item in page3.items:
            print(f"  Item date: {item.created_at}")
    except Exception as e:
        print(f"JS cursor failed: {e}")


asyncio.run(inspect_cursor())

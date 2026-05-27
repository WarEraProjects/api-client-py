import asyncio

import warera


async def test_limit():
    warera.set_api_key("wae_e94b43de3c36a7762815eaaf51a563a1d15d3824efddecaa562f31a6e60b53c6")
    try:
        page = await warera.transaction.get_paginated(user_id="690d6b03becd7485dbb33b05", limit=200)
        print(f"Success! Got {len(page.items)} items with limit=200")
    except Exception as e:
        print(f"Error with limit=200: {e}")

    try:
        page = await warera.transaction.get_paginated(user_id="690d6b03becd7485dbb33b05", limit=250)
        print(f"Success! Got {len(page.items)} items with limit=250")
    except Exception as e:
        print(f"Error with limit=250: {e}")

asyncio.run(test_limit())

import asyncio
import warera

async def main():
    warera.set_api_key("wae_e94b43de3c36a7762815eaaf51a563a1d15d3824efddecaa562f31a6e60b53c6")
    page = await warera.transaction.get_paginated(
        user_id="693593a89291a4015d868c17", 
        limit=1000
    )
    print(f"Limit 1000 returned {len(page.items)} items")

if __name__ == "__main__":
    asyncio.run(main())

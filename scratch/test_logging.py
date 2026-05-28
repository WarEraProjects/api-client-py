import asyncio
import logging
from unittest.mock import AsyncMock

from warera._http import HttpSession

logging.basicConfig(level=logging.WARNING)
logging.getLogger("warera").setLevel(logging.DEBUG)


async def main():
    http = HttpSession()
    # Mock post_batch so it doesn't actually hit the network
    http.post_batch = AsyncMock(return_value=[{"data": "mock"}])
    
    # Fire off a request
    print("Sending request...")
    res = await http.get("test.proc", {"arg": "val"})
    print("Result:", res)


if __name__ == "__main__":
    asyncio.run(main())

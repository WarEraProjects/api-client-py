import asyncio

import warera

# Create a client (Make sure WARERA_API_KEY is set in your environment if needed)
client = warera.WareraClient()


async def fetch_data(scope: warera.CancellationScope) -> None:
    print("Starting a large request...")

    # We wrap our request inside the cancellation scope.
    # Any warera API calls made inside this 'async with' block will be bound to the scope.
    try:
        async with scope:
            # We use an artificially large fetch to ensure we have time to cancel it.
            # Using get_many will auto-batch these IDs.
            # If the batch is extremely large, it will chunk it.
            ids = [str(i) for i in range(100, 200)]
            print(f"Fetching {len(ids)} users...")

            users = await client.user.get_many(ids)
            print(f"Success! Fetched {len(users)} users.")

    except asyncio.CancelledError:
        print("\n[!] Request was successfully cancelled before it could finish!")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")


async def cancel_after_delay(scope: warera.CancellationScope, delay: float) -> None:
    """Wait for a brief moment, then pull the plug."""
    await asyncio.sleep(delay)
    print(f"\n---> Triggering scope.cancel() after {delay} seconds! <---")
    scope.cancel()


async def main() -> None:
    # 1. Create a CancellationScope
    scope = warera.CancellationScope()

    # 2. Run the fetch task and the cancel task concurrently
    fetch_task = asyncio.create_task(fetch_data(scope))
    cancel_task = asyncio.create_task(cancel_after_delay(scope, delay=0.01))

    # Wait for both tasks to complete
    await asyncio.gather(fetch_task, cancel_task)

    print("\nProgram finished gracefully.")


if __name__ == "__main__":
    asyncio.run(main())

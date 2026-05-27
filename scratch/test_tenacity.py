import asyncio
import tenacity

async def test():
    retrying = tenacity.AsyncRetrying(
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_exception_type(RuntimeError),
        reraise=True
    )
    print("starting loop")
    result = None
    try:
        async for attempt in retrying:
            with attempt:
                print("attempting")
                raise ValueError("failed")
                result = 1
    except Exception as e:
        print("Caught exception outside loop:", type(e))
    print("loop finished, result is:", result)

if __name__ == "__main__":
    asyncio.run(test())

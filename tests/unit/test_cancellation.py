import asyncio
import concurrent.futures
import threading
import time

import pytest
import respx
from httpx import Response

from warera import CancellationScope, WareraClient
from warera.sync import WareraClient as SyncClient


@pytest.mark.asyncio
async def test_cancellation_scope_aborts_active_request() -> None:
    """Test that cancelling the scope instantly aborts a slow HTTP request."""

    async def slow_endpoint(request):
        await asyncio.sleep(2.0)
        return Response(
            200,
            json={
                "result": {
                    "data": {
                        "id": "1",
                        "username": "test",
                        "leveling": {"level": 1, "experience": 0},
                    }
                }
            },
        )

    with respx.mock(base_url="https://api2.warera.io/trpc", assert_all_called=False) as mock:
        mock.get(path__startswith="/user.getUserById").mock(side_effect=slow_endpoint)

        scope = CancellationScope()

        async with WareraClient(api_key="test_key") as client:

            async def fetch():
                async with scope:
                    return await client.user.get_by_id("1")

            fetch_task = asyncio.create_task(fetch())

            # Wait briefly to let the request hit the mock and start sleeping
            await asyncio.sleep(0.1)

            # Abort the scope!
            scope.cancel()

            with pytest.raises(asyncio.CancelledError):
                await fetch_task


@pytest.mark.asyncio
async def test_cancellation_scope_aborts_batch() -> None:
    """Test that cancelling a batch aborts all waiting futures."""

    async def slow_batch(request):
        await asyncio.sleep(2.0)
        return Response(200, json=[{"result": {"data": {"id": "1", "username": "test"}}}])

    with respx.mock(base_url="https://api2.warera.io/trpc", assert_all_called=False) as mock:
        mock.post(path__startswith="/user.getUserById").mock(side_effect=slow_batch)

        scope = CancellationScope()

        async with WareraClient(api_key="test_key") as client:

            async def fetch():
                async with scope:
                    # using get_many will trigger post_batch
                    return await client.user.get_many(["1", "2"])

            fetch_task = asyncio.create_task(fetch())

            await asyncio.sleep(0.1)
            scope.cancel()

            with pytest.raises(asyncio.CancelledError):
                await fetch_task


def test_sync_cancellation_scope_aborts_request() -> None:
    """Test that the cancellation scope correctly crosses the sync/async bridge via contextvars."""

    async def slow_endpoint(request):
        await asyncio.sleep(5.0)  # Make it very slow
        return Response(200, json={"result": {"data": {"id": "1", "username": "test"}}})

    with respx.mock(base_url="https://api2.warera.io/trpc", assert_all_called=False) as mock:
        mock.get(path__startswith="/user.getUserById").mock(side_effect=slow_endpoint)

        scope = CancellationScope()
        client = SyncClient(api_key="test_key")

        with client:
            results = []
            exceptions = []

            def worker():
                try:
                    with scope:
                        results.append(client.user.get_by_id("1"))
                except Exception as e:
                    exceptions.append(e)

            t = threading.Thread(target=worker)
            t.start()

            # Wait briefly to ensure the background task has started
            time.sleep(0.2)

            # Cancel from the main thread!
            scope.cancel()
            t.join(timeout=1.0)

            assert not t.is_alive(), "Worker thread did not terminate in time"
            assert len(results) == 0, "Request should not have succeeded"
            assert len(exceptions) == 1, "Expected an exception to be raised"
            assert isinstance(exceptions[0], concurrent.futures.CancelledError)

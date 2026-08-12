import asyncio
from unittest.mock import AsyncMock

import pytest

from warera._enums import RequestPriority
from warera._http import HttpSession


@pytest.mark.asyncio
async def test_priority_queueing() -> None:
    session = HttpSession()
    session._ensure_client = AsyncMock()  # type: ignore

    # Mock the actual post_batch
    mock_post_batch = AsyncMock()
    # Return dummy results
    mock_post_batch.side_effect = lambda procs, inps, **kwargs: [{} for _ in procs]
    session.post_batch = mock_post_batch  # type: ignore[method-assign]

    # Queue up a few requests with different priorities
    # We don't want them to flush immediately, so we mock auto_batch_delay a bit longer
    session._auto_batch_delay = 0.05

    # Start requests
    f_low = asyncio.create_task(session.get("proc.low", {}, priority=RequestPriority.LOW))
    f_normal1 = asyncio.create_task(
        session.get("proc.normal1", {}, priority=RequestPriority.NORMAL)
    )
    f_normal2 = asyncio.create_task(
        session.get("proc.normal2", {}, priority=RequestPriority.NORMAL)
    )
    f_high = asyncio.create_task(session.get("proc.high", {}, priority=RequestPriority.HIGH))

    # wait for all of them to resolve
    await asyncio.gather(f_low, f_normal1, f_normal2, f_high)

    # Check post_batch call arguments
    # We should have seen high flush instantly, breaking the batch,
    # or if they all got queued, high is first.
    # Actually, HIGH priority sets the event, which instantly wakes up the flusher.
    # So HIGH might be flushed in its own chunk, or with whatever was already queued.
    # Let's inspect what procedures were passed to post_batch.

    assert mock_post_batch.called

    # Let's check the first call's procedures
    # It might contain HIGH, or HIGH might have jumped the queue of the *first* flush
    calls = mock_post_batch.call_args_list
    all_flushed_procs = []
    for call in calls:
        procs = call[0][0]
        all_flushed_procs.extend(procs)

    # Since they are queued extremely fast, it's very likely they all make it into one flush,
    # OR they get split because HIGH triggers the flush instantly.
    # Let's verify that if they are in the same batch, HIGH is before NORMAL before LOW.

    if len(calls) == 1:
        procs = calls[0][0][0]
        assert procs[0] == "proc.high"
        assert procs[-1] == "proc.low"

    assert "proc.high" in all_flushed_procs
    assert "proc.low" in all_flushed_procs

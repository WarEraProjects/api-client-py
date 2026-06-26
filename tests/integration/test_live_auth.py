"""
Integration tests for authenticated endpoints against the live WarEra API.

These tests require a valid API key and are skipped entirely when
``WARERA_API_KEY`` is not set (e.g. PRs from forks where secrets are
unavailable). In CI the key is injected from the repository secret.

Run locally with:
    WARERA_API_KEY=your_key pytest tests/integration/test_live_auth.py -v
"""

from __future__ import annotations

import os

import pytest
import pytest_asyncio

from warera import WareraClient, WareraForbiddenError
from warera.models import Equipment, Transaction, Upgrade, Worker

EXAMPLE_USER_ID = "6999b242abdf5405edb36d57"

pytestmark = pytest.mark.skipif(
    not os.environ.get("WARERA_API_KEY"),
    reason="WARERA_API_KEY not set — skipping authenticated endpoint tests",
)


@pytest_asyncio.fixture(scope="module")
async def client():
    async with WareraClient() as c:
        yield c


# ---------------------------------------------------------------------------
# key validation
# ---------------------------------------------------------------------------


async def test_validate_api_key(client):
    assert client.has_api_key is True
    assert await client.validate_api_key() is True


# ---------------------------------------------------------------------------
# transaction (auth-only)
# ---------------------------------------------------------------------------


async def test_transactions_paginated(client):
    page = await client.transaction.get_paginated(limit=10)
    assert len(page.items) > 0
    for txn in page.items:
        assert isinstance(txn, Transaction)
        assert txn.id is not None
        assert txn.transaction_type is not None
    # `money` is present on monetary types (wage, trading, ...) but absent on
    # others (e.g. dismantleItem) — assert it only where applicable.
    monetary = [t for t in page.items if t.transaction_type in ("wage", "trading", "itemMarket")]
    for txn in monetary:
        assert txn.money is not None


async def test_transactions_item_object_is_typed(client):
    page = await client.transaction.get_paginated(limit=50, transaction_type="itemMarket")
    with_item = [t for t in page.items if t.item is not None]
    if not with_item:
        pytest.skip("no recent itemMarket transactions with an item object")
    item = with_item[0].item
    assert isinstance(item, Equipment)
    assert item.code is not None


# ---------------------------------------------------------------------------
# worker (auth-only)
# ---------------------------------------------------------------------------


async def test_get_workers_by_user(client):
    workers = await client.worker.get_workers(user_id=EXAMPLE_USER_ID)
    assert isinstance(workers, list)
    if workers:
        assert isinstance(workers[0], Worker)


async def test_get_total_workers_count(client):
    count = await client.worker.get_total_count(EXAMPLE_USER_ID)
    assert isinstance(count, int)
    assert count >= 0


# ---------------------------------------------------------------------------
# upgrade (verified with auth, works for any region)
# ---------------------------------------------------------------------------


async def test_get_region_upgrade(client):
    regions = await client.region.get_all()
    region_id = next(iter(regions.values())).id
    upgrade = await client.upgrade.get("bunker", region_id=region_id)
    assert isinstance(upgrade, Upgrade)
    assert upgrade.upgrade_type == "bunker"
    assert upgrade.region_id == region_id


# ---------------------------------------------------------------------------
# own-account-only endpoints surface a clear 403 for other users
# ---------------------------------------------------------------------------


async def test_work_stats_for_other_user_raises_clear_403(client):
    with pytest.raises(WareraForbiddenError) as exc_info:
        await client.work.get_stats_by_user(EXAMPLE_USER_ID, days=7, timezone="UTC")
    assert "own account" in str(exc_info.value)

from __future__ import annotations

import unittest.mock as mock

from warera._batch import BatchSession
from warera.client import WareraClient
from warera.models.common import CursorPage, WareraModel
from warera.models.user import User


def test_warera_model_str_shows_all_fields():
    user = User(_id="123", username="testuser")
    rendered = str(user)
    # Pydantic's default rendering: every field is visible, values included.
    assert "id='123'" in rendered
    assert "username='testuser'" in rendered
    assert "leveling=" in rendered

    class SimpleModel(WareraModel):
        pass

    m = SimpleModel(_id="999")
    assert "id='999'" in str(m)
    assert "SimpleModel" in repr(m)


def test_repr_mixin_shows_all_attributes():
    from warera.resources.company import CompanyProductionBonus
    from warera.resources.work_offer import WageRange

    bonus = CompanyProductionBonus.from_raw({"strategicBonus": 1, "total": 5})
    rendered = repr(bonus)
    for field in (
        "strategic_bonus",
        "deposit_bonus",
        "ethic_specialization_bonus",
        "ethic_deposit_bonus",
        "total",
    ):
        assert field in rendered

    wage = WageRange({"min": 1, "max": 2, "average": 1.5})
    assert repr(wage) == "WageRange(min=1.0, max=2.0, average=1.5)"


def test_cursor_page_iter_and_len():
    items = [User(_id=str(i), username=f"u{i}") for i in range(3)]
    page = CursorPage(items=items, has_more=False)

    assert len(page) == 3
    collected = list(page)
    assert len(collected) == 3
    assert collected[0].username == "u0"


def test_base_resource_str():
    # BaseResource is usually instantiated for a namespace
    client = WareraClient(api_key="test")
    assert str(client.user) == "<UserResource>"


def test_warera_client_str():
    client = WareraClient(api_key="test")
    assert "WareraClient(authenticated=True" in str(client)


def test_batch_str():
    http = mock.MagicMock()
    session = BatchSession(http)
    item = session.add("user.get", {"userId": "1"})

    assert str(session) == "<BatchSession queued=1>"
    assert len(session) == 1
    assert str(item) == "<BatchItem user.get (pending)>"

    item._resolve({"id": "1"})
    assert str(item) == "<BatchItem user.get (resolved)>"

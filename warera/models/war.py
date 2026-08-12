from .common import WareraModel


class War(WareraModel):
    """War model."""

    id: str
    status: str | None = None
    attacker_id: str | None = None
    defender_id: str | None = None
    model_config = {"extra": "allow"}

"""
warera-client — Python client for the WarEra tRPC API

Quick start:
    import asyncio
    from warera import WareraClient

    async def main():
        async with WareraClient(api_key="YOUR_KEY") as client:
            user = await client.user.get_by_id("12345")
            print(user.username)

    asyncio.run(main())

Sync:
    from warera.sync import WareraClient
    client = WareraClient(api_key="YOUR_KEY")
    user = client.user.get_by_id("12345")
"""

import typing

from ._enums import (
    ActionLogActionType,
    ArticleType,
    BattleDirection,
    BattleFilter,
    BattleOrderSide,
    BattleRankingDataType,
    BattleRankingEntityType,
    BattleRankingSide,
    EventType,
    MercenaryAuctionStatus,
    RankingType,
    TransactionType,
    UpgradeType,
)
from ._http import RetryInfo
from .client import WareraClient
from .exceptions import (
    WareraBatchError,
    WareraError,
    WareraForbiddenError,
    WareraHTTPError,
    WareraNotFoundError,
    WareraRateLimitError,
    WareraServerError,
    WareraUnauthorizedError,
    WareraValidationError,
)
from .models import (
    ActionLog,
    Alliance,
    AllianceMemberCountry,
    AllianceRankingEntry,
    AllianceRankings,
    Article,
    ArticleLite,
    Battle,
    BattleLive,
    BattleLootPoolItem,
    BattleLootSummary,
    BattleOrder,
    BattleRankingEntry,
    Company,
    Country,
    CountryRankings,
    CountryStrategicBonuses,
    CountryStrategicResourceMap,
    CountryStrategicResources,
    CountryTaxes,
    CountryUnrest,
    CursorPage,
    Donation,
    DonationTotals,
    Election,
    ElectionCandidate,
    Equipment,
    EquipmentSkills,
    Event,
    GameConfig,
    GameDates,
    Government,
    GovernmentDates,
    Hit,
    ItemOffer,
    ItemPrice,
    MercenaryContractAuction,
    MercenaryContractAuctionBid,
    MilitaryUnit,
    MuActiveUpgradeLevels,
    MuLeveling,
    MuMember,
    MuRankings,
    MuRoles,
    Party,
    PartyEthics,
    RankingDetail,
    RankingEntry,
    Region,
    ReprMixin,
    Round,
    SearchResult,
    SearchResults,
    SkillDetail,
    Tournament,
    TournamentMatch,
    TournamentRegistered,
    TournamentRound,
    TournamentTeam,
    TradingOrder,
    Transaction,
    Upgrade,
    User,
    UserDates,
    UserLeveling,
    UserLite,
    UserPreferences,
    UserRankings,
    UserSkills,
    UserStats,
    WareraModel,
    Worker,
    WorkerCount,
    WorkOffer,
    WorkStats,
)

if typing.TYPE_CHECKING:
    from .resources.action_log import ActionLogResource
    from .resources.alliance import AllianceResource
    from .resources.article import ArticleResource
    from .resources.battle import BattleResource
    from .resources.battle_loot_summary import BattleLootSummaryResource
    from .resources.battle_order import BattleOrderResource
    from .resources.battle_ranking import BattleRankingResource
    from .resources.company import CompanyResource
    from .resources.country import CountryResource
    from .resources.donation import DonationResource
    from .resources.election import ElectionResource
    from .resources.event import EventResource
    from .resources.game_config import GameConfigResource
    from .resources.game_stat import GameStatResource
    from .resources.government import GovernmentResource
    from .resources.inventory import InventoryResource
    from .resources.item_trading import ItemTradingResource
    from .resources.mercenary_contract_auction import MercenaryContractAuctionResource
    from .resources.mu import MUResource
    from .resources.mu_member import MuMemberResource
    from .resources.party import PartyResource
    from .resources.ranking import RankingResource
    from .resources.region import RegionResource
    from .resources.round_ import RoundResource
    from .resources.search import SearchResource
    from .resources.tournament import TournamentResource
    from .resources.transaction import TransactionResource
    from .resources.upgrade import UpgradeResource
    from .resources.user import UserResource
    from .resources.work import WorkResource
    from .resources.work_offer import WorkOfferResource
    from .resources.worker import WorkerResource

    action_log: ActionLogResource
    alliance: AllianceResource
    article: ArticleResource
    battle: BattleResource
    battle_loot_summary: BattleLootSummaryResource
    battle_order: BattleOrderResource
    battle_ranking: BattleRankingResource
    company: CompanyResource
    country: CountryResource
    donation: DonationResource
    election: ElectionResource
    event: EventResource
    game_config: GameConfigResource
    game_stat: GameStatResource
    government: GovernmentResource
    inventory: InventoryResource
    item_trading: ItemTradingResource
    mercenary_contract_auction: MercenaryContractAuctionResource
    mu: MUResource
    mu_member: MuMemberResource
    party: PartyResource
    ranking: RankingResource
    region: RegionResource
    round: RoundResource
    search: SearchResource
    tournament: TournamentResource
    transaction: TransactionResource
    upgrade: UpgradeResource
    user: UserResource
    work: WorkResource
    work_offer: WorkOfferResource
    worker: WorkerResource


_default_client: WareraClient | None = None
api_key: str | None = None


def set_api_key(key: str) -> None:
    """Configure the global API key for the module-level client."""
    global api_key, _default_client
    api_key = key
    if _default_client is not None:
        _default_client._http._api_key = key


def get_client() -> WareraClient:
    """Get or create the global WareraClient."""
    global _default_client
    if _default_client is None:
        _default_client = WareraClient(api_key=api_key)
    return _default_client


async def validate_api_key() -> bool:
    """
    Check whether the configured API key is accepted by the server.

    Returns ``True`` if the key is valid, ``False`` if no key is configured
    or the server rejected it. Typical flow::

        warera.set_api_key("...")
        if not await warera.validate_api_key():
            raise SystemExit("invalid WarEra API key")
    """
    return await get_client().validate_api_key()


_RESOURCE_NAMES = {
    "action_log",
    "alliance",
    "article",
    "battle",
    "battle_loot_summary",
    "battle_order",
    "battle_ranking",
    "company",
    "country",
    "donation",
    "election",
    "event",
    "game_config",
    "game_stat",
    "government",
    "inventory",
    "item_trading",
    "mercenary_contract_auction",
    "mu",
    "mu_member",
    "party",
    "ranking",
    "region",
    "round",
    "search",
    "tournament",
    "transaction",
    "upgrade",
    "user",
    "work",
    "work_offer",
    "worker",
}


def __getattr__(name: str) -> typing.Any:
    if name in _RESOURCE_NAMES:
        return getattr(get_client(), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__version__ = "0.2.2"

__all__ = [
    # Client
    "WareraClient",
    "set_api_key",
    "get_client",
    "validate_api_key",
    "RetryInfo",
    # Exceptions
    "WareraError",
    "WareraHTTPError",
    "WareraUnauthorizedError",
    "WareraForbiddenError",
    "WareraNotFoundError",
    "WareraRateLimitError",
    "WareraServerError",
    "WareraValidationError",
    "WareraBatchError",
    # Enums
    "ActionLogActionType",
    "ArticleType",
    "BattleDirection",
    "BattleFilter",
    "BattleOrderSide",
    "BattleRankingDataType",
    "BattleRankingEntityType",
    "BattleRankingSide",
    "EventType",
    "MercenaryAuctionStatus",
    "RankingType",
    "TransactionType",
    "UpgradeType",
    # Models
    "ActionLog",
    "Alliance",
    "AllianceMemberCountry",
    "AllianceRankingEntry",
    "AllianceRankings",
    "Article",
    "ArticleLite",
    "Battle",
    "BattleLootPoolItem",
    "BattleLootSummary",
    "BattleLive",
    "BattleOrder",
    "BattleRankingEntry",
    "Company",
    "Country",
    "CountryRankings",
    "CountryStrategicBonuses",
    "CountryStrategicResourceMap",
    "CountryStrategicResources",
    "CountryTaxes",
    "CountryUnrest",
    "CursorPage",
    "Donation",
    "DonationTotals",
    "Election",
    "ElectionCandidate",
    "Equipment",
    "EquipmentSkills",
    "Event",
    "GameConfig",
    "GameDates",
    "Government",
    "GovernmentDates",
    "Hit",
    "ItemOffer",
    "ItemPrice",
    "MercenaryContractAuction",
    "MercenaryContractAuctionBid",
    "MilitaryUnit",
    "MuActiveUpgradeLevels",
    "MuLeveling",
    "MuMember",
    "MuRankings",
    "MuRoles",
    "Party",
    "PartyEthics",
    "RankingDetail",
    "RankingEntry",
    "Region",
    "ReprMixin",
    "Round",
    "SearchResult",
    "SearchResults",
    "SkillDetail",
    "Tournament",
    "TournamentMatch",
    "TournamentRegistered",
    "TournamentRound",
    "TournamentTeam",
    "TradingOrder",
    "Transaction",
    "Upgrade",
    "User",
    "UserDates",
    "UserLeveling",
    "UserLite",
    "UserPreferences",
    "UserRankings",
    "UserSkills",
    "UserStats",
    "WareraModel",
    "WorkOffer",
    "WorkStats",
    "Worker",
    "WorkerCount",
]

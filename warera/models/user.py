from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class UserLiteDates(WareraModel):
    last_connection_at: str | None = Field(
        default=None, description="The timestamp of the user's last login."
    )
    last_taking_control_at: str | None = Field(
        default=None, description="The timestamp of the last taking control event."
    )


class UserDates(UserLiteDates):
    last_notifications_check_at: str | None = None
    last_country_message_check_at: str | None = None
    last_global_message_check_at: str | None = None
    last_events_check_at: str | None = None
    last_work_offer_applications: list[str] | None = None
    last_hires_at: list[str] | None = None
    last_work_at: str | None = None
    last_company_joined_at: str | None = None
    last_daily_reward_claimed_at: str | None = None
    last_skills_reset_at: str | None = None
    last_help_asked_at: str | None = None
    last_citizenship_change_at: str | None = None


class UserLeveling(WareraModel):
    level: int | None = Field(default=None, description="The current overall level of the entity.")
    total_xp: int | None = Field(
        default=None, description="The total lifetime experience points accumulated."
    )
    daily_xp_left: int | None = Field(
        default=None,
        description="The remaining experience points the user can earn today before hitting the daily cap.",
    )
    available_skill_points: int | None = Field(
        default=None, description="Unspent skill points awarded from leveling up."
    )
    spent_skill_points: int | None = Field(default=None, description="The spent skill points.")
    total_skill_points: int | None = Field(default=None, description="The total skill points.")
    free_reset: int | None = Field(default=None, description="The free reset.")


class SkillDetail(WareraModel):
    level: int | None = Field(default=None, description="The current overall level of the entity.")
    current_bar_value: float | None = Field(default=None, description="The current bar value.")
    value: float | None = Field(default=None, description="The value.")
    weapon: float | None = Field(default=None, description="The weapon.")
    equipment: float | None = Field(default=None, description="The equipment.")
    limited: float | None = Field(default=None, description="The limited.")
    total: float | None = Field(default=None, description="The total.")
    hourly_bar_regen: float | None = Field(default=None, description="The hourly bar regen.")
    total_after_soft_cap: float | None = Field(
        default=None, description="The total after soft cap."
    )
    overflow: float | None = Field(default=None, description="The overflow.")
    # Combat modifiers (returned on attack-type skills)
    ammo_percent: float | None = Field(default=None, description="The ammo percent.")
    buffs_percent: float | None = Field(default=None, description="The buffs percent.")
    debuffs_percent: float | None = Field(default=None, description="The debuffs percent.")
    military_rank_percent: float | None = Field(
        default=None, description="The military rank percent."
    )


class UserSkills(WareraModel):
    energy: SkillDetail | None = Field(default=None, description="The energy.")
    health: SkillDetail | None = Field(default=None, description="The health.")
    hunger: SkillDetail | None = Field(default=None, description="The hunger.")
    attack: SkillDetail | None = Field(default=None, description="The attack.")
    companies: SkillDetail | None = Field(default=None, description="The companies.")
    entrepreneurship: SkillDetail | None = Field(default=None, description="The entrepreneurship.")
    production: SkillDetail | None = Field(default=None, description="The production.")
    critical_chance: SkillDetail | None = Field(default=None, description="The critical chance.")
    critical_damages: SkillDetail | None = Field(default=None, description="The critical damages.")
    armor: SkillDetail | None = Field(default=None, description="The armor.")
    precision: SkillDetail | None = Field(default=None, description="The precision.")
    dodge: SkillDetail | None = Field(default=None, description="The dodge.")
    loot_chance: SkillDetail | None = Field(default=None, description="The loot chance.")
    management: SkillDetail | None = Field(default=None, description="The management.")


class UserStatsWealth(WareraModel):
    companies: float | None = Field(default=None, description="The companies.")
    items: float | None = Field(default=None, description="The items.")
    money: float | None = Field(default=None, description="The money.")
    equipments: float | None = Field(default=None, description="The equipments.")
    weapons: float | None = Field(default=None, description="The weapons.")
    total: float | None = Field(default=None, description="The total.")


class UserStatsCase1ByRarity(WareraModel):
    common: int | None = Field(default=None, description="The common.")
    uncommon: int | None = Field(default=None, description="The uncommon.")
    rare: int | None = Field(default=None, description="The rare.")
    epic: int | None = Field(default=None, description="The epic.")
    legendary: int | None = Field(default=None, description="The legendary.")


class UserStatsCase1(WareraModel):
    by_rarity: UserStatsCase1ByRarity | None = Field(default=None, description="The by rarity.")
    opened_count: int | None = Field(default=None, description="The total number of opened.")


class UserStats(WareraModel):
    estimated_company_values: float | None = Field(
        default=None, description="The estimated company values."
    )
    estimated_inventory_value: float | None = Field(
        default=None, description="The estimated inventory value."
    )
    estimated_wealth: float | None = Field(default=None, description="The estimated wealth.")
    works_count: int | None = Field(default=None, description="The total number of works.")
    damages_count: int | None = Field(default=None, description="The total number of damages.")
    wealth: UserStatsWealth | None = Field(default=None, description="The wealth.")
    case1: UserStatsCase1 | None = Field(default=None, description="The case1.")


class RankingDetail(WareraModel):
    value: float | None = Field(default=None, description="The value.")
    rank: int | None = Field(default=None, description="The rank.")
    tier: str | None = Field(default=None, description="The tier.")
    country: str | None = Field(
        default=None, description="The UUID of the country this user holds citizenship in."
    )


class UserRankings(WareraModel):
    user_damages: RankingDetail | None = Field(default=None, description="The user damages.")
    weekly_user_damages: RankingDetail | None = Field(
        default=None, description="The weekly user damages."
    )
    user_wealth: RankingDetail | None = Field(default=None, description="The user wealth.")
    user_level: RankingDetail | None = Field(default=None, description="The user level.")
    user_referrals: RankingDetail | None = Field(default=None, description="The user referrals.")
    user_terrain: RankingDetail | None = Field(default=None, description="The user terrain.")
    user_cases_opened: RankingDetail | None = Field(
        default=None, description="The user cases opened."
    )
    user_bounty: RankingDetail | None = Field(default=None, description="The user bounty.")
    user_gems_purchased: RankingDetail | None = Field(
        default=None, description="The user gems purchased."
    )
    user_premium_gifts: RankingDetail | None = Field(
        default=None, description="The user premium gifts."
    )
    user_premium_months: RankingDetail | None = Field(
        default=None, description="The user premium months."
    )
    user_subscribers: RankingDetail | None = Field(
        default=None, description="The user subscribers."
    )


class UserEquipment(WareraModel):
    ammo: str | None = Field(default=None, description="The ammo.")
    helmet: str | None = Field(default=None, description="The helmet.")
    chest: str | None = Field(default=None, description="The chest.")
    boots: str | None = Field(default=None, description="The boots.")
    pants: str | None = Field(default=None, description="The pants.")
    gloves: str | None = Field(default=None, description="The gloves.")
    weapon: str | None = Field(default=None, description="The weapon.")


class UserMissionsClaimedAt(WareraModel):
    starting: str | None = Field(default=None, description="The starting.")
    daily: str | None = Field(default=None, description="The daily.")
    weekly: str | None = Field(default=None, description="The weekly.")
    monthly: str | None = Field(default=None, description="The monthly.")


class UserMissions(WareraModel):
    claimed_at: UserMissionsClaimedAt | None = Field(default=None, description="The claimed at.")
    rerolled_daily_missions: int | None = Field(
        default=None, description="The rerolled daily missions."
    )
    rerolled_weekly_missions: int | None = Field(
        default=None, description="The rerolled weekly missions."
    )


class UserInfos(WareraModel):
    color_scheme: str | None = Field(default=None, description="The color scheme.")
    description: str | None = Field(default=None, description="The description.")
    font: str | None = Field(default=None, description="The font.")
    is_premium: bool | None = Field(default=None, description="The is premium.")
    premium_gifts_count: int | None = Field(
        default=None, description="The total number of premium gifts."
    )
    premium_months_count: int | None = Field(
        default=None, description="The total number of premium months."
    )
    vice_president_of: str | None = Field(default=None, description="The vice president of.")


class UserPreferences(WareraModel):
    auto_replace_on_break: bool | None = Field(
        default=None, description="The auto replace on break."
    )
    auto_equip_mode: str | None = Field(default=None, description="The auto equip mode.")
    app_font: str | None = Field(default=None, description="The app font.")
    app_pattern: str | None = Field(default=None, description="The app pattern.")
    locale: str | None = Field(default=None, description="The locale.")
    sfx: bool | None = Field(default=None, description="The sfx.")
    colorblind: bool | None = Field(default=None, description="The colorblind.")


class UserLite(WareraModel):
    username: str | None = Field(default=None, description="The unique display name of the user.")
    username_lower: str | None = Field(
        default=None,
        description="The lowercase version of the username used for case-insensitive indexing.",
    )
    can_onboard: bool | None = Field(
        default=None,
        description="Whether the user is a new player eligible for the onboarding tutorial.",
    )
    country: str | None = Field(
        default=None, description="The UUID of the country this user holds citizenship in."
    )
    is_active: bool | None = Field(
        default=None,
        description="Whether the user has logged in recently and is considered an active player.",
    )
    avatar_url: str | None = Field(
        default=None, description="The CDN URL pointing to the user's profile picture."
    )
    mu: str | None = Field(
        default=None, description="The UUID of the Military Unit this user belongs to."
    )
    military_rank: int | None = Field(
        default=None,
        description="The total military rank points indicating the user's overall combat experience.",
    )
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
    email_verified: bool | None = Field(
        default=None,
        description="Whether the user has verified their email address to unlock trading and chat.",
    )
    # user.getUserLite returns the full dates object, same as user.getUserById.
    dates: UserDates | None = Field(default=None, description="The dates.")
    leveling: UserLeveling | None = Field(default=None, description="The leveling.")
    stats: UserStats | None = Field(default=None, description="The stats.")
    rankings: UserRankings | None = Field(
        default=None, description="The country's current standing in the global leaderboards."
    )
    infos: UserInfos | None = Field(default=None, description="The infos.")
    skills: UserSkills | None = Field(default=None, description="The skills.")
    equipped_skin_keys: dict[str, str] | None = Field(
        default=None, description="The equipped skin keys."
    )


class User(UserLite):
    dates: UserDates | None = None
    skills: UserSkills | None = None
    missions: UserMissions | None = None
    equipment: UserEquipment | None = None
    party: str | None = None
    company: str | None = None
    mu_max_level_rewarded: int | None = None
    available_color_schemes: list[str] | None = None
    equipped_skin_keys: dict[str, str] | None = None
    finished_tours: dict[str, bool] | None = None
    should_update_profile: bool | None = None
    orgs: list[str] | None = None
    preferences: UserPreferences | None = None

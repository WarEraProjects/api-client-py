"""
Strict game-configuration models.

Auto-generated from WarEra TypeScript responses.
Do not edit by hand.
"""
from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import WareraModel


class BadgeRewardWithPreserve(WareraModel):
    preserve_between_reset: bool | None = Field(default=None, alias="preserveBetweenReset")
    reward: float | None = Field(default=None, alias="reward")
    availabilities: list[str] | None = Field(default=None, alias="availabilities")
    cooldown_days: int | None = Field(default=None, alias="cooldownDays")

class BadgeReward(WareraModel):
    reward: float | None = Field(default=None, alias="reward")
    availabilities: list[str] | None = Field(default=None, alias="availabilities")
    cooldown_days: int | None = Field(default=None, alias="cooldownDays")

class BadgeRewardWithMetadata(WareraModel):
    preserve_between_reset: bool | None = Field(default=None, alias="preserveBetweenReset")
    reward: float | None = Field(default=None, alias="reward")
    unique_metadata_key: str | None = Field(default=None, alias="uniqueMetadataKey")
    availabilities: list[str] | None = Field(default=None, alias="availabilities")
    cooldown_days: int | None = Field(default=None, alias="cooldownDays")

class GameConfigBadges(WareraModel):
    alpha_tester: BadgeRewardWithPreserve | None = Field(default=None, alias="alphaTester")
    baby_boomer: BadgeRewardWithPreserve | None = Field(default=None, alias="babyBoomer")
    battle_terrain_top1: BadgeReward | None = Field(default=None, alias="battleTerrainTop1")
    battle_top1: BadgeReward | None = Field(default=None, alias="battleTop1")
    bug_finder: BadgeRewardWithPreserve | None = Field(default=None, alias="bugFinder")
    coffee: BadgeRewardWithPreserve | None = Field(default=None, alias="coffee")
    congress_member: BadgeReward | None = Field(default=None, alias="congressMember")
    council_member: BadgeRewardWithPreserve | None = Field(default=None, alias="councilMember")
    country_president: BadgeReward | None = Field(default=None, alias="countryPresident")
    country_tournament_winner: BadgeRewardWithPreserve | None = Field(default=None, alias="countryTournamentWinner")
    exploit_finder: BadgeRewardWithPreserve | None = Field(default=None, alias="exploitFinder")
    founding_father: BadgeRewardWithPreserve | None = Field(default=None, alias="foundingFather")
    gift_premium: BadgeRewardWithPreserve | None = Field(default=None, alias="giftPremium")
    giveaway_winner: BadgeReward | None = Field(default=None, alias="giveawayWinner")
    gov_member: BadgeRewardWithPreserve | None = Field(default=None, alias="govMember")
    hard_worker: BadgeReward | None = Field(default=None, alias="hardWorker")
    mu_tournament_winner: BadgeRewardWithPreserve | None = Field(default=None, alias="muTournamentWinner")
    popular_article: BadgeRewardWithMetadata | None = Field(default=None, alias="popularArticle")
    premium: BadgeRewardWithPreserve | None = Field(default=None, alias="premium")
    referral: BadgeReward | None = Field(default=None, alias="referral")
    reset_survivor: BadgeRewardWithPreserve | None = Field(default=None, alias="resetSurvivor")
    round_terrain_top1: BadgeReward | None = Field(default=None, alias="roundTerrainTop1")
    round_top1: BadgeReward | None = Field(default=None, alias="roundTop1")
    staff: BadgeRewardWithPreserve | None = Field(default=None, alias="staff")
    sugar_daddy: BadgeRewardWithPreserve | None = Field(default=None, alias="sugarDaddy")
    translator: BadgeRewardWithPreserve | None = Field(default=None, alias="translator")
    vice_president: BadgeReward | None = Field(default=None, alias="vicePresident")
    voted: BadgeReward | None = Field(default=None, alias="voted")

class BattleTickPoints(WareraModel):
    val_1: int | None = Field(default=None, alias="1")
    val_100: int | None = Field(default=None, alias="100")
    val_200: int | None = Field(default=None, alias="200")
    val_300: int | None = Field(default=None, alias="300")
    val_400: int | None = Field(default=None, alias="400")
    val_500: int | None = Field(default=None, alias="500")

class GameConfigBattle(WareraModel):
    alliance_damages_bonus_percent: float | None = Field(default=None, alias="allianceDamagesBonusPercent")
    cases_per1k_damages_in_pool: float | None = Field(default=None, alias="casesPer1kDamagesInPool")
    country_order_bonus_percent: float | None = Field(default=None, alias="countryOrderBonusPercent")
    enemy_damages_bonus_percent: float | None = Field(default=None, alias="enemyDamagesBonusPercent")
    health_cost: float | None = Field(default=None, alias="healthCost")
    hit_for1_case_in_pool: int | None = Field(default=None, alias="hitFor1CaseInPool")
    lost_attacking_region_malus_percent: float | None = Field(default=None, alias="lostAttackingRegionMalusPercent")
    max_rounds: int | None = Field(default=None, alias="maxRounds")
    mu_order_bonus_percent: float | None = Field(default=None, alias="muOrderBonusPercent")
    occupying_your_regions_malus_percent: float | None = Field(default=None, alias="occupyingYourRegionsMalusPercent")
    patriotic_bonus_percent: float | None = Field(default=None, alias="patrioticBonusPercent")
    points_to_win_round: int | None = Field(default=None, alias="pointsToWinRound")
    region_not_linked_to_capital_malus_percent: float | None = Field(default=None, alias="regionNotLinkedToCapitalMalusPercent")
    rounds_to_win: int | None = Field(default=None, alias="roundsToWin")
    set_country_order_money_cost: float | None = Field(default=None, alias="setCountryOrderMoneyCost")
    set_mu_order_money_cost: float | None = Field(default=None, alias="setMuOrderMoneyCost")
    set_order_money_cost: float | None = Field(default=None, alias="setOrderMoneyCost")
    tick_points: BattleTickPoints | None = Field(default=None, alias="tickPoints")
    gov_member_bounty_reward_percent: float | None = Field(default=None, alias="govMemberBountyRewardPercent")
    rankings_loot_percent_per_1k_dmg: float | None = Field(default=None, alias="rankingsLootPercentPer1kDmg")

class GameConfigCitizenshipApplication(WareraModel):
    auto_approval_enabled: bool | None = Field(default=None, alias="autoApprovalEnabled")
    auto_approval_max_population: int | None = Field(default=None, alias="autoApprovalMaxPopulation")

class GameConfigCompany(WareraModel):
    change_item_cost: float | None = Field(default=None, alias="changeItemCost")
    construction_cost_increase_per_company: float | None = Field(default=None, alias="constructionCostIncreasePerCompany")
    deposit_resource_bonus: float | None = Field(default=None, alias="depositResourceBonus")
    destruction_value_percent: float | None = Field(default=None, alias="destructionValuePercent")
    move_cost: float | None = Field(default=None, alias="moveCost")

class GameConfigCountry(WareraModel):
    hijacked_tax_percent_per_resistance: float | None = Field(default=None, alias="hijackedTaxPercentPerResistance")
    max_tax_amount: int | None = Field(default=None, alias="maxTaxAmount")

class GameConfigElection(WareraModel):
    candidate_duration_hours: int | None = Field(default=None, alias="candidateDurationHours")
    candidate_min_level: int | None = Field(default=None, alias="candidateMinLevel")
    election_vote_duration_hours: int | None = Field(default=None, alias="electionVoteDurationHours")
    vote_min_level: int | None = Field(default=None, alias="voteMinLevel")

class GameConfigGovernmentAnnouncement(WareraModel):
    max_per_hour: int | None = Field(default=None, alias="maxPerHour")
    duration_hours: int | None = Field(default=None, alias="durationHours")

class GameConfigGovernment(WareraModel):
    resistance_decreased_cooldown_in_hours: int | None = Field(default=None, alias="resistanceDecreasedCooldownInHours")
    resistance_increased_cooldown_in_hours: int | None = Field(default=None, alias="resistanceIncreasedCooldownInHours")
    announcement: GameConfigGovernmentAnnouncement | None = Field(default=None, alias="announcement")
    member_wage_percent: float | None = Field(default=None, alias="memberWagePercent")
    president_wage_percent: float | None = Field(default=None, alias="presidentWagePercent")
    nomination_cooldown_days: int | None = Field(default=None, alias="nominationCooldownDays")

class ItemFlatStatsPercentAttack(WareraModel):
    percent_attack: float | None = Field(default=None, alias="percentAttack")

class ItemProductionNeedsLead(WareraModel):
    lead: float | None = Field(default=None, alias="lead")

class ItemAmmo(WareraModel):
    code: str | None = Field(default=None, alias="code")
    flat_stats: ItemFlatStatsPercentAttack | None = Field(default=None, alias="flatStats")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsLead | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemDynamicStatsDodge(WareraModel):
    dodge: list[float] | None = Field(default=None, alias="dodge")

class ItemBoots(WareraModel):
    code: str | None = Field(default=None, alias="code")
    dynamic_stats: ItemDynamicStatsDodge | None = Field(default=None, alias="dynamicStats")
    icon_img: str | None = Field(default=None, alias="iconImg")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemFlatStatsHealthRegen(WareraModel):
    health_regen: float | None = Field(default=None, alias="healthRegen")
    health_regen_percent: float | None = Field(default=None, alias="healthRegenPercent")

class ItemIconComponent(WareraModel):
    compare: Any | None = Field(default=None, alias="compare")

class ItemProductionNeedsGrain(WareraModel):
    grain: float | None = Field(default=None, alias="grain")

class ItemBread(WareraModel):
    code: str | None = Field(default=None, alias="code")
    flat_stats: ItemFlatStatsHealthRegen | None = Field(default=None, alias="flatStats")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    icon_img: str | None = Field(default=None, alias="iconImg")
    is_consumable: bool | None = Field(default=None, alias="isConsumable")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsGrain | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemCase(WareraModel):
    code: str | None = Field(default=None, alias="code")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemDynamicStatsArmor(WareraModel):
    armor: list[float] | None = Field(default=None, alias="armor")

class ItemChestOrPants(WareraModel):
    code: str | None = Field(default=None, alias="code")
    dynamic_stats: ItemDynamicStatsArmor | None = Field(default=None, alias="dynamicStats")
    icon_img: str | None = Field(default=None, alias="iconImg")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemDepositResource(WareraModel):
    climates: list[str] | None = Field(default=None, alias="climates")
    code: str | None = Field(default=None, alias="code")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    is_deposit: bool | None = Field(default=None, alias="isDeposit")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemFlatStatsCocain(WareraModel):
    buff_duration_hours: int | None = Field(default=None, alias="buffDurationHours")
    debuff_duration_hours: float | None = Field(default=None, alias="debuffDurationHours")
    percent_attack: float | None = Field(default=None, alias="percentAttack")

class ItemProductionNeedsCoca(WareraModel):
    coca: float | None = Field(default=None, alias="coca")

class ItemCocain(WareraModel):
    code: str | None = Field(default=None, alias="code")
    flat_stats: ItemFlatStatsCocain | None = Field(default=None, alias="flatStats")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsCoca | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemProductionNeedsLimestone(WareraModel):
    limestone: float | None = Field(default=None, alias="limestone")

class ItemConcrete(WareraModel):
    code: str | None = Field(default=None, alias="code")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsLimestone | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemProductionNeedsFish(WareraModel):
    fish: float | None = Field(default=None, alias="fish")

class ItemCookedFish(WareraModel):
    code: str | None = Field(default=None, alias="code")
    flat_stats: ItemFlatStatsHealthRegen | None = Field(default=None, alias="flatStats")
    is_consumable: bool | None = Field(default=None, alias="isConsumable")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsFish | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemDynamicStatsPrecision(WareraModel):
    precision: list[float] | None = Field(default=None, alias="precision")

class ItemGloves(WareraModel):
    code: str | None = Field(default=None, alias="code")
    dynamic_stats: ItemDynamicStatsPrecision | None = Field(default=None, alias="dynamicStats")
    icon_img: str | None = Field(default=None, alias="iconImg")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemDynamicStatsWeaponBase(WareraModel):
    attack: list[float] | None = Field(default=None, alias="attack")
    critical_chance: list[float] | None = Field(default=None, alias="criticalChance")

class ItemWeaponMeleeOrHeavy(WareraModel):
    code: str | None = Field(default=None, alias="code")
    dynamic_stats: ItemDynamicStatsWeaponBase | None = Field(default=None, alias="dynamicStats")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemHeavyAmmo(WareraModel):
    code: str | None = Field(default=None, alias="code")
    flat_stats: ItemFlatStatsPercentAttack | None = Field(default=None, alias="flatStats")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsLead | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemDynamicStatsCriticalDamages(WareraModel):
    critical_damages: list[float] | None = Field(default=None, alias="criticalDamages")

class ItemHelmet(WareraModel):
    code: str | None = Field(default=None, alias="code")
    dynamic_stats: ItemDynamicStatsCriticalDamages | None = Field(default=None, alias="dynamicStats")
    icon_img: str | None = Field(default=None, alias="iconImg")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemRawResource(WareraModel):
    climates: list[str] | None = Field(default=None, alias="climates")
    code: str | None = Field(default=None, alias="code")
    is_deposit: bool | None = Field(default=None, alias="isDeposit")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemRifleLike(WareraModel):
    code: str | None = Field(default=None, alias="code")
    dynamic_stats: ItemDynamicStatsWeaponBase | None = Field(default=None, alias="dynamicStats")
    rarity: str | None = Field(default=None, alias="rarity")
    skin_slot: str | None = Field(default=None, alias="skinSlot")
    type: str | None = Field(default=None, alias="type")
    usage: str | None = Field(default=None, alias="usage")

class ItemProductionNeedsPetroleum(WareraModel):
    petroleum: float | None = Field(default=None, alias="petroleum")

class ItemOil(WareraModel):
    code: str | None = Field(default=None, alias="code")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsPetroleum | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemScraps(WareraModel):
    code: str | None = Field(default=None, alias="code")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemProductionNeedsLivestock(WareraModel):
    livestock: float | None = Field(default=None, alias="livestock")

class ItemSteak(WareraModel):
    code: str | None = Field(default=None, alias="code")
    flat_stats: ItemFlatStatsHealthRegen | None = Field(default=None, alias="flatStats")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    is_consumable: bool | None = Field(default=None, alias="isConsumable")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsLivestock | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemProductionNeedsIron(WareraModel):
    iron: float | None = Field(default=None, alias="iron")

class ItemSteel(WareraModel):
    code: str | None = Field(default=None, alias="code")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsIron | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemWood(WareraModel):
    climates: list[str] | None = Field(default=None, alias="climates")
    code: str | None = Field(default=None, alias="code")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    is_deposit: bool | None = Field(default=None, alias="isDeposit")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class ItemProductionNeedsWood(WareraModel):
    wood: float | None = Field(default=None, alias="wood")

class ItemPaper(WareraModel):
    code: str | None = Field(default=None, alias="code")
    icon_component: ItemIconComponent | None = Field(default=None, alias="IconComponent")
    is_tradable: bool | None = Field(default=None, alias="isTradable")
    production_needs: ItemProductionNeedsWood | None = Field(default=None, alias="productionNeeds")
    production_points: int | None = Field(default=None, alias="productionPoints")
    rarity: str | None = Field(default=None, alias="rarity")
    type: str | None = Field(default=None, alias="type")

class GameConfigItems(WareraModel):
    ammo: ItemAmmo | None = Field(default=None, alias="ammo")
    boots1: ItemBoots | None = Field(default=None, alias="boots1")
    boots2: ItemBoots | None = Field(default=None, alias="boots2")
    boots3: ItemBoots | None = Field(default=None, alias="boots3")
    boots4: ItemBoots | None = Field(default=None, alias="boots4")
    boots5: ItemBoots | None = Field(default=None, alias="boots5")
    boots6: ItemBoots | None = Field(default=None, alias="boots6")
    bread: ItemBread | None = Field(default=None, alias="bread")
    case1: ItemCase | None = Field(default=None, alias="case1")
    case2: ItemCase | None = Field(default=None, alias="case2")
    chest1: ItemChestOrPants | None = Field(default=None, alias="chest1")
    chest2: ItemChestOrPants | None = Field(default=None, alias="chest2")
    chest3: ItemChestOrPants | None = Field(default=None, alias="chest3")
    chest4: ItemChestOrPants | None = Field(default=None, alias="chest4")
    chest5: ItemChestOrPants | None = Field(default=None, alias="chest5")
    chest6: ItemChestOrPants | None = Field(default=None, alias="chest6")
    coca: ItemDepositResource | None = Field(default=None, alias="coca")
    cocain: ItemCocain | None = Field(default=None, alias="cocain")
    concrete: ItemConcrete | None = Field(default=None, alias="concrete")
    cooked_fish: ItemCookedFish | None = Field(default=None, alias="cookedFish")
    fish: ItemDepositResource | None = Field(default=None, alias="fish")
    gloves1: ItemGloves | None = Field(default=None, alias="gloves1")
    gloves2: ItemGloves | None = Field(default=None, alias="gloves2")
    gloves3: ItemGloves | None = Field(default=None, alias="gloves3")
    gloves4: ItemGloves | None = Field(default=None, alias="gloves4")
    gloves5: ItemGloves | None = Field(default=None, alias="gloves5")
    gloves6: ItemGloves | None = Field(default=None, alias="gloves6")
    grain: ItemDepositResource | None = Field(default=None, alias="grain")
    gun: ItemWeaponMeleeOrHeavy | None = Field(default=None, alias="gun")
    heavy_ammo: ItemHeavyAmmo | None = Field(default=None, alias="heavyAmmo")
    helmet1: ItemHelmet | None = Field(default=None, alias="helmet1")
    helmet2: ItemHelmet | None = Field(default=None, alias="helmet2")
    helmet3: ItemHelmet | None = Field(default=None, alias="helmet3")
    helmet4: ItemHelmet | None = Field(default=None, alias="helmet4")
    helmet5: ItemHelmet | None = Field(default=None, alias="helmet5")
    helmet6: ItemHelmet | None = Field(default=None, alias="helmet6")
    iron: ItemRawResource | None = Field(default=None, alias="iron")
    jet: ItemRifleLike | None = Field(default=None, alias="jet")
    knife: ItemWeaponMeleeOrHeavy | None = Field(default=None, alias="knife")
    lead: ItemRawResource | None = Field(default=None, alias="lead")
    light_ammo: ItemAmmo | None = Field(default=None, alias="lightAmmo")
    limestone: ItemRawResource | None = Field(default=None, alias="limestone")
    livestock: ItemDepositResource | None = Field(default=None, alias="livestock")
    oil: ItemOil | None = Field(default=None, alias="oil")
    paper: ItemPaper | None = Field(default=None, alias="paper")
    pants1: ItemChestOrPants | None = Field(default=None, alias="pants1")
    pants2: ItemChestOrPants | None = Field(default=None, alias="pants2")
    pants3: ItemChestOrPants | None = Field(default=None, alias="pants3")
    pants4: ItemChestOrPants | None = Field(default=None, alias="pants4")
    pants5: ItemChestOrPants | None = Field(default=None, alias="pants5")
    pants6: ItemChestOrPants | None = Field(default=None, alias="pants6")
    petroleum: ItemDepositResource | None = Field(default=None, alias="petroleum")
    rifle: ItemRifleLike | None = Field(default=None, alias="rifle")
    scraps: ItemScraps | None = Field(default=None, alias="scraps")
    sniper: ItemRifleLike | None = Field(default=None, alias="sniper")
    steak: ItemSteak | None = Field(default=None, alias="steak")
    steel: ItemSteel | None = Field(default=None, alias="steel")
    tank: ItemWeaponMeleeOrHeavy | None = Field(default=None, alias="tank")
    wood: ItemWood | None = Field(default=None, alias="wood")

class LawActionCostAndMaintenance(WareraModel):
    cost: float | None = Field(default=None, alias="cost")
    maintenance_cost: float | None = Field(default=None, alias="maintenanceCost")

class LawActionCost(WareraModel):
    cost: float | None = Field(default=None, alias="cost")

class LawSendMoneyToCountry(WareraModel):
    alliance_tax_rate: float | None = Field(default=None, alias="allianceTaxRate")
    external_tax_rate: float | None = Field(default=None, alias="externalTaxRate")

class GameConfigLaw(WareraModel):
    abusive_law_possible_voters_needed: float | None = Field(default=None, alias="abusiveLawPossibleVotersNeeded")
    abusive_laws_cooldown_in_days: int | None = Field(default=None, alias="abusiveLawsCooldownInDays")
    accept_alliance: LawActionCostAndMaintenance | None = Field(default=None, alias="accept_alliance")
    accept_join_alliance: LawActionCostAndMaintenance | None = Field(default=None, alias="accept_join_alliance")
    create_alliance: LawActionCostAndMaintenance | None = Field(default=None, alias="create_alliance")
    leave_alliance: LawActionCostAndMaintenance | None = Field(default=None, alias="leave_alliance")
    send_money_to_country: LawSendMoneyToCountry | None = Field(default=None, alias="sendMoneyToCountry")
    define_enemy_country: LawActionCostAndMaintenance | None = Field(default=None, alias="define_enemy_country")
    law_votes_duration_hours: int | None = Field(default=None, alias="lawVotesDurationHours")
    propose_alliance: LawActionCostAndMaintenance | None = Field(default=None, alias="propose_alliance")
    set_color_scheme: LawActionCost | None = Field(default=None, alias="set_color_scheme")
    voters_ratio_needed: float | None = Field(default=None, alias="votersRatioNeeded")

class MergingCostByRarity(WareraModel):
    common: float | None = Field(default=None, alias="common")
    epic: float | None = Field(default=None, alias="epic")
    legendary: float | None = Field(default=None, alias="legendary")
    mythic: float | None = Field(default=None, alias="mythic")
    rare: float | None = Field(default=None, alias="rare")
    uncommon: float | None = Field(default=None, alias="uncommon")

class MissionRerollCostByLevel(WareraModel):
    val_0: int | None = Field(default=None, alias="0")
    val_1: int | None = Field(default=None, alias="1")
    val_10: int | None = Field(default=None, alias="10")
    val_11: int | None = Field(default=None, alias="11")
    val_12: int | None = Field(default=None, alias="12")
    val_13: int | None = Field(default=None, alias="13")
    val_14: int | None = Field(default=None, alias="14")
    val_15: int | None = Field(default=None, alias="15")
    val_16: int | None = Field(default=None, alias="16")
    val_17: int | None = Field(default=None, alias="17")
    val_18: int | None = Field(default=None, alias="18")
    val_19: int | None = Field(default=None, alias="19")
    val_2: int | None = Field(default=None, alias="2")
    val_20: int | None = Field(default=None, alias="20")
    val_3: int | None = Field(default=None, alias="3")
    val_4: int | None = Field(default=None, alias="4")
    val_5: int | None = Field(default=None, alias="5")
    val_6: int | None = Field(default=None, alias="6")
    val_7: int | None = Field(default=None, alias="7")
    val_8: int | None = Field(default=None, alias="8")
    val_9: int | None = Field(default=None, alias="9")

class MissionRewardConfig(WareraModel):
    cases: float | None = Field(default=None, alias="cases")
    money: float | None = Field(default=None, alias="money")
    xp: float | None = Field(default=None, alias="xp")
    xp_when_finished: float | None = Field(default=None, alias="xpWhenFinished")

class MissionRewardByPeriod(WareraModel):
    daily: MissionRewardConfig | None = Field(default=None, alias="daily")
    monthly: MissionRewardConfig | None = Field(default=None, alias="monthly")
    starting: MissionRewardConfig | None = Field(default=None, alias="starting")
    weekly: MissionRewardConfig | None = Field(default=None, alias="weekly")

class GameConfigMission(WareraModel):
    reroll_mission_cost: MissionRerollCostByLevel | None = Field(default=None, alias="rerollMissionCost")
    reward: MissionRewardByPeriod | None = Field(default=None, alias="reward")

class GameConfigMu(WareraModel):
    construction_cost: float | None = Field(default=None, alias="constructionCost")
    destruction_value_percent: float | None = Field(default=None, alias="destructionValuePercent")
    health_per_help: float | None = Field(default=None, alias="healthPerHelp")
    help_cooldown_hours: int | None = Field(default=None, alias="helpCooldownHours")
    help_value: float | None = Field(default=None, alias="helpValue")
    max_owned_mus: int | None = Field(default=None, alias="maxOwnedMus")
    move_cost: float | None = Field(default=None, alias="moveCost")

class GameConfigNewspaper(WareraModel):
    comment_min_level: int | None = Field(default=None, alias="commentMinLevel")
    create_article_min_level: int | None = Field(default=None, alias="createArticleMinLevel")
    gem_tip_value: float | None = Field(default=None, alias="gemTipValue")
    publish_cost: float | None = Field(default=None, alias="publishCost")
    tip_min_level: int | None = Field(default=None, alias="tipMinLevel")
    tip_value: float | None = Field(default=None, alias="tipValue")

class GameConfigOrg(WareraModel):
    construction_cost: float | None = Field(default=None, alias="constructionCost")
    move_cost: float | None = Field(default=None, alias="moveCost")

class GameConfigParty(WareraModel):
    create_cost: float | None = Field(default=None, alias="createCost")

class GameConfigReferral(WareraModel):
    can_set_referrer_before_or_at_level: int | None = Field(default=None, alias="canSetReferrerBeforeOrAtLevel")
    level_needed_for_badge: int | None = Field(default=None, alias="levelNeededForBadge")
    life_time_badge_money_share_percent: float | None = Field(default=None, alias="lifeTimeBadgeMoneySharePercent")
    money_for_being_referred: float | None = Field(default=None, alias="moneyForBeingReferred")

class RegionResourceBonusByTier(WareraModel):
    val_1: float | None = Field(default=None, alias="1")
    val_2: float | None = Field(default=None, alias="2")
    val_3: float | None = Field(default=None, alias="3")

class GameConfigRegion(WareraModel):
    battle_cooldown_hours: int | None = Field(default=None, alias="battleCooldownHours")
    decrease_by: float | None = Field(default=None, alias="decreaseBy")
    decrease_resistance_cost: float | None = Field(default=None, alias="decreaseResistanceCost")
    deplete_hourly_percent: float | None = Field(default=None, alias="depleteHourlyPercent")
    increase_by: float | None = Field(default=None, alias="increaseBy")
    increase_resistance_cost: float | None = Field(default=None, alias="increaseResistanceCost")
    liberation_days_cooldown: int | None = Field(default=None, alias="liberationDaysCooldown")
    non_aggression_hours_after_liberation: int | None = Field(default=None, alias="nonAggressionHoursAfterLiberation")
    non_aggression_hours_after_peace: int | None = Field(default=None, alias="nonAggressionHoursAfterPeace")
    max_daily_resistance: int | None = Field(default=None, alias="maxDailyResistance")
    max_resistance: int | None = Field(default=None, alias="maxResistance")
    min_daily_resistance: int | None = Field(default=None, alias="minDailyResistance")
    region_not_linked_to_capital_malus_development_percent: float | None = Field(default=None, alias="regionNotLinkedToCapitalMalusDevelopmentPercent")
    resistance_ally_bonus_percent: float | None = Field(default=None, alias="resistanceAllyBonusPercent")
    resistance_bar_multiplier: float | None = Field(default=None, alias="resistanceBarMultiplier")
    resistance_battle_cooldown_hours: int | None = Field(default=None, alias="resistanceBattleCooldownHours")
    resistance_battle_start_cost_multiplier: float | None = Field(default=None, alias="resistanceBattleStartCostMultiplier")
    resistance_citizen_bonus: float | None = Field(default=None, alias="resistanceCitizenBonus")
    resistance_citizen_bonus_percent: float | None = Field(default=None, alias="resistanceCitizenBonusPercent")
    resistance_contribution_cooldown_after_revolt_hours: int | None = Field(default=None, alias="resistanceContributionCooldownAfterRevoltHours")
    resistance_contribution_cost: float | None = Field(default=None, alias="resistanceContributionCost")
    resistance_contribution_min_level: int | None = Field(default=None, alias="resistanceContributionMinLevel")
    resistance_contribution_value: float | None = Field(default=None, alias="resistanceContributionValue")
    resistance_decay_percent: float | None = Field(default=None, alias="resistanceDecayPercent")
    resistance_foreign_gov_cost_multiplier: float | None = Field(default=None, alias="resistanceForeignGovCostMultiplier")
    resistance_growth_percent_max: float | None = Field(default=None, alias="resistanceGrowthPercentMax")
    resistance_growth_percent_min: float | None = Field(default=None, alias="resistanceGrowthPercentMin")
    resistance_passive_growth_percent: float | None = Field(default=None, alias="resistancePassiveGrowthPercent")
    resources_bonus: RegionResourceBonusByTier | None = Field(default=None, alias="resourcesBonus")
    transfer_days_cooldown: int | None = Field(default=None, alias="transferDaysCooldown")

class SkillLevelZero(WareraModel):
    total_cost: float | None = Field(default=None, alias="totalCost")
    unlock_at_level: int | None = Field(default=None, alias="unlockAtLevel")
    value: float | None = Field(default=None, alias="value")

class SkillLevel(WareraModel):
    cost: float | None = Field(default=None, alias="cost")
    total_cost: float | None = Field(default=None, alias="totalCost")
    unlock_at_level: int | None = Field(default=None, alias="unlockAtLevel")
    value: float | None = Field(default=None, alias="value")

class SkillLevels(WareraModel):
    val_0: SkillLevelZero | None = Field(default=None, alias="0")
    val_1: SkillLevel | None = Field(default=None, alias="1")
    val_10: SkillLevel | None = Field(default=None, alias="10")
    val_2: SkillLevel | None = Field(default=None, alias="2")
    val_3: SkillLevel | None = Field(default=None, alias="3")
    val_4: SkillLevel | None = Field(default=None, alias="4")
    val_5: SkillLevel | None = Field(default=None, alias="5")
    val_6: SkillLevel | None = Field(default=None, alias="6")
    val_7: SkillLevel | None = Field(default=None, alias="7")
    val_8: SkillLevel | None = Field(default=None, alias="8")
    val_9: SkillLevel | None = Field(default=None, alias="9")

class SkillTrack(WareraModel):
    levels: SkillLevels | None = Field(default=None, alias="levels")
    soft_cap: float | None = Field(default=None, alias="softCap")
    skill_overflow: str | None = Field(default=None, alias="skillOverflow")
    skill_overflow_value: float | None = Field(default=None, alias="skillOverflowValue")

class BarSkillLevelZero(WareraModel):
    is_a_bar: bool | None = Field(default=None, alias="isABar")
    total_cost: float | None = Field(default=None, alias="totalCost")
    unlock_at_level: int | None = Field(default=None, alias="unlockAtLevel")
    value: float | None = Field(default=None, alias="value")

class BarSkillLevels(WareraModel):
    val_0: BarSkillLevelZero | None = Field(default=None, alias="0")
    val_1: SkillLevel | None = Field(default=None, alias="1")
    val_10: SkillLevel | None = Field(default=None, alias="10")
    val_2: SkillLevel | None = Field(default=None, alias="2")
    val_3: SkillLevel | None = Field(default=None, alias="3")
    val_4: SkillLevel | None = Field(default=None, alias="4")
    val_5: SkillLevel | None = Field(default=None, alias="5")
    val_6: SkillLevel | None = Field(default=None, alias="6")
    val_7: SkillLevel | None = Field(default=None, alias="7")
    val_8: SkillLevel | None = Field(default=None, alias="8")
    val_9: SkillLevel | None = Field(default=None, alias="9")

class BarSkillTrack(WareraModel):
    levels: BarSkillLevels | None = Field(default=None, alias="levels")

class GameConfigSkills(WareraModel):
    armor: SkillTrack | None = Field(default=None, alias="armor")
    attack: SkillTrack | None = Field(default=None, alias="attack")
    companies: SkillTrack | None = Field(default=None, alias="companies")
    critical_chance: SkillTrack | None = Field(default=None, alias="criticalChance")
    critical_damages: SkillTrack | None = Field(default=None, alias="criticalDamages")
    dodge: SkillTrack | None = Field(default=None, alias="dodge")
    energy: BarSkillTrack | None = Field(default=None, alias="energy")
    entrepreneurship: BarSkillTrack | None = Field(default=None, alias="entrepreneurship")
    health: BarSkillTrack | None = Field(default=None, alias="health")
    hunger: BarSkillTrack | None = Field(default=None, alias="hunger")
    loot_chance: SkillTrack | None = Field(default=None, alias="lootChance")
    management: SkillTrack | None = Field(default=None, alias="management")
    precision: SkillTrack | None = Field(default=None, alias="precision")
    production: BarSkillTrack | None = Field(default=None, alias="production")

class GameConfigUnrest(WareraModel):
    bar_multiplier: float | None = Field(default=None, alias="barMultiplier")
    battle_cooldown_hours: int | None = Field(default=None, alias="battleCooldownHours")
    battle_start_cost: float | None = Field(default=None, alias="battleStartCost")
    borders_open_days: int | None = Field(default=None, alias="bordersOpenDays")
    contribution_cooldown_after_revolution_hours: int | None = Field(default=None, alias="contributionCooldownAfterRevolutionHours")
    contribution_cost: float | None = Field(default=None, alias="contributionCost")
    contribution_min_level: int | None = Field(default=None, alias="contributionMinLevel")
    contribution_value: float | None = Field(default=None, alias="contributionValue")
    nomination_period_hours: int | None = Field(default=None, alias="nominationPeriodHours")

class GameConfigUpgrade(WareraModel):
    refund_percent: float | None = Field(default=None, alias="refundPercent")
    region_downgrade_cooldown_hours: int | None = Field(default=None, alias="regionDowngradeCooldownHours")
    region_upgrade_cooldown_hours: int | None = Field(default=None, alias="regionUpgradeCooldownHours")

class UpgradeConfigStorageStats(WareraModel):
    daily_prod: int | None = Field(default=None, alias="dailyProd")

class UpgradeConfigStorageLevel(WareraModel):
    construction_points_cost: int | None = Field(default=None, alias="constructionPointsCost")
    level: int | None = Field(default=None, alias="level")
    stats: UpgradeConfigStorageStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigStorageLevels(WareraModel):
    val_1: UpgradeConfigStorageLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigStorageLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigStorageLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigStorageLevel | None = Field(default=None, alias="4")
    val_5: UpgradeConfigStorageLevel | None = Field(default=None, alias="5")
    val_6: UpgradeConfigStorageLevel | None = Field(default=None, alias="6")
    val_7: UpgradeConfigStorageLevel | None = Field(default=None, alias="7")

class UpgradeConfigAutomatedEngine(WareraModel):
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigStorageLevels | None = Field(default=None, alias="levels")
    pending_duration_hours: int | None = Field(default=None, alias="pendingDurationHours")

class UpgradeConfigAttackBonusStats(WareraModel):
    attack_bonus: float | None = Field(default=None, alias="attackBonus")

class UpgradeConfigBaseLevel(WareraModel):
    construction_points_cost: int | None = Field(default=None, alias="constructionPointsCost")
    level: int | None = Field(default=None, alias="level")
    maintenance_cost_country_dev_scale: float | None = Field(default=None, alias="maintenanceCostCountryDevScale")
    minimum_maintenance_cost: float | None = Field(default=None, alias="minimumMaintenanceCost")
    stats: UpgradeConfigAttackBonusStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigBaseLevels(WareraModel):
    val_1: UpgradeConfigBaseLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigBaseLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigBaseLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigBaseLevel | None = Field(default=None, alias="4")
    val_5: UpgradeConfigBaseLevel | None = Field(default=None, alias="5")

class UpgradeConfigBase(WareraModel):
    can_be_destroyed: bool | None = Field(default=None, alias="canBeDestroyed")
    can_be_disabled: bool | None = Field(default=None, alias="canBeDisabled")
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigBaseLevels | None = Field(default=None, alias="levels")
    pending_duration_hours: int | None = Field(default=None, alias="pendingDurationHours")

class UpgradeConfigBreakRoomStats(WareraModel):
    daily_hires: int | None = Field(default=None, alias="dailyHires")
    max_workers: int | None = Field(default=None, alias="maxWorkers")

class UpgradeConfigBreakRoomLevel(WareraModel):
    level: int | None = Field(default=None, alias="level")
    stats: UpgradeConfigBreakRoomStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigBreakRoomLevels(WareraModel):
    val_1: UpgradeConfigBreakRoomLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigBreakRoomLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigBreakRoomLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigBreakRoomLevel | None = Field(default=None, alias="4")
    val_5: UpgradeConfigBreakRoomLevel | None = Field(default=None, alias="5")

class UpgradeConfigBreakRoom(WareraModel):
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigBreakRoomLevels | None = Field(default=None, alias="levels")

class UpgradeConfigDefenseBonusStats(WareraModel):
    defense_bonus: float | None = Field(default=None, alias="defenseBonus")

class UpgradeConfigBunkerLevel(WareraModel):
    construction_points_cost: int | None = Field(default=None, alias="constructionPointsCost")
    level: int | None = Field(default=None, alias="level")
    maintenance_cost_country_dev_scale: float | None = Field(default=None, alias="maintenanceCostCountryDevScale")
    minimum_maintenance_cost: float | None = Field(default=None, alias="minimumMaintenanceCost")
    stats: UpgradeConfigDefenseBonusStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigBunkerLevels(WareraModel):
    val_1: UpgradeConfigBunkerLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigBunkerLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigBunkerLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigBunkerLevel | None = Field(default=None, alias="4")
    val_5: UpgradeConfigBunkerLevel | None = Field(default=None, alias="5")

class UpgradeConfigBunker(WareraModel):
    can_be_destroyed: bool | None = Field(default=None, alias="canBeDestroyed")
    can_be_disabled: bool | None = Field(default=None, alias="canBeDisabled")
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigBunkerLevels | None = Field(default=None, alias="levels")
    pending_duration_hours: int | None = Field(default=None, alias="pendingDurationHours")

class UpgradeConfigDormitoriesStats(WareraModel):
    members: int | None = Field(default=None, alias="members")

class UpgradeConfigDormitoriesLevel(WareraModel):
    level: int | None = Field(default=None, alias="level")
    stats: UpgradeConfigDormitoriesStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigDormitoriesLevels(WareraModel):
    val_1: UpgradeConfigDormitoriesLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigDormitoriesLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigDormitoriesLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigDormitoriesLevel | None = Field(default=None, alias="4")
    val_5: UpgradeConfigDormitoriesLevel | None = Field(default=None, alias="5")

class UpgradeConfigDormitories(WareraModel):
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigDormitoriesLevels | None = Field(default=None, alias="levels")

class UpgradeConfigHeadquartersLevel(WareraModel):
    level: int | None = Field(default=None, alias="level")
    maintenance_cost: float | None = Field(default=None, alias="maintenanceCost")
    stats: UpgradeConfigAttackBonusStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigHeadquartersLevels(WareraModel):
    val_1: UpgradeConfigHeadquartersLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigHeadquartersLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigHeadquartersLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigHeadquartersLevel | None = Field(default=None, alias="4")

class UpgradeConfigHeadquarters(WareraModel):
    can_be_disabled: bool | None = Field(default=None, alias="canBeDisabled")
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigHeadquartersLevels | None = Field(default=None, alias="levels")
    pending_duration_hours: int | None = Field(default=None, alias="pendingDurationHours")

class UpgradeConfigPacificationCenterStats(WareraModel):
    resistance_growth_reduction: float | None = Field(default=None, alias="resistanceGrowthReduction")

class UpgradeConfigPacificationCenterLevel(WareraModel):
    construction_points_cost: int | None = Field(default=None, alias="constructionPointsCost")
    level: int | None = Field(default=None, alias="level")
    maintenance_cost_region_dev_scale: float | None = Field(default=None, alias="maintenanceCostRegionDevScale")
    minimum_maintenance_cost: float | None = Field(default=None, alias="minimumMaintenanceCost")
    stats: UpgradeConfigPacificationCenterStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigPacificationCenterLevels(WareraModel):
    val_1: UpgradeConfigPacificationCenterLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigPacificationCenterLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigPacificationCenterLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigPacificationCenterLevel | None = Field(default=None, alias="4")
    val_5: UpgradeConfigPacificationCenterLevel | None = Field(default=None, alias="5")

class UpgradeConfigPacificationCenter(WareraModel):
    can_be_destroyed: bool | None = Field(default=None, alias="canBeDestroyed")
    can_be_disabled: bool | None = Field(default=None, alias="canBeDisabled")
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigPacificationCenterLevels | None = Field(default=None, alias="levels")
    pending_duration_hours: int | None = Field(default=None, alias="pendingDurationHours")

class UpgradeConfigStorageCapacityStats(WareraModel):
    max_production: int | None = Field(default=None, alias="maxProduction")

class UpgradeConfigStorageCapacityLevel(WareraModel):
    construction_points_cost: int | None = Field(default=None, alias="constructionPointsCost")
    level: int | None = Field(default=None, alias="level")
    stats: UpgradeConfigStorageCapacityStats | None = Field(default=None, alias="stats")
    steel_cost: float | None = Field(default=None, alias="steelCost")

class UpgradeConfigStorageCapacityLevels(WareraModel):
    val_1: UpgradeConfigStorageCapacityLevel | None = Field(default=None, alias="1")
    val_2: UpgradeConfigStorageCapacityLevel | None = Field(default=None, alias="2")
    val_3: UpgradeConfigStorageCapacityLevel | None = Field(default=None, alias="3")
    val_4: UpgradeConfigStorageCapacityLevel | None = Field(default=None, alias="4")
    val_5: UpgradeConfigStorageCapacityLevel | None = Field(default=None, alias="5")
    val_6: UpgradeConfigStorageCapacityLevel | None = Field(default=None, alias="6")
    val_7: UpgradeConfigStorageCapacityLevel | None = Field(default=None, alias="7")

class UpgradeConfigStorage(WareraModel):
    can_downgrade: bool | None = Field(default=None, alias="canDowngrade")
    levels: UpgradeConfigStorageCapacityLevels | None = Field(default=None, alias="levels")
    pending_duration_hours: int | None = Field(default=None, alias="pendingDurationHours")

class GameConfigUpgradesConfig(WareraModel):
    automated_engine: UpgradeConfigAutomatedEngine | None = Field(default=None, alias="automatedEngine")
    base: UpgradeConfigBase | None = Field(default=None, alias="base")
    break_room: UpgradeConfigBreakRoom | None = Field(default=None, alias="breakRoom")
    bunker: UpgradeConfigBunker | None = Field(default=None, alias="bunker")
    dormitories: UpgradeConfigDormitories | None = Field(default=None, alias="dormitories")
    headquarters: UpgradeConfigHeadquarters | None = Field(default=None, alias="headquarters")
    pacification_center: UpgradeConfigPacificationCenter | None = Field(default=None, alias="pacificationCenter")
    storage: UpgradeConfigStorage | None = Field(default=None, alias="storage")

class UserDailyReward(WareraModel):
    case1: float | None = Field(default=None, alias="case1")
    money: float | None = Field(default=None, alias="money")
    xp: float | None = Field(default=None, alias="xp")

class UserEquipmentSets(WareraModel):
    non_premium_max: int | None = Field(default=None, alias="nonPremiumMax")
    premium_max: int | None = Field(default=None, alias="premiumMax")

class GameConfigUser(WareraModel):
    active_citizen_min_level: int | None = Field(default=None, alias="activeCitizenMinLevel")
    can_take_control_at_level: int | None = Field(default=None, alias="canTakeControlAtLevel")
    chat_min_level: int | None = Field(default=None, alias="chatMinLevel")
    citizenship_days_cooldown: int | None = Field(default=None, alias="citizenshipDaysCooldown")
    construction_energy_cost: float | None = Field(default=None, alias="constructionEnergyCost")
    daily_reward: UserDailyReward | None = Field(default=None, alias="dailyReward")
    daily_xp: float | None = Field(default=None, alias="dailyXp")
    donation_min_level: int | None = Field(default=None, alias="donationMinLevel")
    energy_cost_per_action: float | None = Field(default=None, alias="energyCostPerAction")
    equipment_sets: UserEquipmentSets | None = Field(default=None, alias="equipmentSets")
    fields_to_populate: str | None = Field(default=None, alias="fieldsToPopulate")
    is_inactive_after_days: int | None = Field(default=None, alias="isInactiveAfterDays")
    kits: UserEquipmentSets | None = Field(default=None, alias="kits")
    market_min_level: int | None = Field(default=None, alias="marketMinLevel")
    max_construction_points: int | None = Field(default=None, alias="maxConstructionPoints")
    max_energy: int | None = Field(default=None, alias="maxEnergy")
    max_hunger: int | None = Field(default=None, alias="maxHunger")
    regen_divided_by: float | None = Field(default=None, alias="regenDividedBy")
    reset_skill_days_cooldown: int | None = Field(default=None, alias="resetSkillDaysCooldown")
    reset_skills_cost_per_point: float | None = Field(default=None, alias="resetSkillsCostPerPoint")
    take_control_cooldown_in_days: int | None = Field(default=None, alias="takeControlCooldownInDays")
    xp_per_action: float | None = Field(default=None, alias="xpPerAction")

class GameConfigWorker(WareraModel):
    fidelity_production_bonus_percent: float | None = Field(default=None, alias="fidelityProductionBonusPercent")
    max_fidelity: int | None = Field(default=None, alias="maxFidelity")

class GameConfigAlliance(WareraModel):
    leave_cooldown_days: int | None = Field(default=None, alias="leaveCooldownDays")

class GameConfigLoot(WareraModel):
    weapon_chance_percent: float | None = Field(default=None, alias="weaponChancePercent")
    damage_per_loot_item: float | None = Field(default=None, alias="damagePerLootItem")
    battle_loot_damage_per_loot_item: float | None = Field(default=None, alias="battleLootDamagePerLootItem")

class MercenaryAuctionConfig(WareraModel):
    min_duration: float | None = Field(default=None, alias="minDuration")
    max_duration: float | None = Field(default=None, alias="maxDuration")
    max_per_k_multiplier: float | None = Field(default=None, alias="maxPerKMultiplier")
    min_per_k: float | None = Field(default=None, alias="minPerK")
    bid_step: float | None = Field(default=None, alias="bidStep")
    timer_extension_threshold: float | None = Field(default=None, alias="timerExtensionThreshold")
    timer_extension_amount: float | None = Field(default=None, alias="timerExtensionAmount")
    max_damage_per_contract: float | None = Field(default=None, alias="maxDamagePerContract")

class MercenaryReputationConfig(WareraModel):
    professionals_only_threshold: float | None = Field(default=None, alias="professionalsOnlyThreshold")
    success_per_dollar: float | None = Field(default=None, alias="successPerDollar")
    failure_per_dollar: float | None = Field(default=None, alias="failurePerDollar")
    failure_per_damage: float | None = Field(default=None, alias="failurePerDamage")
    weekly_decay_percent: float | None = Field(default=None, alias="weeklyDecayPercent")
    negative_buy_cost: float | None = Field(default=None, alias="negativeBuyCost")
    negative_buy_amount: float | None = Field(default=None, alias="negativeBuyAmount")
    negative_buy_cooldown_hours: float | None = Field(default=None, alias="negativeBuyCooldownHours")

class GameConfigMercenaryContract(WareraModel):
    enabled: bool | None = Field(default=None, alias="enabled")
    acceptance_fee_percent: float | None = Field(default=None, alias="acceptanceFeePercent")
    cancellation_penalty_percent: float | None = Field(default=None, alias="cancellationPenaltyPercent")
    reputation: MercenaryReputationConfig | None = Field(default=None, alias="reputation")
    bounty_min_active_citizens: int | None = Field(default=None, alias="bountyMinActiveCitizens")
    national_bounty_min_active_citizens: int | None = Field(default=None, alias="nationalBountyMinActiveCitizens")
    national_bounty_enabled: bool | None = Field(default=None, alias="nationalBountyEnabled")
    bounty_cooldown_minutes: float | None = Field(default=None, alias="bountyCooldownMinutes")
    max_bounty_wage_multiplier: float | None = Field(default=None, alias="maxBountyWageMultiplier")
    auction: MercenaryAuctionConfig | None = Field(default=None, alias="auction")

class GameConfigSubSkinReward(WareraModel):
    skin_key: str | None = Field(default=None, alias="skinKey")
    deadline: str | None = Field(default=None, alias="deadline")

class GameConfig(WareraModel):
    alliance: GameConfigAlliance | None = Field(default=None, alias="alliance")
    badge: GameConfigBadges | None = Field(default=None, alias="badge")
    battle: GameConfigBattle | None = Field(default=None, alias="battle")
    citizenship_application: GameConfigCitizenshipApplication | None = Field(default=None, alias="citizenshipApplication")
    company: GameConfigCompany | None = Field(default=None, alias="company")
    country: GameConfigCountry | None = Field(default=None, alias="country")
    election: GameConfigElection | None = Field(default=None, alias="election")
    government: GameConfigGovernment | None = Field(default=None, alias="government")
    items: GameConfigItems | None = Field(default=None, alias="items")
    law: GameConfigLaw | None = Field(default=None, alias="law")
    loot: GameConfigLoot | None = Field(default=None, alias="loot")
    mercenary_contract: GameConfigMercenaryContract | None = Field(default=None, alias="mercenaryContract")
    merging_cost: MergingCostByRarity | None = Field(default=None, alias="mergingCost")
    mission: GameConfigMission | None = Field(default=None, alias="mission")
    mu: GameConfigMu | None = Field(default=None, alias="mu")
    newspaper: GameConfigNewspaper | None = Field(default=None, alias="newspaper")
    org: GameConfigOrg | None = Field(default=None, alias="org")
    party: GameConfigParty | None = Field(default=None, alias="party")
    referral: GameConfigReferral | None = Field(default=None, alias="referral")
    region: GameConfigRegion | None = Field(default=None, alias="region")
    skills: GameConfigSkills | None = Field(default=None, alias="skills")
    sub_skin_reward: GameConfigSubSkinReward | None = Field(default=None, alias="subSkinReward")
    unrest: GameConfigUnrest | None = Field(default=None, alias="unrest")
    upgrade: GameConfigUpgrade | None = Field(default=None, alias="upgrade")
    upgrades_config: GameConfigUpgradesConfig | None = Field(default=None, alias="upgradesConfig")
    user: GameConfigUser | None = Field(default=None, alias="user")
    worker: GameConfigWorker | None = Field(default=None, alias="worker")


class GameDates(WareraModel):
    next_day_at: str | None = Field(default=None, alias="nextDayAt")
    next_regen_at: str | None = Field(default=None, alias="nextRegenAt")
    previous_day_at: str | None = Field(default=None, alias="previousDayAt")
    next_congress_elections_at: str | None = Field(default=None, alias="nextCongressElectionsAt")
    next_presidential_elections_at: str | None = Field(default=None, alias="nextPresidentialElectionsAt")
    next_month_at: str | None = Field(default=None, alias="nextMonthAt")
    daily_mission_regen_at: str | None = Field(default=None, alias="dailyMissionRegenAt")
    weekly_mission_regen_at: str | None = Field(default=None, alias="weeklyMissionRegenAt")
    game_day: int | None = Field(default=None, alias="gameDay")
    game_month: int | None = Field(default=None, alias="gameMonth")
    game_year: int | None = Field(default=None, alias="gameYear")
    real_date: str | None = Field(default=None, alias="realDate")
    day_duration_seconds: int | None = Field(default=None, alias="dayDurationSeconds")

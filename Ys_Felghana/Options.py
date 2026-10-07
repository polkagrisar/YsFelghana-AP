from dataclasses import dataclass
from Options import Toggle, Choice, Range, PerGameCommonOptions


class ExtraProgressive(Range):
    """
    Add more copies of Proggressive Equipment (Swords, Shields, Armors)
    Does NOT add extra bracelets if using with Progressive Bracelets
    """
    display_name = "More Progressive Equipment"
    range_start = 0
    range_end = 3
    default = 0

class KeyringItem(Choice):
    """
    Add a Keyring Item that give you the "Storehouse Key", "Ruins Key" and "Clock Tower Key" when you find it.
    dont_add = Don't add the Keyring Item and keep the 3 different keys as their separate items. (Vanilla)
    add_replace = Add 3 Keyring Items to the pool, removing the original Keys from the pool. (0 Different Keys, 3 Keyring Items that give all Keys)
    add_keep = Add 1 Keyring Item to the pool, but the 3 different Keys are kept in the pool. (3 different Keys, 1 Keyring Item that give all Keys)
    add_remove = Add 1 Keyring Item to the pool, removing the original Keys from the pool. (0 Different Keys, 1 Keyring Item that give all Keys)
    """
    display_name = "Keyring Item"
    option_dont_add = 0
    option_add_replace = 1
    option_add_keep = 2
    option_add_remove = 3
    default = 0
    

class ProgressiveBracelets(Toggle):
    """
    Combine the gemstones into extra bracelets, the first one you find will always give the bracelet, the rest will become gemstones.
    This will make it so there are 4 of each bracelet in the pool, instead of the usual 1.
    """
    display_name = "Progressive Bracelets"
    default = False

### Logic
class StatuePlacement(Choice):
    """
    How should the four Statues be placed?
    Randomized = They can be anywhere in the world
    Vanilla = They will be in their original locations (Beating the boss protecting them)
    """
    display_name = "Statue Placement"
    option_randomized = 0
    option_vanilla = 1
    default = 0

class StatuesRequired(Range):
    """
    How many Statues are required to enter Valestein Castle.
    """
    display_name = "Statues needed to enter Valestein Castle"
    range_start = 0
    range_end = 4
    default = 4

class BossesRequired(Range):
    """
    How many Bosses must be defeated to enter Genos Island.
    """
    display_name = "Bosses Required for Genos"
    range_start = 0
    range_end = 12
    default = 12

class OpenDungeon(Choice):
    """
    Should the Dungeon in Valestein Castle always be open, or require placing the three Organ Parts (Vanilla, closed).
    Either way, the organ parts can still be placed for their locations.
    Note: You still need to be able to enter Valestein Castle before you can reach the Dungeon.
    """
    display_name = "Open Valestein Dungeon"
    option_open = 0
    option_closed = 1
    default = 1

### Quality of Life ###
class AutoItem(Choice):
    """
    If true:
    When you have them, the "Nightfire Gem" will automatically be equipped in the Abandoned Mine,
    the "Firewyrm's Amulet" will automatically be equipped in the Lava Zone,
    and the "Stone Shoes" will automatically be equipped in the Icebound Cave.

    Note: They will not be equipped automatically if you have the "Spirit Cape" or the "Spirit Necklace" equipped
    """
    display_name = "Auto-equip Items"
    option_true = 0
    option_false = 1
    default = 0

class BrociaSerumChange(Choice):
    """
    vanilla = Brocia Serum is randomized into the pool and gives the Dash ability on use.
    Other choices = Dash is randomized into the pool as its own item, Brocia Serum does not give Dash, instead its use changes depending on the option chosen.

    boss_level = Brocia Serum can be used any number of times, if used in the save-room before a boss, your level will be set to the recomended level for that boss.
    boss_level_x = Brocia Serum can be used any number of times, if used in the save-room before a boss, your level will be set to the recomended level for that boss + X.
    xpflask = Brocia Serum can be used any number of times, everytime it is used you will gain 10000 XP.
    """
    display_name = "How should Brocia Serum work"
    option_vanilla = 0
    option_boss_level = 1
    option_boss_level_1 = 2
    option_boss_level_2 = 3
    option_boss_level_3 = 4
    option_boss_level_4 = 5
    option_xpflask = 6
    default = 0

class BrociaSerumStart(Toggle):
    """
    True: Start with the Brocia Serum.
    False: The Brocia Serum is randomized into the Item Pool.
    """
    display_name = "Start with Brocia Serum"
    default  = False

class UseSwordAnywhere(Choice):
    """
    Let's you use the sword anywhere (and also doublejump if you have it)
    Has no actual impact on gameplay or logic
    """
    display_name = "Use the sword anywhere"
    option_true = 0
    option_false = 1
    default = 1

@dataclass
class YsFelghanaOptions(PerGameCommonOptions):
    extra_progressive: ExtraProgressive
    progressive_bracelets: ProgressiveBracelets
    statue_placement: StatuePlacement
    statues_required: StatuesRequired
    bosses_required: BossesRequired
    open_dungeon: OpenDungeon
    auto_item: AutoItem
    keyring_item: KeyringItem
    brocia_serum_change: BrociaSerumChange
    brocia_start: BrociaSerumStart
    sword_anywhere: UseSwordAnywhere
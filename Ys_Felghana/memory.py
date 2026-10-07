from pymem import Pymem
from typing import Set
from .items_data import ITEMS
import threading
import time
import re



SWORD_PROGRESSION = [
    "Short Sword",       # index 0
    "Long Sword",        # Progressive Sword #1
    "Broad Sword",     # Progressive Sword #2
    "Banded Slayer",       # Progressive Sword #3
    "Battle Saber",      # Progressive Sword #4
    "Brave Sword",       # Progressive Sword #5
]

SHIELD_PROGRESSION = [
    "Wooden Shield",
    "Small Shield",
    "Large Shield",
    "Banded Shield",
    "Battle Shield",
    "Raval Shield",
]

ARMOR_PROGRESSION = [
    "Leather Armor",
    "Chain Mail",
    "Plate Mail",
    "Banded Mail",
    "Battle Armor",
    "Raval Armor",
]

SHOP_EQUIPMENT = [
    "Long Sword", "Banded Slayer",
    "Large Shield", "Banded Shield",
    "Chain Mail", "Plate Mail", "Banded Mail",
    "Amulet", "Illusion Mirror", "Katol Elixir",
    "Spirit Necklace",
]

SHOP_ITEMS = {
    "Long Sword":       "Redmont - Buy Long Sword",
    "Banded Slayer":    "Redmont - Buy Banded Slayer",
    "Large Shield":     "Redmont - Buy Large Shield",
    "Banded Shield":    "Redmont - Buy Banded Shield",
    "Chain Mail":       "Redmont - Buy Chain Mail",
    "Plate Mail":       "Redmont - Buy Plate Mail",
    "Banded Mail":      "Redmont - Buy Banded Mail",
    "Illusion Mirror":  "Redmont - Buy Illusion Mirror",
    "Amulet":           "Redmont - Buy Amulet",
    "Katol Elixir":     "Redmont - Buy Katol Elixir",
    "Spirit Necklace":  "Redmont - Buy Spirit Necklace",
}

REDMONT = {20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 34, 36, 43}
CASTLE_ENTRY = {40, 46, 160}   # outside / entrance only if needed
CAVE_GAP = {147, 148, 151, 157, 158}
GENOS_UNLOCK = {41, 46, 206}

ROOMS = {

    36: "Overworld - Outside Redmont", #Set all the Redmont flags needed when here (So that the town is in the correct state when entering), also set it in any rooms leading to the street
    37: "Overworld - Outside Quarry",
    38: "Overworld - Outside Illburn",
    39: "Overworld - Outside Mountain",
    40: "Overworld - Outside Castle",           #Set castle flag here and 46
    41: "Overworld - At the Docks",             #Set genos flag here and 46
    46: "Overworld - Between Castle and Docks", #Set castle and genos flag here

    #Set "Falon Beaten" to 1 here to open Upper Castle Door
    # 40, outside the castle
    160: "Castle - Entrance Room",
    161: "Castle - West Room 1",
    175: "Castle - West Room 1",
    189: "Castle - Organ Room",
    202: "Castle - Outside Organ Room",
    168: "Castle - West Before Organ",
    182: "Castle - East Before Organ",


    #Set "Falon Beaten" to 0 here to not accidently send the location
    #171
    174: "Castle - Faleon Bossroom", #only send location here

    #Redmont
    20: "Redmont - Inn",                            #Set all the Redmont flags when needed here
    21: "Redmont - Inn, Right Room",
    22: "Redmont - Inn, Left Room",
    24: "Redmont - Weapon Shop",                    #Set all the Redmont flags when needed here
    25: "Redmont - Mayor's House, Mayor's Room",
    26: "Redmont - Mayor's House Right",
    27: "Redmont - Mayor's House",                  #Set all the Redmont flags when needed here
    28: "Redmont - Bob's House",                    #Set all the Redmont flags when needed here
    29: "Redmont - Elenas House",                   #Set all the Redmont flags when needed here
    30: "Redmont - Church",                         #Set all the Redmont flags when needed here
    31: "Redmont - Extra House",                    #Set all the Redmont flags when needed here
    34: "Redmont - Street",                         #Set all the Redmont flags when needed here

    #Rooms before bosses (Used to see what level boss_xp brocia should make you)
    # "Quarry - Fight Dularn" = 55: "Quarry - Storehouse Save", #Lvl 6
    65: "Quarry - Fight Ellefale",  #Lvl 7
    108: "Illburn - Fight Chester", #Lvl 13
    115: "Lava - Fight Guilen", #Lvl 16
    123: "Lava - Fight Gyalva", #Lvl 18
    81: "Mine - Fight Istersiva",   #Lvl 23
    136: "Mountain - Fight Ligaty", #26
    157: "Cave - Fight Gildias", #31
    171: "Castle - Fight Faleon",  #33
    185: "Castle - Fight Zellfel",  #36  
    193: "Castle - Fight Zirduros", #39       
    204: "Castle - Fight Chester",  #42
    209: "Genos - Fight Dularn", #44
    224: "Genos - Fight Garland and Galbalan", #50   


    #Tigris Quarry (To force open door if you have Nightfire Gem)
    55: "Quarry - Storehouse Save",
    57: "Quarry - Abandonded Mines Door",

    #Open the gap where Dogi gives Terra
    147: "Cave - Room before Gaproom",
    148: "Cave - Gaproom",
    #also 151, 157, 158

    #Lava Zone - Lava Rooms (To force Firewyrm's Necklace)
    184: "Castle - Lavaroom",
    112: "Lava - Lavafloor Start",
    113: "Lava - Road to Sword Chest",
    128: "Lava - Guilen Bossroom",
    116: "Lava - Ventus room",

    #Abandoned Mines - Dark Room (To force Nightfire Gem)
    183: "Castle - Darkroom",
    70: "Mine - First Room",
    71: "Mine - Second Room",
    72: "Mine - First Mineshaft",
    74: "Mine - Right Room Mineshaft",
    75: "Mine - Room after First Mineshaft",
    76: "Mine - Room with Pond",
    77: "Mine - Jump to Emerald Chest",
    78: "Mine - Room Before Gap",
    79: "Mine - Gap Room",
    80: "Mine - Final Room",
    
    #Elderm Mountain - Ice Rooms (To force Stone Shoes)
    163: "Castle - Ice Bridge",
    177: "Castle - Ice Room",
    #Add the room before the Castle Ice Bridge and Ice Room
    83: "Mine - Istersiva Room",
    145: "Mountain - Iceroom",
    149: "Cave - Iceroom drop",
    151: "Cave - Ice Parkour",
    152: "Cave - Iceroom under Parkour",
    153: "Cave - Stoneshoes Room",
    154: "Cave - Iceslide Room",
    155: "Cave - Steep Icesloop",
    158: "Cave - Gildias Bossroom",


 }





class YsMemory:
    def __init__(self, bosses_required: int = 2, statues_required: int = 2, open_dungeon: int = 1, brocia_serum_change: int = 0, sword_anywhere: int = 1):
        self.pm = Pymem("ysf_win_dx9.exe")
        self.base = self.pm.base_address
        self.module_base = self.base  # Fix: Set module_base to base address
        print(f"Attached to Ys! Base: {hex(self.base)}")

        self.xp_address = self.base + 0x1C4398

        self.progressive_sword_count = 0
        self.progressive_shield_count = 0
        self.progressive_armor_count = 0

        self.progressive_ignis_count = 0
        self.progressive_ventus_count = 0
        self.progressive_terra_count = 0

        self.ruby_debt = 0
        self.emerald_debt = 0
        self.topaz_debt = 0
        self.raval_debt = 0
        self.berm_debt = 0

        self.shop_bought = set()

        self.actual_katol = 0
        self.actual_mirror = 0
        self.actual_amulet = 0

        self.bosses_required = bosses_required
        self.statues_required = statues_required
        self.open_dungeon = open_dungeon
        self.brocia_serum_change = brocia_serum_change
        self.sword_anywhere = sword_anywhere

        self.menu_open_address = 0x00594768
        self.menu_open = 0

        ON_ICE_ADDR = 0x0043057A
        self.value_ice_addr = ON_ICE_ADDR + 6

        #Traps
        self.active_traps = {}
        self.armless = False

        #List of items you have recieved
        self.authorized_items = set()

        allowed_items = {
            "Short Sword",
            "Wooden Shield",
            "Leather Armor",
            "Map of Felghana",
            "Bob's Pendant",
            "Wing Talisman",
            "Ruby",
            "Emerald",
            "Topaz",
            "Katol Elixir",
            "Berm Leaves",
            "Amulet",
            "Illusion Mirror",
            "Armless Trap",
        }

        self.authorized_items.update(allowed_items)
        

        self.location_flags = {
            
            "Redmont - Return Bob's Pendant":   0xBC,         #Is completed at flag 0
            "Redmont - Give Hugo a Berm Leaves": 0xF8,        #Is completed at flag 0
            #"Redmont - Give Randolph the Jade Ring": 0x100,   #Is completed at flag 0, only in Inn
            #"Redmont - Sell the Jade Ring to Cynthia":   0X100,         #Is completed at flag 0, only in Store
            #"Redmont - Give Adonis the Lotus Hammer": 0x10C, #Is completed at flag 0, only in Store

            #Only trigger when in the store
            "Redmont - Buy Long Sword":       0x4,         #Same flags as the items #800 Gold
            "Redmont - Buy Banded Slayer":      0xC,       #Same flags as the items #24000 Gold
            "Redmont - Buy Large Shield":        0x20,     #Same flags as the items #2800 Gold
            "Redmont - Buy Banded Shield":      0x24,      #Same flags as the items #16000 Gold
            "Redmont - Buy Chain Mail":         0x34,      #Same flags as the items #650 Gold
            "Redmont - Buy Plate Mail":         0x38,      #Same flags as the items #3500 Gold
            "Redmont - Buy Banded Mail":          0x3C,    #Same flags as the items #18000 Gold
            "Redmont - Buy Illusion Mirror":   0xF0,       #Same flags as the items #50 Gold
            "Redmont - Buy Amulet":            0xF4,       #Same flags as the items #50 Gold
            "Redmont - Buy Katol Elixir":      0xFC,       #Same flags as the items #10000 Gold
            "Redmont - Buy Spirit Necklace":   0x5C,       #Same flags as the items #60000 Gold

            "Overworld - Pot by the Dock":      0x584,        
            "Quarry - Raval Ore x5 Chest":      0x490,
            "Quarry - Raval Ore x8 Chest":      0x498,
            #"Quarry - Open Storehouse Door":    0x2E0,
            "Quarry - Defeat Dularn":           0x2E4,
            "Quarry - Ignis Bracelet Chest":    0x48C,
            "Quarry - Defeat Ellefale":         0x2EC,
            "Quarry - Torch Ruby Chest":        0x49C,
            "Quarry - Pot Above Stairs":        0x594,
            "Quarry - Pot Under Stairs":        0x598,
            "Quarry - Pot Room After Dewey":    0x59C,
            "Quarry - Pot Outside Ellefale":    0x5A0,
            "Quarry - Bob's Pendant":           0xBC,
            "Quarry - Pot Bob's Pendant":       0x590,
            "Quarry - Pot Outside Mine":        0x58C,
            "Quarry - Pot Main Room Double Jump": 0x588,

            ### Illburn Ruins ###
            #"Illburn - Open Ruin Gate":         0x304,
            "Illburn - Small Shield Chest":     0x4C0,
            "Illburn - Raval Ore x6 Chest":     0x4C4,
            "Illburn - Raval Ore x12 Chest":    0x4BC,
            "Illburn - Katol Elixir Chest":     0x4CC,
            "Illburn - Ruby Chest":             0x4D4,
            "Illburn - Raval Ore x8 Chest":     0x4C8,
            "Illburn - Spirit Cape Chest":      0x4D0,
            "Illburn - Raval Ore x20 Chest":    0x4B8,
            "Illburn - Pot Early Left":         0x5B0,
            "Illburn - Pot Upper Room":         0x5A4,
            "Illburn - Pot Right":              0x5B4,
            "Illburn - Pot Katol Elixir Room":  0x5C0,
            "Illburn - Pot End":                0x5A8,
            "Illburn - Pot End Up":             0x5AC,
            "Illburn - Pot End Down 1":         0x5B8,
            "Illburn - Pot End Down 2":         0x5BC,
            "Illburn - Defeat Chester":         0x308,

            ### Zone of Lava ###
            "Lava - Raval Ore x18 Chest":       0x4F0,
            "Lava - Pot Above Chasm":           0x5C4,
            "Lava - Pot In Chasm":              0x5D0,
            "Lava - Pot Mozgouz Room":          0x5D4,
            "Lava - Pot Behind Rock Wall":      0x5E0,
            "Lava - Firewyrm's Amulet Chest":   0x4EC,
            "Lava - Broadsword Chest":          0x4DC,
            "Lava - Raval Ore x200 Chest":      0x4F8,
            "Lava - Pot Right":                 0x5D8,
            "Lava - Pot Cliff Decend Top":      0x5C8,
            "Lava - Pot Cliff Descend Bottom":  0x5CC,
            "Lava - Emerald Chest":             0x4E0,
            "Lava - Pot Ledge":                 0x5DC,
            "Lava - Katol Elixir Chest":        0x4F4,
            "Lava - Defeat Guilen":             0x310,
            "Lava - Defeat Gyalva":             0x314,
            "Lava - Raval Ore x12 Chest":       0x4D8,

            ### Abandoned Mine ###
            "Mine - Pot First Shaft Top":       0x5E8,
            "Mine - Pot First Shaft Right Room": 0x5EC,
            "Mine - Raval Ore x50 Chest":       0x4A0,	
            "Mine - Pot First Shaft Bottom":    0x5E4,
            "Mine - Pot Top of Stairs":         0x5F0,
            "Mine - Raval Ore x25 Chest":       0x4A4,
            "Mine - Emerald Chest":             0x4A8,
            "Mine - Pot Behind Bottom Stairs":  0x5F4,
            "Mine - Pot Cliff Ledge":           0x5F8,
            "Mine - Raval Ore x40 Chest":       0x5FC,
            "Mine - Katol Elixir Chest":        0x4AC,
            "Mine - Raval Ore x65 Chest":       0x4B4,
            "Mine - Raval Ore x200 Chest":      0x4B0,     
            "Mine - Pot behind Rock":           0x600,
            "Mine - Defeat Istersiva":          0x324,

            ### Elderm Mountains ###
            "Mountain - Pot After Drop":        0x604,
            "Mountain - Pot Before Cave":       0x608,
            "Mountain - Pot After Drop In Cave": 0x614,
            "Mountain - Raval Ore x90 Chest":   0x4FC,
            "Mountain - Raval Ore x50 Chest":   0x508,
            "Mountain - Raval Ore x70 Chest":   0x50C,
            "Mountain - Raval Ore x40 Chest":   0x500,
            "Mountain - Berm Leaves 1":         0x43C,
            "Mountain - Berm Leaves 2":         0x444,
            "Mountain - Berm Leaves 3":         0x448,
            "Mountain - Pot Secret Cliffside":  0x60C,
            "Mountain - Defeat Ligaty":         0x32C,
            "Mountain - Berm Leaves 4":         0x440,

            "Mountain - Pot Before Ice Cave":   0x610,
            "Mountain - Katol Elixir Chest":    0x504,
            "Cave - Pot 1 Ice Room":            0x618,
            "Cave - Pot 2 Ice Room":            0x61C,
            "Cave - Pot before Ice Room":       0x620,

            ### Icebound Cave ###
            "Cave - Topaz Chest":               0x510,
            "Cave - Stone Shoes Chest":         0x518,
            "Cave - Pot Ice Platform":          0x624,
            "Cave - Raval Ore x140 Chest":      0x514,
            "Cave - Pot 1 Past Shoes":          0x628,
            "Cave - Pot 2 Past Shoes":          0x62C,
            "Cave - Raval Ore x120 Chest":     0x51C,
            "Cave - Raval Ore x140 Chest 2":    0x520,
            "Cave - Pot Behind Ice":            0x630,
            "Cave - Katol Elixir Chest":        0x524,
            "Cave - Defeat Gildias":            0x340,

            ###Valestein Castle
            "Castle - Raval Ore x200 Chest":    0x528,
            "Castle - Pot Parkour Room":        0x63C,
            "Castle - Pot Under Parkour 1":     0x644,
            "Castle - Pot Under Parkour 2":     0x640,
            "Castle - Battle Armor Chest":      0x538,
            "Castle - Raval Ore x500 Chest":    0x534,
            "Castle - Pot Room Top of West Tower": 0x650,
            "Castle - Defeat Faleon":           0x35C,
            "Castle - Topaz Chest":             0x52C,
            "Castle - Pot Top Of East Tower":   0x638,
            "Castle - Raval Ore x250 Chest":    0x540,
            "Castle - Raval Ore x320 Chest":    0x53C,
            "Castle - Place Organ Pipe":        0x368,
            "Castle - Place Holy Cross":        0x36C,
            "Castle - Place Ivory Key":         0x364,
            "Castle - Pot Boulder Room 1":      0x648,
            "Castle - Pot Boulder Room 2":      0x64C,
            "Castle - Pot Lava Room":           0x654,
            "Castle - Battle Shield Chest":     0x548,
            "Castle - Raval Ore x380 Chest":    0x544,
            "Castle - Defeat Zellfel":          0x360,

            ### Castle Dungeon ###
            "Dungeon - Pot First Room Left":    0x660,
            "Dungeon - Pot Jump Area":          0x664,
            "Dungeon - Battle Saber Chest":     0x54C,
            "Dungeon - Pot First Room Stairs":  0x65C,
            "Dungeon - Defeat Zirduros":        0x374,
            #"Clock - Open Clock Tower Door":    0x37C,
            "Clock - Ruby Chest":               0x550,
        
            ### Clock Tower ###
            "Clock - Raval Ore x350 Chest":     0x554,
            "Clock - Pot Sunset Room":          0x66C,
            "Clock - Pot Darkness Room":        0x670,
            "Clock - Pot Light Room":           0x674,
            "Clock - Pot Room After Climb":     0x678,
            "Castle - Defeat Chester":          0x380,

            "Genos - Defeat Dularn":            0x38C,
            "Genos - Raval Ore x750 Chest":     0x67C,
            "Genos - Emerald Chest":            0x558,
            "Genos - Lotus Hammer Chest":       0x634,
            "Genos - Topaz Chest":              0x568,
            "Genos - Raval Ore x720 Chest":     0x680,
            "Genos - Silver Chimes Chest":      0x560,
            "Genos - Raval Ore x640 Chest":     0x55C,
            "Genos - Raval Armor Chest":        0x564,
            "Genos - Raval Ore x960 Chest":     0x56C,
            "Genos - Pot by Square Hole":       0x684,
            "Genos - Defeat Garland":           0x390,
            

        }

        self.story_flags = {
            # "Location Name": memory_address_or_offset,
            "Quarry Entrance Paul": 0x2D0,
            #"Mine Edgar before Ellefale": 0x005C5768,
            "Quarry Boss Beaten - Chester": 0x2F0,
            "Quarry Boss Beaten - Mayor": 0x2F4,
            "Quarry Boss Beaten - Elena": 0x2F8,
            "Quarry Show Pendant": 0x2DC,

            "Lava Boss Beaten - Chester": 0x318,
            "Lava Boss Beaten - Mayor":	0x320,
            "Lava Boss Beaten - Elena": 0x31C,

            "Current Location": 0x850, #8 = Quarry
            "Teleport Location": 0x19C,
            "Overworld - Escort Quest": 0x3B4, #Is completed at flag 3

            "Spawn Ligaty": 0x328,
            #"Skip Dogi Stab": 0x344,
            "Valestein - First Bell": 0x34C,
            "Open Valestein Castle": 0x348,
            "Open Cave": 0x344,   #Address for when Dogi is stabbed

            "Sword Equipped": 0x1D4,
            "Shield Equipped": 0x1DC,
            "Armor Equipped": 0x1D8,

            "Open Castle Doors": 0x35C,
            "Use Sword Anywhere": 0x1FC,

            "Open Castle Dungeon": 0x370,                         #Always open the Castle Dungeon
            "Top of Castle Cutscene": 0x384,   #Opens Genos //Always 0 in town
            "At Genos Island": 0x388,    #Needed to talk to Dogi, so don't skip Set as win condtion for now
            "Defeat Galbanan": 0x3A8, #The Goal
        }

    def safe_read_int(self, address: int, default: int = 0) -> int:
        """Safely read an int from memory. Returns default on failure."""
        try:
            if not address or address < 0x10000:
                return default
            return self.pm.read_int(address)
        except Exception:
            return default

    def safe_write_int(self, address: int, value: int) -> bool:
        """Safely write an int to memory. Returns True if successful."""
        try:
            if not address or address < 0x10000:
                return False
            self.pm.write_int(address, value)
            return True
        except Exception:
            return False

# Safe Pointer Resolution
    def get_pointer_address(self, base_offset, offsets):
        try:
            addr = self.pm.read_int(self.base + base_offset)
            if not addr:
                return 0
            for offset in offsets[:-1]:
                addr = self.pm.read_int(addr + offset)
                if not addr:
                    return 0
            return addr + offsets[-1]
        except Exception:
            return 0

    def get_flag_address(self, offset: int) -> int:
        try:
            base_ptr = self.item_base
            if not base_ptr or base_ptr < 0x10000:
                return 0

            return base_ptr + offset
        except Exception:
            return 0

    @property
    def item_base(self):
        # Resolve base pointer dynamically
        return self.get_pointer_address(0x000028B0, [0x0])

    @property
    def gold_address(self):
        return self.get_pointer_address(0x000DA69C, [0x0])

    @property
    def raval_address(self):
        return self.get_pointer_address(0x000028B0, [0x200])


    @property
    def equipped_accessory_id(self):
        return self.get_pointer_address(0x0033C80, [0x0])

    @property
    def room_id_address(self):
        return self.base + 0x1C4238

    @property
    def current_level(self):
        return self.base + 0x1C43B0

    def get_room_id(self) -> int:
        return self.safe_read_int(self.room_id_address)

    def skip_story_flags(self, checked_names: set = None):
        if not self.pm or not self.item_base:
            return

        def safe_write(flag_key, value):
            offset = self.story_flags.get(flag_key)
            if offset is None:
                return
            addr = self.get_flag_address(offset)
            self.safe_write_int(addr, value)

        def safe_read(flag_key, default=0):
            offset = self.story_flags.get(flag_key)
            if offset is None:
                return default
            addr = self.get_flag_address(offset)
            return self.safe_read_int(addr, default)

        room = self.get_room_id()

        try:

            # Force basic story flags
            safe_write("Quarry Entrance Paul", 1)
            safe_write("Quarry Show Pendant", 1)
            safe_write("Quarry Boss Beaten - Chester", 1)
            safe_write("Quarry Boss Beaten - Mayor", 1)
            safe_write("Quarry Boss Beaten - Elena", 1)
            safe_write("Valestein - First Bell", 1)
            safe_write("Spawn Ligaty", 1)
            safe_write("Lava Boss Beaten - Chester", 1)
            safe_write("Lava Boss Beaten - Elena", 1)
            safe_write("Overworld - Escort Quest", 3)
            safe_write("Open Cave", 1)

            if self.armless == True:
                safe_write("Use Sword Anywhere", 1)
            elif self.sword_anywhere == 0 or room not in REDMONT:
                safe_write("Use Sword Anywhere", 0)

            #nop_chest = self.get_pointer_address(0x00001214, [0x944])
            #move_chest = self.get_pointer_address(0x000049E4, [0x2C8])
            #walk_talk = self.get_pointer_address(0x00008EEC, [0x0])

            #if room != 24:
                #if self.safe_read_int(nop_chest) == 1:
                #    self.safe_write_int(nop_chest, 0)
                #f self.safe_read_int(move_chest) == 1:
                #    self.safe_write_int(move_chest, 0)
                #if self.safe_read_int(walk_talk) in (1, 2):
                #    self.safe_write_int(walk_talk, 0)

            if room in REDMONT:
                safe_write("At Genos Island", 1)
            else:
                safe_write("At Genos Island", 0)

            ### Fix the inventory when in the shop
            if room == 34:
                self.strip_shop_equipment()
            elif room not in (34, 24):
                # Only restore when outside shop/street so shop stays empty
                if self.progressive_sword_count or self.progressive_shield_count or self.progressive_armor_count:
                    self.restore_shop_equipment()

                self.restore_other_shop_items()

            #Automatically open all the parts of the castle
            #if room in (40, 160, 161, 175, 189, 168, 182, 189):
            #    safe_write("Open Castle Doors", 1)
            #elif room != 174 and not self.is_location_checked("Castle - Defeat Faleon", for_sending=False):
            #    safe_write("Open Castle Doors", 0)

            #Open Castle Dungeons
            if self.open_dungeon == 0:
                safe_write("Open Castle Dungeon", 1)

            #if room in CAVE_GAP:
            #    safe_write("Open Cave", 1)

            #Using a Brocia Serum
            if "Brocia Serum" in self.authorized_items:
                brocia_addr = self.get_item_address("Brocia Serum")
                value = self.safe_read_int(brocia_addr)

                if value > 1:
                    self.safe_write_int(self.get_item_address("Brocia Serum"), 1)
                    value = 1

                if value == 0:
                    self.use_brocia()
                    self.safe_write_int(self.get_item_address("Brocia Serum"), 1)              


            # Abandoned Mine door control
            if room in (55, 57):
                if self.has_item("Nightfire Gem"):
                    safe_write("Lava Boss Beaten - Mayor", 1)
                else:
                    safe_write("Lava Boss Beaten - Mayor", 0)

            # Open Valestein Castle
            if self.has_enough_statues():
                safe_write("Open Valestein Castle", 1)
            else:
                if room in REDMONT and safe_read("Teleport Location") != 4:
                    safe_write("Open Valestein Castle", 1)
                elif safe_read("Teleport Location") == 0:
                    safe_write("Open Valestein Castle", 1)
                elif safe_read("Teleport Location") == 4:
                    safe_write("Open Valestein Castle", 0)
                else:
                    safe_write("Open Valestein Castle", 0)
                if room not in REDMONT:
                    safe_write("Open Valestein Castle", 0)

            #Open Way to Genos Island
            if self.has_enough_bosses(checked_names) and room in GENOS_UNLOCK:
                safe_write("Top of Castle Cutscene", 1)
            elif room in (204, 206, 208):
                safe_write("Top of Castle Cutscene", 1)
            else:
                safe_write("Top of Castle Cutscene", 0)

            #Experiments
            #safe_write("Teleport Location", 0) (Works)

            

        except Exception:
            pass

    def has_enough_statues(self) -> bool:
        statues = [
            "Moonstar Statue",
            "Sunset Statue",
            "Darkness Statue",
            "Light Statue",
        ]
        obtained = sum(1 for statue in statues if self.has_item(statue))
        return obtained >= self.statues_required

    def has_enough_bosses(self, checked_names: set = None) -> bool:
        bosses = [
            "Quarry - Defeat Dularn",
            "Quarry - Defeat Ellefale",
            "Illburn - Defeat Chester",
            "Lava - Defeat Guilen",
            "Lava - Defeat Gyalva",
            "Mine - Defeat Istersiva",
            "Mountain - Defeat Ligaty",
            "Cave - Defeat Gildias",
            "Castle - Defeat Faleon",
            "Castle - Defeat Zellfel",
            "Dungeon - Defeat Zirduros",
            "Castle - Defeat Chester",
            "Genos - Defeat Dularn",
            "Genos - Defeat Garland",
        ]
        
        if checked_names is None:
            checked_names = set()

        # Checks if boss is recorded locally OR synced from the server
        defeated_count = sum(
            1 for b in bosses 
            if b in checked_names or self.is_location_checked(b, for_sending=False)
        )
        
        return defeated_count >= self.bosses_required

    def get_room_id(self) -> int:
        return self.safe_read_int(self.room_id_address)

    def debt_increase(self, location_name: str):
        if not isinstance(location_name, str):
            return
        
        if "Raval Ore" in location_name:
            match = re.search(r"Raval Ore x(\d+)", location_name)
            if match:
                amount = int(match.group(1))
                self.raval_debt += amount
                ##print(f"[Debt] +{amount} Raval debt (Total debt: {self.raval_debt})")

        elif location_name in ("Quarry - Torch Ruby Chest", "Illburn - Ruby Chest", "Clock - Ruby Chest"):
            self.ruby_debt += 1

        elif location_name in ("Lava - Emerald Chest", "Mine - Emerald Chest", "Genos - Emerald Chest"):
            self.emerald_debt += 1
        elif location_name in ("Cave - Topaz Chest", "Castle - Topaz Chest", "Genos - Topaz Chest"):
            self.topaz_debt += 1
        elif "Berm Leaves" in (location_name):
            self.berm_debt += 1

    def debt_collector(self):
        try:
            if not self.item_base:
                return

            current_raval = self.get_raval()
            current_ruby = self.safe_read_int(self.get_item_address("Ruby"))
            current_emerald = self.safe_read_int(self.get_item_address("Emerald"))
            current_topaz = self.safe_read_int(self.get_item_address("Topaz"))
            current_berm = self.safe_read_int(self.get_item_address("Berm Leaves"))

            if self.raval_debt > 0 and current_raval >= self.raval_debt:
                new_value = current_raval - self.raval_debt
                self.set_raval(new_value)
                ##print(f"[Debt] Removed {self.raval_debt} Raval Ore (now {new_value})")
                self.raval_debt = 0

            if self.ruby_debt > 0 and current_ruby >= self.ruby_debt:
                self.safe_write_int(self.get_item_address("Ruby"), current_ruby - self.ruby_debt)
                self.ruby_debt = 0

            if self.emerald_debt > 0 and current_emerald >= self.emerald_debt:
                self.safe_write_int(self.get_item_address("Emerald"), current_emerald - self.emerald_debt)
                self.emerald_debt = 0

            if self.topaz_debt > 0 and current_topaz >= self.topaz_debt:
                self.safe_write_int(self.get_item_address("Topaz"), current_topaz - self.topaz_debt)
                self.topaz_debt = 0

            if self.berm_debt > 0 and current_berm == 1:
                self.safe_write_int(self.get_item_address("Berm Leaves"), -1)
                self.berm_debt = 0
            elif self.berm_debt > 0 and current_berm > 1:
                self.safe_write_int(self.get_item_address("Berm Leaves"), current_berm - self.berm_debt)
                self.berm_debt = 0



        except Exception:
            # Silently ignore all memory errors during loading/transitions
            pass

    def is_location_checked(self, location_name: str, for_sending: bool = True) -> bool:
        offset = self.location_flags.get(location_name)
        if offset is None:
            return False

        room = self.get_room_id()

        store_list = [
            "Redmont - Buy Long Sword",   "Redmont - Buy Banded Slayer",
            "Redmont - Buy Large Shield", "Redmont - Buy Banded Shield", 
            "Redmont - Buy Chain Mail", "Redmont - Buy Plate Mail",
            "Redmont - Buy Banded Mail", "Redmont - Buy Illusion Mirror",
            "Redmont - Buy Amulet", "Redmont - Buy Katol Elixir",
            "Redmont - Buy Spirit Necklace",
        ]

        addr = self.get_flag_address(offset)
        value = self.safe_read_int(addr)

        #Only send the check for a store item, if you are in the Store
        if location_name in store_list:
            if room == 24:
                self.shop_bought.add(location_name)
                return value == 1
            return False

        if location_name == "Redmont - Return Bob's Pendant" and room in (28, 30):
            return value == 0
        elif location_name == "Redmont - Return Bob's Pendant" and room not in (28, 30):
            return False
        
        if location_name == "Redmont - Give Hugo a Berm Leaves" and room in (30, 34): #or location_name == "Redmont - Give Adonis the Lotus Hammer":
            return value == 0
        elif location_name == "Redmont - Give Hugo a Berm Leaves" and room not in (30, 34): #or location_name == "Redmont - Give Adonis the Lotus Hammer":
            return False

        #if  location_name == "Redmont - Give Randolph the Jade Ring" and room == 20:
        #    return value == 0
        #elif location_name == "Redmont - Give Randolph the Jade Ring" and room != 20:
        #    return False

        #if  location_name == "Redmont - Sell the Jade Ring to Cynthia" and room == 24:
        #    return value == 0
        #elif location_name == "Redmont - Sell the Jade Ring to Cynthia" and room != 24:
        #    return False

        return value == 1

    def get_gold(self):
        return self.safe_read_int(self.gold_address)
    
    def set_gold(self, value: int):
        self.safe_write_int(self.gold_address, value)

    def add_gold(self, amount: int):
        current = self.get_gold()
        self.set_gold(current + amount)

    def give_xp(self, amount: float):
        current_xp = self.pm.read_float(self.xp_address)
        self.pm.write_float(self.xp_address, current_xp + float(amount))
        ##print(f"[AP] Granted {amount} XP! New Total: {current_xp + float(amount)}")

    def set_xp(self, value: float):
        """Set total XP (float at module+0x1C4398)."""
        addr = self.base + 0x1C4398
        value = float(value)
        try:
            # Primary
            self.pm.write_float(addr, value)
        except Exception as e:
            print(f"[set_xp] write_float failed: {e}")

        # Verify
        try:
            got = self.pm.read_float(addr)
            print(f"[set_xp] wrote {value}, read back {got}")
        except Exception as e:
            print(f"[set_xp] read back failed: {e}")

    def set_level(self, value: int):
        self.safe_write_int(self.current_level, value)

    def get_raval(self):
        return self.safe_read_int(self.raval_address)

    def set_raval(self, value: int):
        self.safe_write_int(self.raval_address, max(0, value))

    def add_raval(self, amount: int):
        addr = self.raval_address
        #print(f"[Debug] Raval address = {hex(addr) if addr else 'None'}")
        
        current = self.get_raval()
        #print(f"[Debug] Current Raval = {current}")
        
        self.set_raval(current + amount)
        #print(f"[Debug] Tried to set Raval to {current + amount}")

    def get_item_address(self, item_name):
        if item_name not in ITEMS:
            raise ValueError(f"Item '{item_name}' not found")
        if not self.item_base:
            return 0
        return self.item_base + ITEMS[item_name]

    def has_item(self, item_name):
        addr = self.get_item_address(item_name)
        return self.safe_read_int(addr) > 0

    def give_item(self, item_name):
        addr = self.get_item_address(item_name)
        if addr:
            self.authorized_items.add(item_name)
            self.pm.write_int(addr, 1)
            #print(f"Gave: {item_name}")

    def give_incremental_item(self, item_name):
        addr = self.get_item_address(item_name)
        if addr:
            try:
                value = self.pm.read_int(addr)
                if (value < 0):
                    value += 1
                self.pm.write_int(addr, value + 1)

                if item_name == "Katol Elixir":
                    self.actual_katol += 1
                if item_name == "Amulet":
                    self.actual_amulet += 1
                if item_name == "Illusion Mirror":
                    self.actual_mirror += 1

                print(f"Gained +1: {item_name}")
            except Exception as e:
                print(f"Failed to give incremental item {item_name}: {e}")

    def remove_item(self, item_name):

        addr = self.get_item_address(item_name)
        if addr:
            self.pm.write_int(addr, -1)

    def get_checked_locations(self) -> set:
        return {name for name in self.location_flags if self.is_location_checked(name, for_sending=True)}

    def remove_unauthorized_items(self):       
        try:
            for item_name in ITEMS:
                if item_name in ("Armless Trap", "Slippery Trap"):
                    continue

                if self.has_item(item_name) and item_name not in self.authorized_items:
                    self.remove_item(item_name)
        except Exception as e:
            print("Error in item guard:", e)

    def give_progressive_sword(self):

        room = self.get_room_id()
            
        if room in (24, 34):
            return


        self.progressive_sword_count += 1
        count = self.progressive_sword_count

        print(f"Progressive Sword count is now: {count}")

        # Give all swords up to current count
        for i in range(count+1):
            if i < len(SWORD_PROGRESSION):
                sword = SWORD_PROGRESSION[i]
                self.authorized_items.add(sword)
                if not self.has_item(sword):
                    self.give_item(sword)
                    print(f"  → Gained and equipped: {sword}")

        # Auto-equip current highest level
        equipped_id = min(count, 5)
        self.safe_write_int(self.get_flag_address(self.story_flags["Sword Equipped"]), equipped_id)
        #print(f"  → Equipped Sword ID: {self.get_flag_address(self.story_flags["Sword Equipped"])}")

    def give_progressive_shield(self):

        room = self.get_room_id()
    
        if room in (24, 34):
            return

        self.progressive_shield_count += 1
        count = self.progressive_shield_count

        print(f"Progressive Shield count is now: {count}")

        # Give all shields up to current count
        for i in range(count+1):
            if i < len(SHIELD_PROGRESSION):
                shield = SHIELD_PROGRESSION[i]
                self.authorized_items.add(shield)
                if not self.has_item(shield):
                    self.give_item(shield)
                    print(f"  → Gained and equipped: {shield}")

        # Auto-equip current highest level
        equipped_id = min(6 + count, 11)
        self.safe_write_int(self.get_flag_address(self.story_flags["Shield Equipped"]),  equipped_id)
        #print(f"  → Equipped Shield Flag: {self.get_flag_address(self.story_flags["Shield Equipped"])}")

    def give_progressive_armor(self):

        room = self.get_room_id()
            
        if room in (24, 34):
            return
        
        
        self.progressive_armor_count += 1
        count = self.progressive_armor_count
        
        print(f"Progressive Armor count is now: {count}")
        
        # Give all armors up to current count
        for i in range(count+1):
            if i < len(ARMOR_PROGRESSION):
                armor = ARMOR_PROGRESSION[i]
                self.authorized_items.add(armor)
                if not self.has_item(armor):
                    self.give_item(armor)
                    print(f"  → Gained and equipped: {armor}")

                # Auto-equip current highest level
        equipped_id = min(12 + count, 17)
        self.safe_write_int(self.get_flag_address(self.story_flags["Armor Equipped"]), equipped_id)
        #print(f"  → Equipped Armor ID: {self.get_flag_address(self.story_flags["Armor Equipped"])}")

    def give_progressive_ignis(self):
        self.progressive_ignis_count += 1
        self.authorized_items.add("Ignis Bracelet")
        if not self.has_item("Ignis Bracelet"):  
            self.give_item("Ignis Bracelet")
            print(f"  → Gained the Ignis Bracelet")

        if self.progressive_ignis_count > 1:
            rubies = self.progressive_ignis_count -1
            self.pm.write_int(self.get_item_address("Ruby"), min(rubies, 3))

    def give_progressive_ventus(self):
        self.progressive_ventus_count += 1
        self.authorized_items.add("Ventus Bracelet")
        if not self.has_item("Ventus Bracelet"):
            self.give_item("Ventus Bracelet")
            print(f"  → Gained the Ventus Bracelet")

        if self.progressive_ventus_count > 1:
            emeralds = self.progressive_ventus_count -1
            self.pm.write_int(self.get_item_address("Emerald"), min(emeralds, 3))

    def give_progressive_terra(self):
        self.progressive_terra_count += 1
        self.authorized_items.add("Terra Bracelet")
        if not self.has_item("Terra Bracelet"): 
            self.give_item("Terra Bracelet")
            print(f"  → Gained the Terra Bracelet")

        if self.progressive_terra_count > 1:
            terra = self.progressive_terra_count -1
            self.pm.write_int(self.get_item_address("Topaz"), min(terra, 3))

    def give_keys(self):
        self.authorized_items.add("Storehouse Key")
        self.give_item("Storehouse Key")
        self.authorized_items.add("Ruins Key")
        self.give_item("Ruins Key")
        self.authorized_items.add("Clock Tower Key")
        self.give_item("Clock Tower Key")

    def get_equipped_accessory(self):
        addr = self.equipped_accessory_id
        if addr:
            return self.safe_read_int(addr)
        return None

    def auto_equip_accessory(self):
        room = self.get_room_id()
        if  (room in (183, 70, 71, 72, 74, 75, 76, 77, 78, 79, 80)
            and self.has_item("Nightfire Gem")
            and self.safe_read_int(self.equipped_accessory_id) != 18):
                self.safe_write_int(self.equipped_accessory_id, 18)
        if  (room in (184, 112, 113, 128, 116)
            and self.has_item("Firewyrm's Amulet")
            and self.safe_read_int(self.equipped_accessory_id) != 19):
                self.safe_write_int(self.equipped_accessory_id, 19)
        if  (room in (163, 177, 83, 145, 148, 149, 151, 152, 153, 154, 155, 158)
            and self.has_item("Stone Shoes")
            and self.safe_read_int(self.equipped_accessory_id) != 20):
                self.safe_write_int(self.equipped_accessory_id, 20)


    def sync_received_items(self, received_item_names: list[str]):
        if not self.item_base or self.item_base < 0x10000:
            return

        room = self.get_room_id()

        if room in (24, 34):
            return

        increment_list = {
            "Amulet", "Berm Leaves", "Ruby", "Topaz", "Emerald", "Katol Elixir",
            "XP x50000", "XP x25000", "Raval Ore x2000", "Gold x15000", "Gold x10000", "Gold x5000", "Raval Ore x200", "XP x5000",
        }

        # --- Progressive counts from Archipelago ---
        needed_sword  = received_item_names.count("Progressive Sword")
        needed_shield = received_item_names.count("Progressive Shield")
        needed_armor  = received_item_names.count("Progressive Armor")
        needed_ignis  = received_item_names.count("Progressive Ignis")
        needed_ventus = received_item_names.count("Progressive Ventus")
        needed_terra  = received_item_names.count("Progressive Terra")

        for item_name in received_item_names:
            # Ignore traps or invalid items safely inside the loop
            if item_name not in ITEMS or ITEMS[item_name] is None:
                continue

        while self.progressive_sword_count < needed_sword:
            self.give_progressive_sword()
        while self.progressive_shield_count < needed_shield:
            self.give_progressive_shield()
        while self.progressive_armor_count < needed_armor:
            self.give_progressive_armor()
        while self.progressive_ignis_count < needed_ignis:
            self.give_progressive_ignis()
        while self.progressive_ventus_count < needed_ventus:
            self.give_progressive_ventus()
        while self.progressive_terra_count < needed_terra:
            self.give_progressive_terra()

        # Safety: if count > 0 but item was lost on death, put it back
        if needed_ignis > 0:
            self.authorized_items.add("Ignis Bracelet")
            if not self.has_item("Ignis Bracelet"):
                self.give_item("Ignis Bracelet")
            if needed_ignis > 1:
                self.safe_write_int(self.get_item_address("Ruby"), min(needed_ignis - 1, 3))

        if needed_ventus > 0:
            self.authorized_items.add("Ventus Bracelet")
            if not self.has_item("Ventus Bracelet"):
                self.give_item("Ventus Bracelet")
            if needed_ventus > 1:
                self.safe_write_int(self.get_item_address("Emerald"), min(needed_ventus - 1, 3))

        if needed_terra > 0:
            self.authorized_items.add("Terra Bracelet")
            if not self.has_item("Terra Bracelet"):
                self.give_item("Terra Bracelet")
            if needed_terra > 1:
                self.safe_write_int(self.get_item_address("Topaz"), min(needed_terra - 1, 3))

        # --- Normal items ---
        for item_name in received_item_names:
            if item_name in ITEMS and item_name not in increment_list:
                self.authorized_items.add(item_name)
                if not self.has_item(item_name):
                    self.give_item(item_name)

        if "Keyring" in received_item_names:
            self.give_keys()

        self.sync_progressive_gear()

    def sync_progressive_gear(self):

        room = self.get_room_id()

        if room in (24, 34):
            return
            
        """Ensures equipment values in memory match the current progressive counts."""
        # Ensure non-zero progressive counts re-apply their respective gear up to current count
        for i in range(min(self.progressive_sword_count + 1, len(SWORD_PROGRESSION))):
            sword = SWORD_PROGRESSION[i]
            if not self.has_item(sword):
                self.give_item(sword)
                self.safe_write_int(self.get_flag_address(self.story_flags["Sword Equipped"]), min(self.progressive_sword_count, 5))

        for i in range(min(self.progressive_shield_count + 1, len(SHIELD_PROGRESSION))):
            shield = SHIELD_PROGRESSION[i]
            if not self.has_item(shield):
                self.give_item(shield)
                self.safe_write_int(self.get_flag_address(self.story_flags["Shield Equipped"]), min(self.progressive_shield_count+5, 11))

        for i in range(min(self.progressive_armor_count + 1, len(ARMOR_PROGRESSION))):
            armor = ARMOR_PROGRESSION[i]
            if not self.has_item(armor):
                self.give_item(armor)
                self.safe_write_int(self.get_flag_address(self.story_flags["Armor Equipped"]), min(self.progressive_armor_count+11, 17))
                
    def rebuild_from_received(self, received_item_names: list[str]):
        """Call this on connect / reconnect to restore progressive counts and authorized items."""
        self.progressive_sword_count = 0
        self.progressive_shield_count = 0
        self.progressive_armor_count = 0
        self.progressive_ignis_count = 0
        self.progressive_ventus_count = 0
        self.progressive_terra_count = 0

        # Keep the always-allowed starting items
        # (your __init__ already seeds some)

        for name in received_item_names:
            if name == "Progressive Sword":
                self.give_progressive_sword()
            elif name == "Progressive Shield":
                self.give_progressive_shield()
            elif name == "Progressive Armor":
                self.give_progressive_armor()
            elif name == "Progressive Ignis":
                self.give_progressive_ignis()
            elif name == "Progressive Ventus":
                self.give_progressive_ventus()
            elif name == "Progressive Terra":
                self.give_progressive_terra()
            elif name == "Keyring":
                self.give_keys()
            elif name in ITEMS:
                self.authorized_items.add(name)
                if not self.has_item(name):
                    # For normal items; incremental can be handled separately if needed
                    if not name.startswith("XP ") and not name.startswith("Raval Ore ") and not name.endswith("trap") and name not in ("Berm Leaves", "Katol Elixir", "Amulet", "Illusion Mirror"):
                        self.give_item(name)

    def strip_shop_equipment(self):
        """Hide equipment in memory only (do not touch authorized_items)."""
        katol_addr = self.get_item_address("Katol Elixir")
        mirror_addr = self.get_item_address("Illusion Mirror")
        amulet_addr = self.get_item_address("Amulet")

        katol_val = self.safe_read_int(katol_addr)
        if katol_val != -1:
            self.actual_katol = katol_val
    
        mirror_val = self.safe_read_int(mirror_addr)
        if mirror_val != -1:
            self.actual_mirror = mirror_val

        amulet_val = self.safe_read_int(amulet_addr)
        if amulet_val != -1:
            self.actual_amulet = amulet_val

        for item_name, loc_name in SHOP_ITEMS.items():
            if loc_name in self.shop_bought:
                continue
            addr = self.get_item_address(item_name)
            if addr:
                self.safe_write_int(addr, -1)

    def restore_shop_equipment(self):
        """Put back equipment you actually own from progressive counts / authorized."""
        # Swords
        for i in range(min(self.progressive_sword_count + 1, len(SWORD_PROGRESSION))):
            self.authorized_items.add(SWORD_PROGRESSION[i])
            if not self.has_item(SWORD_PROGRESSION[i]):
                self.give_item(SWORD_PROGRESSION[i])
        if self.progressive_sword_count >= 0:
            self.safe_write_int(
                self.get_flag_address(self.story_flags["Sword Equipped"]),
                min(self.progressive_sword_count, 5),
            )

        # Shields
        for i in range(min(self.progressive_shield_count + 1, len(SHIELD_PROGRESSION))):
            self.authorized_items.add(SHIELD_PROGRESSION[i])
            if not self.has_item(SHIELD_PROGRESSION[i]):
                self.give_item(SHIELD_PROGRESSION[i])
        self.safe_write_int(
            self.get_flag_address(self.story_flags["Shield Equipped"]),
            min(6 + self.progressive_shield_count, 11),
        )

        # Armor
        for i in range(min(self.progressive_armor_count + 1, len(ARMOR_PROGRESSION))):
            self.authorized_items.add(ARMOR_PROGRESSION[i])
            if not self.has_item(ARMOR_PROGRESSION[i]):
                self.give_item(ARMOR_PROGRESSION[i])
        self.safe_write_int(
            self.get_flag_address(self.story_flags["Armor Equipped"]),
            min(12 + self.progressive_armor_count, 17),
        )

    def restore_other_shop_items(self):
        
        self.safe_write_int(self.get_item_address("Katol Elixir"), self.actual_katol)
        self.safe_write_int(self.get_item_address("Illusion Mirror"), self.actual_mirror)
        self.safe_write_int(self.get_item_address("Amulet"), self.actual_amulet)

    def use_brocia(self):
        if self.brocia_serum_change == 0:
            self.give_item("Dash")
            return

        #Give yourself a flat 10000xp
        if self.brocia_serum_change == 6:
            self.give_xp(10000.0)
            return

        
        if self.brocia_serum_change not in (1, 2, 3, 4,5):
            return

        #Set your level to the boss level
        boss_level = self.brocia_serum_change -1
        room = self.get_room_id()        

        room_base = {
            55: 6,
            65: 7,
            108: 13,
            115: 16, 
            123: 18,
            81: 23,
            136: 26,
            157: 31,
            171: 33,
            185: 36,
            193: 39,
            204: 42,
            209: 44,
            224: 50,
        }

        xp_table = {
        6: 3801.0,          7: 5477.0,        8: 7457.0,        9: 9743.0,
        10: 12334.0,        11: 15229.0,      12: 18430.0,      13: 21936.0,
        14: 25747.0,        15: 29863.0,      16: 34284.0,      17: 39011.0,
        18: 44042.0,        19: 49378.0,      20: 55020.0,      21: 60967.0,
        22: 67218.0,        23: 73775.0,      24: 80637.0,      25: 87804.0,
        26: 95276.0,        27: 103053.0,     28: 111135.0,     29: 119523.0,
        30: 128215.0,       31: 137212.0,     32: 146515.0,     33: 156123.0,
        34: 166035.0,       35: 176253.0,     36: 186776.0,     37: 197604.0,
        38: 208737.0,       39: 220175.0,     40: 231918.0,     41: 243967.0,
        42: 256320.0,       43: 268978.0,     44: 281942.0,     45: 295211.0, 
        46: 308784.0,       47: 322663.0,     48: 336847.0,     49: 351336.0,
        50: 366130.0,       51: 381229.0,     52: 396634.0,     53: 412343.0,
        54: 428357.0,       55: 444677.0,     56: 461301.0,     57: 478231.0,
        58: 495466.0,       59: 513006.0,     60: 530851.0,
        }

        base = room_base.get(room)
        if base is None:
            return

        
        become_level = base + boss_level
        become_xp = xp_table.get(become_level)

        if become_xp is None:
            return
        
        self.set_xp(become_xp)
        self.set_level(become_level)

        # Verify
        #print("Wrote level", become_level, "xp", become_xp)
        print("Read level", self.safe_read_int(self.current_level))
        #print("Read xp", self.pm.read_float(self.xp_address))

    def armless_trap(self, active: bool):
        self.armless = active

    def slippery_trap(self, active: bool):
        if active:
            self.pm.write_uchar(self.value_ice_addr, 0x3C)
        else:
            self.pm.write_uchar(self.value_ice_addr, 0x00)
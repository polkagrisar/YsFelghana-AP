from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from BaseClasses import Item, ItemClassification, Location
from .Items import item_name_to_id, item_table
from .Locations import location_name_to_id
from .Regions import create_regions
from .Options import YsFelghanaOptions


def launch_ys_client(*args):
    from worlds.Ys_Felghana.Client import launch  # your actual package path
    launch_component(launch, name="Ys Felghana Client", args=args)

components.append(Component(
    "YsFelghana Client",
    func=launch_ys_client,
    component_type=Type.CLIENT,
    description="Client for Ys: The Oath in Felghana",
))


class YsFelghanaWeb(WebWorld):
    theme = "grassland"


class YsFelghanaWorld(World):
    game = "Ys Felghana"
    web = YsFelghanaWeb()
    options_dataclass = YsFelghanaOptions
    options: YsFelghanaOptions

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def create_regions(self):
        create_regions(self.multiworld, self.player)
        self.create_events()

        # Set the victory condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def pre_fill(self):

        # Handle Statues
        if self.options.statue_placement == "vanilla":
            statue_placements = {
                "Quarry - Defeat Ellefale": "Moonstar Statue",
                "Lava - Defeat Gyalva": "Sunset Statue",
                "Mine - Defeat Istersiva": "Darkness Statue",
                "Cave - Defeat Gildias": "Light Statue",
            }

            for loc_name, item_name in statue_placements.items():
                location = self.multiworld.get_location(loc_name, self.player)
                item = self.create_item(item_name)
                location.place_locked_item(item)

    def create_events(self):
        boss_events = {
            "Quarry - Defeat Dularn":    "Defeated Dularn",
            "Quarry - Defeat Ellefale":  "Defeated Ellefale",
            "Illburn - Defeat Chester":  "Defeated Chester 1",
            "Lava - Defeat Guilen":      "Defeated Guilen",
            "Lava - Defeat Gyalva":      "Defeated Gyalva",
            "Mine - Defeat Istersiva":   "Defeated Istersiva",
            "Mountain - Defeat Ligaty":  "Defeated Ligaty",
            "Cave - Defeat Gildias":     "Defeated Gildias",
            "Castle - Defeat Faleon":    "Defeated Faleon",
            "Castle - Defeat Zellfel":   "Defeated Zellfel",
            "Dungeon - Defeat Zirduros": "Defeated Zirduros",
            "Castle - Defeat Chester":   "Defeated Chester 2",
            "Genos - Defeat Dularn":     "Defeated Dularn 2",
            "Genos - Defeat Garland":    "Defeated Garland",
        }

        for location_name, event_name in boss_events.items():
            # Get the original boss location
            boss_location = self.multiworld.get_location(location_name, self.player)

            # Create a new hidden event location in the same region
            event_location = Location(
                self.player,
                event_name,               # Name of the event
                None,                     # No real ID needed for pure events
                boss_location.parent_region
            )

            # Place the event item on this new location
            event_location.place_locked_item(self.create_event(event_name))

            # Make the event location only reachable when the real boss location is checked
            event_location.access_rule = lambda state, loc=boss_location: state.can_reach(loc, "Location", self.player)

            # Add it to the region
            boss_location.parent_region.locations.append(event_location)

        # Victory event
        victory_region = self.multiworld.get_region("Dark Shrine", self.player)  # or any region
        victory_location = Location(self.player, "Victory", None, victory_region)
        victory_location.place_locked_item(self.create_event("Victory"))
        victory_region.locations.append(victory_location)


    def create_event(self, name: str):
        return Item(name, ItemClassification.progression, None, self.player)

    def fill_slot_data(self) -> dict:
        return {
            "statues_required": self.options.statues_required.value,
            "bosses_required": self.options.bosses_required.value,
            "auto_item": self.options.auto_item.value,
            "keyring_item": self.options.keyring_item.value,
            "brocia_serum_change": self.options.brocia_serum_change.value,
            "sword_anywhere": self.options.sword_anywhere.value,
            "trap_filler": self.options.trap_filler.value,
        }

    def create_items(self):
        item_pool = []
        
        ##Force starting items
        self.multiworld.push_precollected(self.create_item("Map of Felghana"))
        self.multiworld.push_precollected(self.create_item("Wing Talisman"))

        if self.options.brocia_start == True:
            self.multiworld.push_precollected(self.create_item("Brocia Serum"))


        # Always place Bob's Pendant at its original location
        bobs_location = self.multiworld.get_location("Quarry - Bob's Pendant", self.player)
        bobs_item = self.create_item("Bob's Pendant")
        bobs_location.place_locked_item(bobs_item)

        # Items with multiple Copies
        item_pool += [self.create_item("Progressive Sword")] * (5 + self.options.extra_progressive.value)
        item_pool += [self.create_item("Progressive Armor")] * (5 + self.options.extra_progressive.value)
        item_pool += [self.create_item("Progressive Shield")] * (5 + self.options.extra_progressive.value)
        item_pool += [self.create_item("Katol Elixir")] * 5
        item_pool += [self.create_item("Berm Leaves")] * 4 # Might also just remove
        item_pool += [self.create_item("XP x50000")] * 3
        item_pool += [self.create_item("XP x25000")] * 6
        item_pool += [self.create_item("XP x15000")] * 10
        item_pool += [self.create_item("XP x10000")] * 12
        item_pool += [self.create_item("Raval Ore x2000")] * 3
        item_pool += [self.create_item("Magic Wallet")] * 7
        #item_pool += [self.create_item("Gold x15000")] * 6
        #item_pool += [self.create_item("Gold x10000")] * 10

        #Bracelets
        if self.options.progressive_bracelets == False:
            item_pool += [self.create_item("Ruby")] * 3
            item_pool += [self.create_item("Emerald")] * 3
            item_pool += [self.create_item("Topaz")] * 3
            item_pool += [self.create_item("Ignis Bracelet")]
            item_pool += [self.create_item("Ventus Bracelet")]
            item_pool += [self.create_item("Terra Bracelet")]
        else:
            item_pool += [self.create_item("Progressive Ignis")] * 4
            item_pool += [self.create_item("Progressive Ventus")] * 4
            item_pool += [self.create_item("Progressive Terra")] * 4

        # Statues
        if self.options.statue_placement == "randomized":
            item_pool += [
                self.create_item("Moonstar Statue"),
                self.create_item("Sunset Statue"),
                self.create_item("Darkness Statue"),
                self.create_item("Light Statue"),
            ]

        if self.options.brocia_start == False:
            item_pool += [self.create_item("Brocia Serum")]


        if self.options.brocia_serum_change > 0:
            item_pool += [self.create_item("Dash")]


        # Other Items
        item_pool += [

            self.create_item("Firewyrm's Amulet"),
            self.create_item("Nightfire Gem"),
            self.create_item("Stone Shoes"),
            self.create_item("Spirit Cape"),
            self.create_item("Silver Chimes"),
            self.create_item("Spirit Necklace"),
            self.create_item("Illusion Mirror"),
            self.create_item("Amulet"),
            self.create_item("Silver Pendant"),
            self.create_item("Mission Tablet"),
            self.create_item("Organ Pipe"),
            self.create_item("Ivory Key"),
            self.create_item("Holy Cross"),
            self.create_item("Jade Ring"),
            self.create_item("Talisman of War"),
            self.create_item("Augite Brooch"),
            self.create_item("Lotus Hammer"),   
            self.create_item("Double Jump"),       
             
        ]

        #Keys
        if self.options.keyring_item in ("dont_add", "add_keep"):
            item_pool += [

                self.create_item("Storehouse Key"),
                self.create_item("Ruins Key"),
                self.create_item("Clock Tower Key"),

            ]

        if self.options.keyring_item in ("add_keep", "add_remove"):
            item_pool += [self.create_item("Keyring")]

        if self.options.keyring_item == "add_replace":
            item_pool += [self.create_item("Keyring")] * 3

    #Trap Items (Not customizable for now)
        item_pool += [self.create_item("Armless Trap")] * 10
        item_pool += [self.create_item("Slippery Trap")] * 10

    # Filler items - fill the rest of the pool
    # Calculate how many filler we need
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        filler_needed = total_locations - len(item_pool)
        

        if self.options.trap_filler > 0:
            trap_fill = round(filler_needed * (self.options.trap_filler / 100))

            for _ in range(trap_fill):

                item_pool.append(self.create_item(self.get_trap_item_name()))


        filler_needed = total_locations - len(item_pool)

        for _ in range(filler_needed):
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool

    def create_item(self, name: str):
        return Item(name, item_table[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        # Dynamically fetch all item names classified as filler from item_table
        filler_items = [
            name for name, classification in item_table.items() 
            if classification == ItemClassification.filler
        ]
        return self.random.choice(filler_items)

    def get_trap_item_name(self) -> str:
        # Dynamically fetch all item names classified as traps from item_table
        trap_items = [
            name for name, classification in item_table.items() 
            if classification == ItemClassification.trap
        ]
        return self.random.choice(trap_items)
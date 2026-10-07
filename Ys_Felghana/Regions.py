from BaseClasses import Region, Location, MultiWorld
from .Locations import location_name_to_id

def has_enough_bosses(state, player, amount):
    bosses = [

        "Defeated Dularn", "Defeated Ellefale",
        "Defeated Chester 1", "Defeated Guilen",
        "Defeated Gyalva", "Defeated Istersiva",
        "Defeated Ligaty", "Defeated Gildias",
        "Defeated Faleon", "Defeated Zellfel",
        "Defeated Zirduros", "Defeated Chester 2",
        "Defeated Dularn 2", "Defeated Garland",

        ]
    
    return sum(state.has(boss, player) for boss in bosses) >= amount

def has_enough_statues(state, player, amount: int) -> bool:
    statues = [
        "Moonstar Statue",
        "Sunset Statue",
        "Darkness Statue",
        "Light Statue",
    ]
    return sum(state.has(statue, player) for statue in statues) >= amount

def create_regions(world: MultiWorld, player: int):

    # ======================
    # Create Regions
    # ======================
    menu            = Region("Menu", player, world)
    redmont         = Region("Redmont", player, world)
    quarry          = Region("Tigray Quarry", player, world)
    illburn         = Region("Illburn Ruins", player, world)
    illburn_right   = Region("Illburn Ruins - Right Side", player, world)
    lava            = Region("Zone of Lava", player, world)
    lava_lava       = Region("Zone of Lava - Lava Side", player, world)
    lava_right      = Region("Zone of Lava - Right Side", player, world)
    mine            = Region("Abandoned Mine", player, world)
    mine_deep       = Region("Abandoned Mine - Deep", player, world)
    mountain        = Region("Elderm Mountains", player, world)
    mountain_right  = Region("Eldern Mountains - Right", player, world)
    cave            = Region("Icebound Cave", player, world)
    cave_ice        = Region("Icebound Cave - Icy", player, world)
    castle          = Region("Valestein Castle", player, world)
    castle_west     = Region("Valestein Castle - West", player, world)
    dungeon         = Region("Dungeon", player, world)
    clock           = Region("Clock Tower", player, world)
    genos           = Region("Genos Island", player, world)
    shrine          = Region("Dark Shrine", player, world)

    options = world.worlds[player].options
    bosses_required = options.bosses_required.value
    statues_required = options.statues_required.value
    open_dungeon = options.open_dungeon.value

    # ======================
    # Redmont Locations
    # ======================
    redmont_locations = [
        "Redmont - Return Bob's Pendant",
        "Redmont - Give Hugo a Berm Leaves",
        #"Redmont - Give Randolph the Jade Ring",
        #"Redmont - Sell the Jade Ring to Cynthia",
        #"Redmont - Give Adonis the Lotus Hammer",
        "Redmont - Buy Long Sword",
        "Redmont - Buy Banded Slayer",
        "Redmont - Buy Large Shield",
        "Redmont - Buy Banded Shield", 
        "Redmont - Buy Chain Mail",
        "Redmont - Buy Plate Mail",
        "Redmont - Buy Banded Mail",
        "Redmont - Buy Illusion Mirror",
        "Redmont - Buy Amulet",
        "Redmont - Buy Katol Elixir",
        "Redmont - Buy Spirit Necklace",
        "Overworld - Pot by the Dock",
    ]
    for name in redmont_locations:
        redmont.locations.append(Location(player, name, location_name_to_id[name], redmont))

    # ======================
    # Tigray Quarry Locations
    # ======================
    quarry_locations = [
        "Quarry - Raval Ore x5 Chest",
        "Quarry - Raval Ore x8 Chest",
        #"Quarry - Open Storehouse Door",
        "Quarry - Defeat Dularn",
        "Quarry - Ignis Bracelet Chest",
        "Quarry - Defeat Ellefale",
        "Quarry - Torch Ruby Chest",
        "Quarry - Pot Above Stairs",
        "Quarry - Pot Under Stairs",
        "Quarry - Pot Room After Dewey",
        "Quarry - Pot Outside Ellefale",
        "Quarry - Bob's Pendant",
        "Quarry - Pot Bob's Pendant",
        "Quarry - Pot Outside Mine",
        "Quarry - Pot Main Room Double Jump",
    ]
    for name in quarry_locations:
        quarry.locations.append(Location(player, name, location_name_to_id[name], quarry))


    # ======================
    # Illburn Ruins Locations
    # ======================
    illburn_locations = [
        #"Illburn - Open Ruin Gate",
        "Illburn - Small Shield Chest",
        "Illburn - Raval Ore x6 Chest",
        "Illburn - Raval Ore x12 Chest",
        "Illburn - Pot Early Left",
        "Illburn - Pot Upper Room", #ventus_ignis or doublejump(?)
        "Illburn - Pot Right",

    ]
    for name in illburn_locations:
        illburn.locations.append(Location(player, name, location_name_to_id[name], illburn))

    illburn_right_locations = [
        "Illburn - Pot Katol Elixir Room",
        "Illburn - Katol Elixir Chest",
        "Illburn - Ruby Chest",
        "Illburn - Raval Ore x8 Chest",
        "Illburn - Spirit Cape Chest",
        "Illburn - Raval Ore x20 Chest",
        "Illburn - Pot End",
        "Illburn - Pot End Up",
        "Illburn - Pot End Down 1",
        "Illburn - Pot End Down 2",
        "Illburn - Defeat Chester",
    ]
    for name in illburn_right_locations:
        illburn_right.locations.append(Location(player, name, location_name_to_id[name], illburn_right))    

    # ======================
    # Zone of Lava Locations
    # ======================
    lava_locations = [


        "Lava - Raval Ore x18 Chest",
        "Lava - Firewyrm's Amulet Chest",
        "Lava - Raval Ore x200 Chest", #terra
        "Lava - Pot Above Chasm",
        "Lava - Pot In Chasm",
        "Lava - Pot Mozgouz Room",
        "Lava - Pot Behind Rock Wall", #terra

    ]
    for name in lava_locations:
        lava.locations.append(Location(player, name, location_name_to_id[name], lava))

    lava_lava_locations = [

        "Lava - Broadsword Chest", #Firewyrm
        "Lava - Pot Cliff Decend Top", #Firewyrm
        "Lava - Pot Cliff Descend Bottom", #Firewyrm
        "Lava - Emerald Chest",
        "Lava - Defeat Guilen", #Firewyrm ventus

    ]
    for name in lava_lava_locations:
        lava_lava.locations.append(Location(player, name, location_name_to_id[name], lava_lava))

    lava_right_locations = [

        ##After the ventus or doublejump side
        "Lava - Pot Right",
        "Lava - Defeat Gyalva",
        "Lava - Pot Ledge", #doublejump
        "Lava - Katol Elixir Chest", #doublejump
        "Lava - Raval Ore x12 Chest",
    ]
    for name in lava_right_locations:
        lava_right.locations.append(Location(player, name, location_name_to_id[name], lava_right))

    # ======================
    # Abandoned Mine Locations
    # ======================
    mine_locations = [

        "Mine - Pot First Shaft Top",
        "Mine - Pot First Shaft Right Room",    #ventus, dash + doublejump, 
        "Mine - Raval Ore x50 Chest", #ventus, dash + doublejump, 		
        "Mine - Pot First Shaft Bottom",

    ]
    for name in mine_locations:
        mine.locations.append(Location(player, name, location_name_to_id[name], mine))

    mine_deep_locations = [
        "Mine - Pot Top of Stairs",
        "Mine - Raval Ore x25 Chest",
        "Mine - Pot Behind Bottom Stairs",
        "Mine - Pot Cliff Ledge",
        "Mine - Raval Ore x40 Chest",

        "Mine - Emerald Chest", #ventus+dash+doublejump
        "Mine - Katol Elixir Chest", #ventus, dash+doublejump
        "Mine - Raval Ore x65 Chest", #ventus+doublejump
        "Mine - Raval Ore x200 Chest", #ventus + doublejump + terra        
        "Mine - Pot behind Rock",	#ventus + doublejump + terra
        "Mine - Defeat Istersiva", #ventus + doublejump
    ]
    for name in mine_deep_locations:
        mine_deep.locations.append(Location(player, name, location_name_to_id[name], mine_deep))

    # ======================
    # Eldermn Mountains Locations
    # ======================
    
    mountain_locations = [
        "Mountain - Pot After Drop",
        "Mountain - Pot Before Cave",
        "Mountain - Pot After Drop In Cave",
        "Mountain - Raval Ore x90 Chest",
        "Mountain - Raval Ore x50 Chest",
        "Mountain - Raval Ore x70 Chest",
        "Mountain - Raval Ore x40 Chest",
        "Mountain - Berm Leaves 1",
        "Mountain - Berm Leaves 2",
        "Mountain - Berm Leaves 3", #terra_or_ignis
        "Mountain - Pot Secret Cliffside",
        "Mountain - Defeat Ligaty", 
        "Mountain - Berm Leaves 4",

        "Mountain - Pot Before Ice Cave",
        "Mountain - Katol Elixir Chest", #dash or ventus
        "Cave - Pot 1 Ice Room",
        "Cave - Pot 2 Ice Room",
        "Cave - Pot before Ice Room",
    ]

    for name in mountain_locations:
        mountain.locations.append(Location(player, name, location_name_to_id[name], mountain))


    mountain_right_locations = [
        "Mountain - Defeat Ligaty", 
        "Mountain - Berm Leaves 4",

        "Mountain - Pot Before Ice Cave",
        "Mountain - Katol Elixir Chest", #dash or ventus
        "Cave - Pot 1 Ice Room",
        "Cave - Pot 2 Ice Room",
        "Cave - Pot before Ice Room",
    ]

    for name in mountain_right_locations:
        mountain_right.locations.append(Location(player, name, location_name_to_id[name], mountain_right))

    # ======================
    # Icebound Cave Locations
    # ======================
    cave_locations = [
        "Cave - Topaz Chest",
        "Cave - Stone Shoes Chest",
    
    ]
    for name in cave_locations:
        cave.locations.append(Location(player, name, location_name_to_id[name], cave))

    cave_ice_locations = [    
        "Cave - Pot Ice Platform",
        "Cave - Raval Ore x120 Chest",
        "Cave - Raval Ore x140 Chest", #stoneshoes
        "Cave - Pot 1 Past Shoes", #stoneshoes
        "Cave - Pot 2 Past Shoes", #stoneshoes
        "Cave - Raval Ore x140 Chest 2", #stoneshoes
        "Cave - Pot Behind Ice", #stoneshoes
        "Cave - Katol Elixir Chest", #stoneshoes
        "Cave - Defeat Gildias", #stoneshoes
    ]
    for name in cave_ice_locations:
        cave_ice.locations.append(Location(player, name, location_name_to_id[name], cave_ice))

    castle_locations = [
        "Castle - Raval Ore x200 Chest", #doublejump, ventus
        "Castle - Pot Parkour Room",	#ventus, doublejump, dash
        "Castle - Pot Under Parkour 1",	#doublejump, ventus
        "Castle - Pot Under Parkour 2",	#doublejump, ventus 
        "Castle - Battle Armor Chest",	#doublejump, ventus
        "Castle - Raval Ore x500 Chest",
        "Castle - Defeat Faleon",	    #doublejump, ventus, dash
        "Castle - Topaz Chest",	            #doublejump
        "Castle - Pot Top Of East Tower",   #doublejump, ventus, terra_jump
    ]

    for name in castle_locations:
        castle.locations.append(Location(player, name, location_name_to_id[name], castle))

    castle_west_locations = [
        "Castle - Raval Ore x250 Chest",    #dash_double + ventus
        "Castle - Raval Ore x320 Chest",    #terra + doublejump
        "Castle - Place Organ Pipe",        #Need Organ Pipe
        "Castle - Place Holy Cross",        #Need Holy Cross
        "Castle - Place Ivory Key",         #Need Ivory Key
        "Castle - Pot Boulder Room 1",		#stoneshoes
        "Castle - Pot Boulder Room 2",		#stoneshoes
        "Castle - Pot Lava Room",			#doublejump, ventus
        "Castle - Pot Room Top of West Tower",
        "Castle - Battle Shield Chest",		#doublejump + terra, ventus + terra
        "Castle - Raval Ore x380 Chest",	#Nightgem
        "Castle - Defeat Zellfel",			#Nightgem
    ]

    for name in castle_west_locations:
        castle_west.locations.append(Location(player, name, location_name_to_id[name], castle_west))

    dungeon_locations = [
        "Dungeon - Pot First Room Left",        #doublejump, ventus,
        "Dungeon - Pot Jump Area",              #doublejump, ventus,
        "Dungeon - Battle Saber Chest",         #ventus, #doublejump + terra_jump1
        "Dungeon - Pot First Room Stairs",      #ventus, #doublejump + terra_jump1
        "Dungeon - Defeat Zirduros",
        #"Clock - Open Clock Tower Door",        #clock_key
        "Clock - Ruby Chest",                   #doublejump + clock_key + ventus, clock_key + doublejump + ignis
        ]
    
    for name in dungeon_locations:
        dungeon.locations.append(Location(player, name, location_name_to_id[name], dungeon))

    clock_locations = [
        "Clock - Raval Ore x350 Chest",
        "Clock - Pot Sunset Room",
        "Clock - Pot Darkness Room",
        "Clock - Pot Light Room",
        "Clock - Pot Room After Climb",
        "Castle - Defeat Chester",
        ]
    
    for name in clock_locations:
        clock.locations.append(Location(player, name, location_name_to_id[name], clock))

    genos_locations = [
        "Genos - Defeat Dularn",
    ]

    for name in genos_locations:
        genos.locations.append(Location(player, name, location_name_to_id[name], genos))

    shrine_locations = [
        "Genos - Raval Ore x750 Chest",
        "Genos - Emerald Chest",
        "Genos - Lotus Hammer Chest",
        "Genos - Topaz Chest",
        "Genos - Raval Ore x720 Chest",
        "Genos - Silver Chimes Chest",
        "Genos - Raval Ore x640 Chest",
        "Genos - Raval Armor Chest",
        "Genos - Raval Ore x960 Chest",
        "Genos - Pot by Square Hole",
        "Genos - Defeat Garland",
        #"Genos - Defeat Galbanan",
    ]

    for name in shrine_locations:
        shrine.locations.append(Location(player, name, location_name_to_id[name], shrine))      


    # ======================
    # Region Connections
    # ======================

    rules = {
        "ignis":            lambda state: (state.has("Ignis Bracelet", player) or state.has("Progressive Ignis", player)),
        "ventus":           lambda state: (state.has("Ventus Bracelet", player) or state.has("Progressive Ventus", player)),
        "ventus2":          lambda state: (state.has("Ventus Bracelet", player) and state.has("Emerald", player, 1)),
        "terra":            lambda state: (state.has("Terra Bracelet", player) or state.has("Progressive Terra", player)),
        "storehouse_key":   lambda state: (state.has("Storehouse Key", player) or state.has("Keyring", player)),
        "ruins_key":        lambda state: (state.has("Ruins Key", player) or state.has("Keyring", player)),
        "clock_key":        lambda state: (state.has("Clock Tower Key", player) or state.has("Keyring", player)),
        "ventus_ignis":     lambda state: (state.has("Ventus Bracelet", player) or state.has("Progressive Ventus", player)) and (state.has("Ignis Bracelet", player) or state.has("Progressive Ignis", player)),
        "ventus_or_ignis":  lambda state: (state.has("Ventus Bracelet", player) or state.has("Progressive Ventus", player)) or (state.has("Ignis Bracelet", player) or state.has("Progressive Ignis", player)),
        "terra_or_ignis":   lambda state: (state.has("Terra Bracelet", player) or state.has("Progressive Terra", player)) or (state.has("Ignis Bracelet", player) or state.has("Progressive Ignis", player)),
        "terra_jump":       lambda state: (state.has("Terra Bracelet", player) and state.has("Topaz", player)) or (state.has("Progressive Terra", player, 2)),
        "terra_jump2":      lambda state: (state.has("Terra Bracelet", player) and state.has("Topaz", player, 2)) or (state.has("Progressive Terra", player, 3)),
        "doublejump":       lambda state: state.has("Double Jump", player),
        "nightfire_gem":    lambda state: state.has("Nightfire Gem", player),
        "bob":              lambda state: state.has("Bob's Pendant", player),
        "berm":             lambda state: state.has("Berm Leaves", player),
        "jade":             lambda state: state.has("Jade Ring", player),
        "lotus":            lambda state: state.has("Lotus Hammer", player),
        "pipe":             lambda state: state.has("Organ Pipe", player),
        "cross":            lambda state: state.has("Holy Cross", player),
        "ivory":            lambda state: state.has("Ivory Key", player),
        "firewyrm":         lambda state: state.has("Firewyrm's Amulet", player),
        "stoneshoes":       lambda state: state.has("Stone Shoes", player),
        "dash":             lambda state: state.has("Dash", player),
        "dash_or_ventus":   lambda state: state.has("Dash", player) or (state.has("Ventus Bracelet", player) or state.has("Progressive Ventus", player)),
        "dash_doublejump":  lambda state: state.has("Dash", player) and state.has("Double Jump", player),
        "all_statues":      lambda state: state.has("Moonstar Statue", player) and state.has("Sunset Statue", player) and state.has("Darkness Statue", player) and state.has("Light Statue", player),
        "all_organ":        lambda state: state.has("Organ Pipe", player) and state.has("Ivory Key", player) and state.has("Holy Cross", player),
        "prog_sword1":      lambda state: state.has("Progressive Sword", player, 1),
        "prog_sword2":      lambda state: state.has("Progressive Sword", player, 2),
        "prog_sword3":      lambda state: state.has("Progressive Sword", player, 3),
        "prog_sword4":      lambda state: state.has("Progressive Sword", player, 4),
        "prog_sword5":      lambda state: state.has("Progressive Sword", player, 5),
        "chester1":         lambda state: state.has("Defeated Chester 1", player),
        "gyalva":         lambda state: state.has("Defeated Gyalva", player),
        "faleon":           lambda state: state.has("Defeated Faleon", player),
        "gold":             lambda state: state.has("Gold x10000", player, 7),
        "gold2":            lambda state: state.has("Gold x15000", player, 3),

    }

    def illburn_right_rule(state):
        has_ventus = rules["ventus"](state)
        has_ignis  = rules["ignis"](state)
        has_doublejump     = rules["doublejump"](state)
        print(f"[DEBUG] Illburn Right check → Ventus:{has_ventus}  Ignis:{has_ignis}  DJ:{has_doublejump}")
        return has_ventus or has_ignis or has_doublejump

    location_rules = {
        ## Redmont + Quarry ## 
        "Redmont - Buy Banded Slayer":      rules["gold"],       #Same flags as the items #24000 Gold
        "Redmont - Buy Banded Shield":      rules["gold"],      #Same flags as the items #16000 Gold
        "Redmont - Buy Banded Mail":        rules["gold"],    #Same flags as the items #18000 Gold
        "Redmont - Buy Katol Elixir":       rules["gold"],      #Same flags as the items #10000 Gold
        "Redmont - Buy Spirit Necklace":    rules["gold2"],       #Same flags as the items #60000 Gold


        "Redmont - Return Bob's Pendant": rules["bob"],
        "Redmont - Give Hugo a Berm Leaves": rules["berm"],
        #"Redmont - Give Randolph the Jade Ring": rules["jade"],
        #"Redmont - Sell the Jade Ring to Cynthia": rules["jade"],
        #"Redmont - Give Adonis the Lotus Hammer": rules["lotus"],

        "Quarry - Bob's Pendant":           lambda state: rules["ventus"](state) or
                                                             rules["doublejump"](state), 
        "Quarry - Pot Bob's Pendant":         lambda state: rules["ventus"](state) or
                                                             rules["doublejump"](state),                                                       
        "Quarry - Pot Main Room Double Jump": rules["doublejump"],
        #"Quarry - Open Storehouse Door": rules["storehouse_key"],
        "Quarry - Defeat Dularn": rules["storehouse_key"],
        "Quarry - Ignis Bracelet Chest": rules["storehouse_key"],
        "Quarry - Defeat Ellefale": rules["ignis"],
        "Quarry - Torch Ruby Chest": rules["ignis"],
        
        "Quarry - Raval Ore x8 Chest": lambda state: (rules["ventus"](state) or
                                                      rules["doublejump"](state) or
                                                      rules["terra_jump"](state)),

        ## Illburn + Lava ## 
        "Illburn - Raval Ore x20 Chest": lambda state: (rules["ventus_ignis"](state)
                                                   or rules["doublejump"](state)
                                                   or rules["terra_jump2"](state)),
        "Illburn - Pot Upper Room": lambda state: rules["ventus_ignis"](state)
                                                   or rules["doublejump"](state)
                                                   or (rules["terra_jump2"](state) and rules["ignis"](state)),
        "Illburn - Raval Ore x8 Chest": rules["ignis"],
        "Illburn - Spirit Cape Chest": rules["terra"],

        "Lava - Raval Ore x200 Chest": rules["terra"],
        "Lava - Pot Behind Rock Wall": rules["terra"],
        "Lava - Emerald Chest": rules["ventus"],
        "Lava - Pot Ledge": rules["doublejump"],
        "Lava - Katol Elixir Chest": rules["doublejump"],
        "Lava - Defeat Guilen": lambda state: (rules["ventus"](state) and
                                               rules["firewyrm"](state) and
                                               rules["prog_sword2"](state)),
        "Lava - Pot Right": lambda state: (rules["ventus"](state) or
                                            rules["doublejump"](state) or
                                            rules["ignis"](state)),
        "Lava - Raval Ore x12 Chest": rules["gyalva"],
        "Lava - Defeat Gyalva": rules["prog_sword2"],

        ## Mine ## 
        "Mine - Pot First Shaft Right Room": lambda state: rules["ventus"](state) or
                                                            rules["dash_doublejump"](state),    #ventus, dash + doublejump, 
        "Mine - Raval Ore x50 Chest": lambda state: rules["ventus"](state) or
                                                     rules["dash_doublejump"](state), 				
        "Mine - Emerald Chest": lambda state: (rules["ventus"](state) and
                                                     rules["dash_doublejump"](state)) or
                                                     (rules["ventus2"](state)), 	#ventus charge
        "Mine - Katol Elixir Chest": lambda state: (rules["ventus"](state) or
                                                     rules["dash_doublejump"](state)),
        "Mine - Raval Ore x65 Chest": lambda state: rules["ventus"](state) and
                                                     rules["doublejump"](state), 
        "Mine - Raval Ore x200 Chest": lambda state: (rules["ventus"](state) and
                                                     rules["doublejump"](state) and
                                                     rules["terra"](state)),       
        "Mine - Pot behind Rock": lambda state: (rules["ventus"](state) and
                                                     rules["doublejump"](state) and
                                                     rules["terra"](state)),
        "Mine - Defeat Istersiva": lambda state: rules["ventus"](state) and
                                                     rules["doublejump"](state) and
                                                     rules["prog_sword2"](state),

        "Cave - Defeat Gildias":   rules["prog_sword3"],
        "Dungeon - Defeat Zirduros": rules["prog_sword4"],
        "Castle - Defeat Chester": rules["prog_sword3"],

        ## Mountain + Cave ## 
        "Mountain - Berm Leaves 3": rules["terra_or_ignis"],
        "Mountain - Katol Elixir Chest": rules["dash_or_ventus"],

        "Castle - Raval Ore x200 Chest": lambda state: rules["doublejump"](state) or
                                        	rules["ventus"](state) or
                                            rules["terra"](state),
        "Castle - Pot Parkour Room":    lambda state: (rules["ventus"](state) or
                                                       rules["doublejump"](state) or
                                                        rules["dash"](state)),
        "Castle - Pot Room Top of West Tower": lambda state: rules["doublejump"](state) or
                                        	             rules["ventus"](state),
        "Castle - Pot Under Parkour 1": lambda state: rules["doublejump"](state) or
                                                        rules["ventus"](state),
        "Castle - Pot Under Parkour 2": lambda state: rules["doublejump"](state) or
                                                        rules["ventus"](state),
        "Castle - Battle Armor Chest":  lambda state: rules["doublejump"](state) or
                                                        rules["ventus"](state),
        "Castle - Raval Ore x500 Chest": lambda state: (rules["doublejump"](state) and rules["ventus"](state)) or (rules["ventus2"](state)),
        "Castle - Defeat Faleon":       lambda state: (rules["doublejump"](state) or
                                                        rules["ventus"](state) or
                                                        rules["dash"](state))
                                                        and
                                                        (rules["ignis"](state) and
                                                         rules["ventus"](state) and
                                                         rules["terra"](state) and
                                                         rules["prog_sword3"](state)),
        "Castle - Topaz Chest": rules["doublejump"],
        "Castle - Pot Top Of East Tower":   lambda state: rules["doublejump"](state) or
                                                        rules["ventus"](state) or
                                                        rules["terra_jump"](state),
        "Castle - Raval Ore x250 Chest":    lambda state: rules["dash_doublejump"](state) and
                                                        rules["ventus"](state),
        "Castle - Raval Ore x320 Chest":    lambda state: rules["doublejump"](state) and
                                                        rules["terra"](state),
        "Castle - Place Organ Pipe": rules["pipe"],    
        "Castle - Place Holy Cross": rules["cross"],    
        "Castle - Place Ivory Key": rules["ivory"],      
        "Castle - Pot Boulder Room 1": rules["stoneshoes"],		
        "Castle - Pot Boulder Room 2": rules["stoneshoes"],			
        "Castle - Pot Lava Room":           lambda state: rules["doublejump"](state) or
                                                        rules["ventus"](state),
        "Castle - Battle Shield Chest":     lambda state: (rules["doublejump"](state) and rules["terra"](state)) or
                                                          (rules["ventus"](state) and rules["terra"](state)),
        "Castle - Raval Ore x380 Chest":  rules["nightfire_gem"],
        "Castle - Defeat Zellfel":	lambda state: rules["nightfire_gem"](state) and rules["prog_sword4"](state),

        "Dungeon - Pot First Room Left": lambda state: rules["doublejump"](state) or rules["ventus"](state),        #doublejump, ventus,
        "Dungeon - Pot Jump Area":       lambda state: rules["doublejump"](state) or rules["ventus"](state),              #doublejump, ventus,
        "Dungeon - Battle Saber Chest":  lambda state: (rules["ventus"](state)) or
                                                        (rules["doublejump"](state) and rules["terra_jump"](state)),         #ventus, #doublejump + terra_jump1
        "Dungeon - Pot First Room Stairs":  lambda state: (rules["ventus"](state)) or
                                                        (rules["doublejump"](state) and rules["terra_jump"](state)), 

        #"Clock - Open Clock Tower Door": rules["clock_key"],       #clock_key
        "Clock - Ruby Chest":               lambda state: (rules["doublejump"](state) and rules["clock_key"](state) and rules["ventus"](state)) or
                                                    (rules["clock_key"](state) and rules["doublejump"](state) and rules["ignis"](state)),

        "Genos - Defeat Garland": lambda state:  (rules["prog_sword5"](state) and
                                                  rules["terra"](state) and
                                                  rules["ignis"](state)), #Ignis is actually for Galbalan
        #"Genos - Defeat Galbanan":     rules["ignis"],
        # Add more location rules here later
    }  

    for region in [redmont, quarry, illburn, illburn_right, lava, lava_lava, lava_right, mine, mine_deep, mountain, mountain_right, cave, cave_ice, castle, castle_west, dungeon, clock, genos, shrine]:
        for location in region.locations:
            if location.name in location_rules:
                location.access_rule = location_rules[location.name]

    menu.connect(redmont)

    redmont.connect(quarry)
    quarry.connect(mine, rule=rules["nightfire_gem"])
    mine.connect(mine_deep, rule=rules["doublejump"])

    redmont.connect(illburn, rule=rules["ruins_key"])
    illburn.connect(illburn_right, rule=illburn_right_rule)
    illburn_right.connect(lava, rule=rules["prog_sword1"])
    lava.connect(lava_lava, rule=rules["firewyrm"])
    lava.connect(lava_right, lambda state: (rules["ventus"](state) or
                                            rules["doublejump"](state)))
    
    redmont.connect(mountain, rule=rules["doublejump"])
    mountain.connect(mountain_right, rule=rules["prog_sword3"])
    mountain_right.connect(cave, rule=rules["terra"])
    cave.connect(cave_ice, rule=rules["stoneshoes"])

    redmont.connect(castle, rule=lambda state: has_enough_statues(state, player, statues_required))
    castle.connect(dungeon, rule=lambda state: rules["all_organ"](state) or open_dungeon == 0)
    castle.connect(castle_west, rule=rules["faleon"])
    dungeon.connect(clock, rule=lambda state: (rules["clock_key"](state) and
                                                    rules["ignis"](state) and
                                                    rules["doublejump"](state)))
    
    redmont.connect(genos, rule=lambda state: has_enough_bosses(state, player, bosses_required))
    genos.connect(shrine, rule=lambda state: (rules["doublejump"](state)
                                               and rules["ventus"](state)))

    # ======================
    # Register regions
    # ======================

    world.regions += [menu, redmont, quarry, illburn, illburn_right, lava, lava_lava, lava_right, mine, mine_deep, mountain, mountain_right, cave, cave_ice, castle, castle_west, dungeon, clock, genos, shrine]
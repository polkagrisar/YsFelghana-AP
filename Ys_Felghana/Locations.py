from BaseClasses import Location


# Item ID starting point (you can change this later)
BASE_ID = 86000

location_names = [

    ### Redmont ###
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

    ### Tigray Quarry ###
    "Quarry - Raval Ore x5 Chest",
    "Quarry - Raval Ore x8 Chest",
    #"Quarry - Open Storehouse Door",
    "Quarry - Defeat Dularn",
    "Quarry - Ignis Bracelet Chest",
    "Quarry - Defeat Ellefale",
    #"Quarry - Moonstar Statue",
    "Quarry - Torch Ruby Chest",
    "Quarry - Pot Above Stairs",
    "Quarry - Pot Under Stairs",
    "Quarry - Pot Room After Dewey",
    "Quarry - Pot Outside Ellefale",
    "Quarry - Bob's Pendant",
    "Quarry - Pot Bob's Pendant",
    "Quarry - Pot Outside Mine",
    "Quarry - Pot Main Room Double Jump",

    ### Illburn Ruins ###
    #"Illburn - Open Ruin Gate",
    "Illburn - Small Shield Chest",
    "Illburn - Raval Ore x6 Chest",
    "Illburn - Raval Ore x12 Chest",
    "Illburn - Katol Elixir Chest",
    "Illburn - Ruby Chest",
    "Illburn - Raval Ore x8 Chest",
    "Illburn - Spirit Cape Chest",
    "Illburn - Raval Ore x20 Chest",
    "Illburn - Pot Early Left",
    "Illburn - Pot Upper Room",
    "Illburn - Pot Right",
    "Illburn - Pot Katol Elixir Room",
    "Illburn - Pot End",
    "Illburn - Pot End Up",
    "Illburn - Pot End Down 1",
    "Illburn - Pot End Down 2",
    "Illburn - Defeat Chester",

    ### Zone of Lava ###
    "Lava - Raval Ore x18 Chest",
    "Lava - Pot Above Chasm",
    "Lava - Pot In Chasm",
    "Lava - Pot Mozgouz Room",
    "Lava - Pot Behind Rock Wall",
    "Lava - Firewyrm's Amulet Chest",
    "Lava - Broadsword Chest",
    "Lava - Raval Ore x200 Chest",
    "Lava - Pot Right",
    "Lava - Pot Cliff Decend Top",
    "Lava - Pot Cliff Descend Bottom",
    "Lava - Emerald Chest",
    "Lava - Pot Ledge",
    "Lava - Katol Elixir Chest",
    "Lava - Defeat Guilen",
    "Lava - Defeat Gyalva",
    "Lava - Raval Ore x12 Chest",

    ### Abandoned Mine ###
    "Mine - Pot First Shaft Top",
    "Mine - Pot First Shaft Right Room",    #ventus, dash + doublejump, 
    "Mine - Raval Ore x50 Chest", #ventus, dash + doublejump, 		
    "Mine - Pot First Shaft Bottom",
    "Mine - Pot Top of Stairs",
    "Mine - Raval Ore x25 Chest",		
    "Mine - Emerald Chest", #ventus+dash+doublejump
    "Mine - Pot Behind Bottom Stairs",
    "Mine - Pot Cliff Ledge", #doublejump
    "Mine - Raval Ore x40 Chest", #doublejump
    "Mine - Katol Elixir Chest", #ventus, dash+doublejump

    "Mine - Raval Ore x65 Chest", #ventus+doublejump
    "Mine - Raval Ore x200 Chest", #ventus + doublejump + terra        
    "Mine - Pot behind Rock",	#ventus + doublejump + terra
    "Mine - Defeat Istersiva", #ventus + doublejump

    ### Elderm Mountains ###
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

    ### Icebound Cave ###
    "Cave - Topaz Chest",
    "Cave - Stone Shoes Chest",

    "Cave - Pot Ice Platform",
    "Cave - Raval Ore x140 Chest",
    "Cave - Pot 1 Past Shoes",
    "Cave - Pot 2 Past Shoes",
    "Cave - Raval Ore x120 Chest",
    "Cave - Raval Ore x140 Chest 2",
    "Cave - Pot Behind Ice",
    "Cave - Katol Elixir Chest",
    "Cave - Defeat Gildias",

    ### Valestein Castle ###
    "Castle - Raval Ore x200 Chest",	        #doublejump, ventus
    "Castle - Pot Parkour Room",	#ventus, doublejump, dash
    "Castle - Pot Under Parkour 1",	#doublejump, ventus
    "Castle - Pot Under Parkour 2",	#doublejump, ventus 
    "Castle - Battle Armor Chest",	#doublejump, ventus
    "Castle - Raval Ore x500 Chest",
    "Castle - Pot Room Top of West Tower",
    "Castle - Defeat Faleon",	    #doublejump, ventus, dash
    "Castle - Topaz Chest",	            #doublejump
    "Castle - Pot Top Of East Tower",   #doublejump, ventus
    "Castle - Raval Ore x250 Chest",    #dash_double + ventus
    "Castle - Raval Ore x320 Chest",    #terra + doublejump
    "Castle - Place Organ Pipe",        #Need Organ Pipe
    "Castle - Place Holy Cross",        #Need Holy Cross
    "Castle - Place Ivory Key",         #Need Ivory Key
    "Castle - Pot Boulder Room 1",		#stoneshoes
    "Castle - Pot Boulder Room 2",		#stoneshoes
    "Castle - Pot Lava Room",			#doublejump, ventus
    "Castle - Battle Shield Chest",		#doublejump + terra, ventus + terra
    "Castle - Raval Ore x380 Chest",	#Nightgem
    "Castle - Defeat Zellfel",			#Nightgem

    ### Castle Dungeon ###
    "Dungeon - Pot First Room Left",        #doublejump, ventus,
    "Dungeon - Pot Jump Area",              #doublejump, ventus,
    "Dungeon - Battle Saber Chest",         #ventus, #doublejump + terra_jump1
    "Dungeon - Pot First Room Stairs",      #ventus, #doublejump + terra_jump1
    "Dungeon - Defeat Zirduros",
    #"Clock - Open Clock Tower Door",       #clock_key
    "Clock - Ruby Chest",                   #doublejump + clock_key + ventus, clock_key + doublejump + ignis

    ### Clock Tower ###
    "Clock - Raval Ore x350 Chest",
    "Clock - Pot Sunset Room",
    "Clock - Pot Darkness Room",
    "Clock - Pot Light Room",
    "Clock - Pot Room After Climb",
    "Castle - Defeat Chester",

    ### Genos Island ###
    "Genos - Defeat Dularn",
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

location_name_to_id = {name: BASE_ID + i for i, name in enumerate(location_names)}
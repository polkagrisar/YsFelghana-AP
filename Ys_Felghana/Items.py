from BaseClasses import Item, ItemClassification

# Item ID starting point (you can change this later)
BASE_ID = 85000

item_table = {
    # Bracelets
    "Ignis Bracelet":        ItemClassification.progression,
    "Ventus Bracelet":       ItemClassification.progression,
    "Terra Bracelet":        ItemClassification.progression,

    "Progressive Ignis":     ItemClassification.progression,
    "Progressive Ventus":    ItemClassification.progression,
    "Progressive Terra":     ItemClassification.progression,

    ### Progressive Items ###
    "Progressive Sword":     ItemClassification.progression,
    "Progressive Armor":     ItemClassification.useful,
    "Progressive Shield":    ItemClassification.useful,

    "Ruby":                  ItemClassification.useful,
    "Emerald":               ItemClassification.useful,
    "Topaz":                 ItemClassification.progression,

    ### Accessoaries ###
    "Firewyrm's Amulet":     ItemClassification.progression,
    "Nightfire Gem":         ItemClassification.progression,
    "Stone Shoes":           ItemClassification.progression,
    "Spirit Cape":           ItemClassification.useful,
    "Silver Chimes":         ItemClassification.useful,
    "Spirit Necklace":       ItemClassification.useful,

    ### Inventory Items ###
    "Map of Felghana":       ItemClassification.useful, #Start With
    "Wing Talisman":         ItemClassification.useful, #Start With
    "Illusion Mirror":       ItemClassification.useful,
    "Amulet":                ItemClassification.useful,

    "Katol Elixir":          ItemClassification.useful,
    "Brocia Serum":          ItemClassification.progression,
    "Berm Leaves":           ItemClassification.progression,
    "Bob's Pendant":         ItemClassification.progression, #Original Location, not randomized

    "Silver Pendant":        ItemClassification.useful,
    "Storehouse Key":        ItemClassification.progression,
    "Ruins Key":             ItemClassification.progression,
    "Clock Tower Key":       ItemClassification.progression,

    "Mission Tablet":        ItemClassification.progression,
    "Organ Pipe":            ItemClassification.progression,
    "Ivory Key":             ItemClassification.progression,
    "Holy Cross":            ItemClassification.progression,

    "Jade Ring":             ItemClassification.progression,
    "Talisman of War":       ItemClassification.useful,
    "Augite Brooch":         ItemClassification.useful,
    "Lotus Hammer":          ItemClassification.useful,

    "Moonstar Statue":       ItemClassification.progression,
    "Sunset Statue":         ItemClassification.progression,
    "Darkness Statue":       ItemClassification.progression,
    "Light Statue":          ItemClassification.progression,

    "Keyring":               ItemClassification.progression,

    #Abilities
    "Double Jump":           ItemClassification.progression,
    "Dash":                  ItemClassification.progression,

    #"Useful" filler
    "XP x50000":             ItemClassification.useful,
    "XP x25000":             ItemClassification.useful,
    "Raval Ore x2000":       ItemClassification.useful,
    "Gold x15000":           ItemClassification.progression,
    "Gold x10000":           ItemClassification.progression,

    # ======================
    # Filler
    # ======================
    "Raval Ore x200":        ItemClassification.filler,
    "XP x5000":              ItemClassification.filler,
    "Gold x5000":            ItemClassification.filler,

    # ======================
    # Traps
    # ======================
    "Armless Trap":         ItemClassification.trap,
    "Slippery Trap":        ItemClassification.trap,
}

# Create the name → ID mapping
item_name_to_id = {name: BASE_ID + i for i, name in enumerate(item_table)}
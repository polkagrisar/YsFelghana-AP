# Ys: The Oath in Felghana - Archipelago

Archipelago randomizer world for *Ys: The Oath in Felghana*.

I've found the world to be very stable, without any crashes or softlocks.
The problems that it do have is a bit wonky Store locations, and some of the logic chains in Valestein Castle.

## AI USAGE ##
This randomizer does use vibe coding, by Grok, and by Gemini.\
Some things have been integrated without too much editing, so it wouldn't be completely unfair to call some of it Ai generated.\
Specifically the archipelago library integration with the client is something I personally didn't understand that much about, and that is all made by the Ai.\
All the memory addresses, flags and things have been manually found in Cheat Engine, no Ai has been used for that (except teaching me the program).

I have learnt a lot about Python, pymem, Cheat Engine and more, so hopefully my next apworld will use much less Ai.\
I also contemplated to not even post this apworld, since it is made possible by Ai, but I wanted to share it anyways, especially since I have gotten to enjoy many other peoples apworlds.

## Locations (151) ##
1. Shop Items
2. All Chests
3. All Pots
4. Giving Berm Leaves to Hugo, giving Bob's Pendant
5. Defeating the Bosses

Note: I have added all the chests and pots manually, and I keep finding new ones. Feel free to tell me if you found something I've missed.

Nothing is missable and nothing can become softlocked, but some shop-items might automatically send themselves in the store.\
Logic is all working and done, but the Castle might be a bit wonky, or not very noob friendly.\
Any item given by other NPCs or that is found in the Overworld except Bob's Pendant (i.e Ventus Bracelet, Brocia Serum) are not a location, but those items are randomized into the pool.
   
## Items ##
1. Swords, Shields and Armor are all Progressive, they also auto-equip the best version you have.
2. Bracelets and gemstones are all randomized individually, but can be set to progressive as an option.
3. All accessories, with an option that auto-equips them when needed.
4. All the items.
5. XP, Gold, Raval Ore in various amounts (boring filler)
6. Traps.\
"Armless Trap": You can't attack for a short while.\
"Slippery Trap": The game get Ice-physics for a short while.\
(Feel free to give more ideas for fun traps).

Note: Katol Elixirs, Illusion Mirror and Amulet are currently infinite uses.

## Special Options ##
1. Keyring option: Can add an item that gives all the 3 keys ("Storehouse Key", "Ruins Key", "Clock Tower Key")
2. Choose how many of the 4 statues are needed to access Valestein Castle.
3. Choose how many of the 12 bosses are needed to access Genos Island.
4. Option to auto-equip accessories depending on the room you are in.
5. Brocia Serum rework, can be used to set your level or just give flat-xp.
6. Change % of filler to Traps

## GOAL ##
1. The Goal is sent when defeating Galbalan on Genos Island.

## Requirements ##
- Archipelago 0.6.7+
- Ys: The Oath in Felghana (Steam), [Default Public Version Mar 11, 2020] #Not tested on anything else
- Start it using the DirectX9 version (Just start the game normally, do not choose DirectX8)
- Only tested on Windows 11

## Installation ##
1. Download the latest 'Ys_Felghana.apworld' from the Releases page.
2. Place it in your 'custom_worlds' folder.
3. Download the yaml and edit it as you like, then place it in the 'Players' folder (or generate yaml templates and create you own).

## Client ##
When the apworld is in the custom_worlds folder, The "Ys Felghana Client" will appear in the Archipelago Launcher.

-- How to Use --
1. Launch the Game on steam.
2. Start a New Game, or load a previous save (it does not skip the opening cutscene, but you can prepare a save that already start after it).
3. Start the 'Ys Felghana Client' in the Archipelago Launcher, input the server:port, slot_name and password (if any).
4. The Client should say: "=== Successfully connected to Archipelago! ===".

-- Overlay --\
The client does give an overlay to the game window, that will show you when you recieve items or send locations.
The client does not change any assets in the game, so opening the Ignis Bracelet Chest will still play the vanilla animation (which will be wrong from what is actually sent).

Note: Starting other old saves WILL send out any locations that save has gotten, so don't do that unless you want to mess up the world for everyone, it might also remove items from that save, so do not save over any saves you don't want to mess up

## Quirks and logic specific to this randomizer ##
- Many cutscenes are skipped or removed, there is no escort quest, Dogi does not throw you the Terra Bracelet and you can just walk over the gap.\
  The most noticeable cutscene that remain is the first time you fight Chester and he throws you down to the Lava Zone.
- When in Redmont some of your Equipment might/will disappear, this is because of the way the flags in the store works. Just exit the town and they will all come back, this approach does however sadly prevent you from upgrading some equipment.
- Abandonded Mine will only be accessible when you have the "Nightfire Gem" item.
- Due to the way you get XP as items and the possibility of the Brocia Serum giving XP and levels, there should not be any real grinding in this apworld.
- However, being granted access to hard areas (Elderm Mountain, Valestain Castle) as early sphere's might have you needing to just run and avoid as much as you can.

## Known Issues ##
- The Stone Shoes might not work correctly when auto equipped upon entering a room, if the first surface you touch in that room is ice.
- Don't mind the dead guards outside Redmont, just reset the room (go inside the Town, or away from the Town), they will disappear either way.
- The room where the Ventus Bracelet is in Vanilla: Don't go in there, you might be "softlocked" from the lava chase, just use the Wing Talisman if this happens (The Ventus location is not a location in this AP).
- The Boss "Guilen" (boss by the Vanilla Ventus Bracelet) will spawn if you walk to the start of the corridor towards Vanilla Ventus Bracelet (You must have Ventus Bracelet unlocked).
- The Armless Trap also make it so you keep healing to full health.

## Credits
- Created by polkagrisar

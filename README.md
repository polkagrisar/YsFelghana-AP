# Ys: The Oath in Felghana - Archipelago

Archipelago randomizer world for *Ys: The Oath in Felghana*.

## AI USAGE ##
This randomizer does use vibe coding, mostly by Grok, but also a bit from Gemini.
Some things have been integrated from Grok without much editing, so it wouldn't be completely unfair to call it Ai generated.
Specifically the archipelago library integration with the client is something I personally don't understand that much about, and that is all made by the Ai.
All the memory addresses, flags and things have been manually found in Cheat Engine, no Ai has been used for that (except teaching me the program).

I have learnt a lot about Python, pymem, Cheat Engine and more, so hopefully my next apworld will use much less Ai.
I also contemplated to not even post this apworld, since it is made by Ai, but I wanted to share it anyways, especially since I have gotten to enjoy many other peoples apworlds.

## Features ##
- Location randomization 
1. Shop Items
2. Chests
3. Pots
4. Giving items to people (not receiving items)
5. Opening Doors
6. Defeating Bosses
   
- Items and Equipment
1. Swords, Shields, Armor, Bracelets
2. All accessories and items.

- Special Options
1. Keyring option (Customizable)
2. Statue and boss requirements
3. Auto-equip options
4. Client with memory integration
* Everything is done using pymem, there is no .dll or similar hooks.

  - GOAL
1. The Goal is on defeating Galbalan on Genos Island.

* The game does not actually show any messages and does not change any sprites or anything, all information of what you send or get is in the Client only.

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

* Starting other old saves WILL send out any locations that save has gotten, so don't do that unless you want to mess up the world for everyone, it might also remove items from that save, so do not save over any saves you don't want to mess up *

## Quirks specific to this randomizer ##
- When in Redmont some of your Equipment might/will disappear, this is because of the way the flags in the store works. Just exit the town and they will all come back.
- Abandoned Mine is only open when you have the Nightfire Gem item.
- Valestein Castle open when you have 0-4 of the Statues.
- Genos Island is accessible when you have defeated 0-12 of all the bosses (that's not on Genos Island).

## Known Issues ##
- The Stone Shoes might not work correctly when auto equipped upon entering a room, if the first surface you touch in that room is ice.

## Credits
- Created by polkagrisar

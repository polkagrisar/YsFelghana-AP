import asyncio
from typing import Optional, Set
import re
import tkinter as tk
from tkinter import font as tkfont
import colorama
import queue
import threading
import time
import win32gui

from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, server_loop
from NetUtils import ClientStatus

from .memory import YsMemory
from .Locations import location_name_to_id

class NotificationOverlay:
    """Displays semi-transparent overlay popups positioned over the game window."""
    def __init__(self, root: tk.Tk, window_title: str = "Ys: The Oath in Felghana"):
        self.root = root
        self.window_title = window_title
        self.queue = queue.Queue()
        self.active_popups = []  # Keeps track of active popup windows for stacking
        self.persistent_popups = {}  # Active persistent popups keyed by name
        self.root.after(100, self._process_queue)

    def set_persistent(self, name: str, text: str, show: bool, category: str = "received"):
        """
        Shows or hides a persistent popup based on a condition boolean (`show`).
        `name` is a unique identifier (e.g. 'dash_indicator').
        """
        def _update():
            if show and name not in self.persistent_popups:
                popup = self._create_popup_window(text, category)
                self.persistent_popups[name] = popup
            elif not show and name in self.persistent_popups:
                popup = self.persistent_popups.pop(name)
                popup.destroy()

        self.root.after(0, _update)

    def show(self, text: str, category: str = "received", duration_ms: int = 3500):
        """
        Thread-safe method to queue notification popups.
        category: 'received' or 'sent'
        """
        self.queue.put((text, category, duration_ms))

    def _process_queue(self):
        try:
            while not self.queue.empty():
                text, category, duration = self.queue.get_nowait()
                self._create_popup(text, category, duration)
        finally:
            self.root.after(100, self._process_queue)

    def _get_game_rect(self):
        """Finds the bounding box (left, top, right, bottom) of the game window."""
        hwnd = win32gui.FindWindow(None, self.window_title)
        if hwnd:
            return win32gui.GetWindowRect(hwnd)
        return None

    def _create_popup_window(self, text: str, category: str):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)      # Remove window frame & borders
        popup.wm_attributes("-topmost", True)  # Keep above game screen
        
        popup.configure(bg="#1e1e1e")
        popup.wm_attributes("-alpha", 0.85)

        # Style colors based on event type
        border_color = "#00FFCC" if category == "received" else "#FFCC00"

        label = tk.Label(
            popup, 
            text=text, 
            font=("Consolas", 11, "bold"), 
            fg=border_color, 
            bg="#1e1e1e",
            padx=12, 
            pady=6,
            relief="ridge",
            bd=2
        )
        label.pack()

        popup.update_idletasks()
        popup_width = popup.winfo_reqwidth()

        game_rect = self._get_game_rect()

        if game_rect:
            left, top, right, bottom = game_rect
            game_width = right - left

            if category == "sent":
                x = left + (game_width // 2) - (popup_width // 2)
                y = top + 35
            elif category == "doublejump":
                x = right - 180
                y = top + 35
            elif category == "dash":
                x = right - 180
                y = top + 50
            elif category == "bossinfo":
                x = left + (game_width // 2) - (popup_width // 2)
                y = bottom - 165
            elif category == "armtrap":
                x = left + (game_width // 2) - (popup_width // 2)
                y = bottom - 180
            elif category == "slipperytrap":
                x = left + (game_width // 2) - (popup_width // 2)
                y = bottom - 165
            else:  # Handles "received" or any default fallback
                x = left + 35
                y = top + 35
        else:
            screen_width = popup.winfo_screenwidth()
            x = (screen_width // 2) - (popup_width // 2) if category == "sent" else 35
            y = 50

        # Offset y based on persistent popups as well as active stacked notifications
        stack_offset = (len(self.persistent_popups) + len(self.active_popups)) * 40
        y += stack_offset

        popup.geometry(f"+{x}+{y}")
        return popup

    def _create_popup(self, text: str, category: str, duration_ms: int):
        popup = self._create_popup_window(text, category)
        popup_height = popup.winfo_reqheight()

        popup_info = {"window": popup, "category": category, "height": popup_height}
        self.active_popups.append(popup_info)

        def _destroy():
            if popup_info in self.active_popups:
                self.active_popups.remove(popup_info)
            popup.destroy()

        popup.after(duration_ms, _destroy)

class YsFelghanaCommandProcessor(ClientCommandProcessor):
    def _cmd_test(self):
        print("Ys Felghana Client is working!")


class YsFelghanaContext(CommonContext):
    game = "Ys Felghana"
    command_processor = YsFelghanaCommandProcessor
    items_handling = 0b111

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.memory: YsMemory | None = None
        self.sent_locations: Set[int] = set()  # Track already sent locations
        self.overlay: Optional[NotificationOverlay] = None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            print("=== Successfully connected to Archipelago! ===")

            slot_data = args.get("slot_data", {})

            self.statue_placement = slot_data.get("statue_placement", 0)
            self.statues_required = slot_data.get("statues_required", 2)
            self.bosses_required = slot_data.get("bosses_required", 2)
            self.keyring_item = slot_data.get("keyring_item", 0)
            self.auto_item = slot_data.get("auto_item", 1)
            self.brocia_serum_change = slot_data.get("brocia_serum_change", 0)
            self.sword_anywhere = slot_data.get("sword_anywhere", 0)

            missing_locs = [loc_id for loc_id in location_name_to_id.values() if loc_id not in self.sent_locations]
            if missing_locs:
                asyncio.create_task(
                    self.send_msgs([{"cmd": "LocationScouts", "locations": missing_locs, "create_as_hint": 0}])
                )

            # Locations already checked on the server (reconnect-safe)
            raw = args.get("checked_locations", [])
            if isinstance(raw, (list, set, tuple)):
                self.sent_locations = set(raw)
            else:
                self.sent_locations = set()

            try:
                self.memory = YsMemory(
                    statues_required=self.statues_required,
                    bosses_required=self.bosses_required,
                    brocia_serum_change=self.brocia_serum_change,
                    sword_anywhere=self.sword_anywhere,
                )

                print("Successfully attached to Ys memory!")               

                # Start the unified non-blocking background task
                self.game_loop_task = asyncio.create_task(self.game_watcher_loop())

            except Exception as e:
                print(f"Failed to attach to game memory: {e}")
                self.memory = None

        elif cmd == "LocationInfo":
            if not hasattr(self, "scouted_items_map"):
                self.scouted_items_map = {}

            for item in args.get("locations", []):
                self.scouted_items_map[item.location] = item

        elif cmd == "ReceivedItems":
            if not self.memory:
                print("Memory not connected - cannot give items")
                return

            index = args.get("index", 0)

            # If this batch is part of the initial connection burst, skip consumable currency payouts
            is_reconnect_sync = index < len(self.items_received) - len(args["items"])

            for item in args["items"]:
                item_name = self.item_names.lookup_in_game(item.item)
                player_name = self.player_names.get(item.player, "Unknown")
                if not is_reconnect_sync and hasattr(self, "overlay") and self.overlay:
                    self.overlay.show(f"Received: {item_name} from {player_name}", category="received")
                #print(f"Received: {item_name} (from {player_name})")

                incremental_item_list = {
                    "Ruby", "Emerald", "Topaz",
                    "Berm Leaves", "Katol Elixir",
                    "Illusion Mirror", "Amulet",
                }

                # 1. Handle Raval Ore, XP and Gold dynamically for any location
                raval_amount = 0
                xp_amount = 0
                gold_amount = 0
                trap_duration = 15

                if "Raval Ore" in item_name:
                     # Matches any digits immediately following 'Raval Ore x'
                    match = re.search(r"Raval Ore x(\d+)", item_name)
                    if match:
                        raval_amount = int(match.group(1))
                    #print(f"You will be given {raval_amount} Raval Ore")

                if "XP" in item_name:
                     # Matches any digits immediately following 'XP x'
                    match = re.search(r"XP x(\d+)", item_name)
                    if match:
                        xp_amount = int(match.group(1))
                    #print(f"You will be given {xp_amount} XP")

                if "Gold" in item_name:
                     # Matches any digits immediately following 'Gold Ore x'
                    match = re.search(r"Gold x(\d+)", item_name)
                    if match:
                        gold_amount = int(match.group(1))
                    #print(f"You will be given {gold_amount} Gold")

                try:
                    if item_name == "Progressive Sword":
                        self.memory.give_progressive_sword()
                    elif item_name == "Progressive Shield":
                        self.memory.give_progressive_shield()
                    elif item_name == "Progressive Armor":
                        self.memory.give_progressive_armor()
                    elif item_name == "Progressive Ignis":
                        self.memory.give_progressive_ignis()
                    elif item_name == "Progressive Ventus":
                        self.memory.give_progressive_ventus()
                    elif item_name == "Progressive Terra":
                        self.memory.give_progressive_terra()
                    elif item_name in incremental_item_list:
                        self.memory.give_incremental_item(item_name)
                    elif item_name == "Keyring":
                        self.memory.give_keys()
                    elif xp_amount > 0:
                        self.memory.obtained_xp += xp_amount
                    elif raval_amount > 0:
                        if not is_reconnect_sync:
                            self.memory.add_raval(raval_amount)
                    elif gold_amount > 0:
                        if not is_reconnect_sync:
                            self.memory.add_gold(gold_amount)

                    elif item_name == "Magic Wallet":
                        self.memory.magic_wallet_count += 1

                    #Traps
                    elif item_name == "Armless Trap":
                        if not is_reconnect_sync:
                            self.memory.armless_trap(True)
                            self.memory.active_traps["Armless Trap"] = time.time() + trap_duration
                    elif item_name == "Slippery Trap":
                        if not is_reconnect_sync:
                            self.memory.slippery_trap(True)
                            self.memory.active_traps["Slippery Trap"] = time.time() + trap_duration
                    else:
                        self.memory.give_item(item_name)

                    print(f"→ Successfully gave {item_name}")
                except Exception as e:
                    print(f"Failed to give {item_name}: {e}")

    async def game_watcher_loop(self):
        print("[AP Client] Background watcher loop active.")

        rebuilt = False  # one-time rebuild after leaving title screen

        while not self.exit_event.is_set():
            try:
                if not self.memory:
                    await asyncio.sleep(0.5)
                    continue

                room = self.memory.get_room_id()

                # Title screen / main menu – no save loaded
                if room == 1:
                    print("(START A NEW GAME, OR LOAD A SAVE)")
                    await asyncio.sleep(2.0)
                    continue

                # First time we see a real game room: restore items once
                if not rebuilt and self.items_received:
                    received_names = [
                        self.item_names.lookup_in_game(item.item)
                        for item in self.items_received
                        if not self.item_names.lookup_in_game(item.item).endswith("Trap")
                    ]

                    self.memory.safe_write_int(self.memory.get_item_address("Ruby"), 0)
                    self.memory.safe_write_int(self.memory.get_item_address("Emerald"), 0)
                    self.memory.safe_write_int(self.memory.get_item_address("Topaz"), 0)
                    self.memory.rebuild_from_received(received_names)
                    rebuilt = True
                    print("[AP Client] Initial item rebuild done (in-game).")

                # 1. Send checked locations
                try:
                    await self.check_new_locations()
                except Exception as e:
                    print(f"Error in check_new_locations: {e}")

                checked_names = {
                name for name, loc_id in location_name_to_id.items()
                if loc_id in self.sent_locations
                }
            # ----------------------------------

                # Pass `checked_names` into your story flag handler
                
                # 2. Story flags
                try:
                    self.memory.skip_story_flags(checked_names)
                except Exception as e:
                    print(f"Error in skip_story_flags: {e}")

                # 3. Debt collector
                try:
                    self.memory.debt_collector()
                except Exception as e:
                    print(f"Error in debt_collector: {e}")

                # 4. Unauthorized items
                try:
                    self.memory.remove_unauthorized_items()
                except Exception as e:
                    print(f"Error in remove_unauthorized_items: {e}")

                # New handlers
                try:
                    self.memory.xp_handler()

                except Exception as e:
                    print(f"Error in handlers: {e}")

                # 5. Sync missing items
                try:
                    received_item_names = [
                        self.item_names.lookup_in_game(item.item)
                        for item in self.items_received
                        if not self.item_names.lookup_in_game(item.item).endswith("Trap")
                    ]
                    self.memory.sync_received_items(received_item_names)
                except Exception as e:
                    print(f"Error in restoring old items: {e}")

                #Check traps
                now = time.time()
                expired_traps = []

                for trap_name, end_time in list(self.memory.active_traps.items()):
                    if now >= end_time:
                        expired_traps.append(trap_name)

                for trap_name in expired_traps:
                    del self.memory.active_traps[trap_name]

                    if trap_name == "Armless Trap":
                        self.memory.armless_trap(False)
                        self.memory.safe_write_int("Use Sword Anywhere", 0)

                    if trap_name == "Slippery Trap":
                        self.memory.slippery_trap(False)

                # 6. Goal
                try:
                    await self.check_goal()
                except Exception as e:
                    print(f"Error in checking goal: {e}")

                # 7. Auto equip
                try:
                    if self.auto_item:
                        current = self.memory.get_equipped_accessory()
                        if current not in (21, 23):
                            self.memory.auto_equip_accessory()
                except Exception as e:
                    print(f"Error in auto equip: {e}")

            except Exception as e:
                print(f"Error in watcher loop: {e}")

            if self.overlay:
                # Show popups during the menu if you have doublejump or dash
                menu_open = self.memory.safe_read_int(self.memory.menu_open_address) == 1

                if self.memory.has_item("Double Jump"):
                    self.overlay.set_persistent(
                        name="doublejump_indicator",
                        text="Doublejump",
                        show=menu_open,
                        category="doublejump"
                    )

                if self.memory.has_item("Dash"):
                        self.overlay.set_persistent(
                        name="dash_indicator",
                        text="Dash",
                        show=menu_open,
                        category="dash"
                    )

                # Show information in the menu
                #bosses_killed  = str(self.memory.has_bosses(checked_names))
                #bosses_needed = str(self.bosses_required)
                
                #self.overlay.set_persistent(
                #    name="show_bosses",
                #    text=bosses_killed + " / " + bosses_needed,
                #    show=menu_open,
                #    category="bossinfo"
                #)

                # Show popups if you have a trap active
                is_armless = "Armless Trap" in self.memory.active_traps
                self.overlay.set_persistent(
                    name="armless_trap",
                    text="Armless Trap Active",
                    show=is_armless,
                    category="armtrap"
                )

                is_slippery = "Slippery Trap" in self.memory.active_traps
                self.overlay.set_persistent(
                    name="slippery_trap",
                    text="Slippery Trap Active",
                    show=is_slippery,
                    category="slipperytrap"
                )


            await asyncio.sleep(0.2)

    async def check_goal(self):
        if not self.memory:
            return

        offset = self.memory.story_flags.get("Defeat Galbanan")
        if offset is None:
            return

        addr = self.memory.get_flag_address(offset)
        
        value = self.memory.safe_read_int(addr)
        #print(f"Address = {addr}, Offset = {offset}, Value = {value} ")
        if value == 1:
            if not getattr(self, "goal_sent", False):
                await self.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                self.goal_sent = True
                print("=== GOAL COMPLETED ===")
                if hasattr(self, "overlay"):
                    self.overlay.show("Goal Completed!")


    async def check_new_locations(self):
        try:
            if not isinstance(getattr(self, "sent_locations", None), set):
                self.sent_locations = set()

            checked_names = self.memory.get_checked_locations()
            newly_checked_ids = []

            for name in checked_names:
                if not isinstance(name, str):
                    continue

                loc_id = location_name_to_id.get(name)
                if loc_id is None:
                    continue
                if loc_id in self.sent_locations:
                    continue

                newly_checked_ids.append(loc_id)
                self.sent_locations.add(loc_id)

                self.memory.debt_increase(name)

                # Fetch item info for the location
                item_desc = "Sent Check"
                if hasattr(self, "scouted_items_map") and loc_id in self.scouted_items_map:
                    scouted_item = self.scouted_items_map[loc_id]
                    target_player = self.player_names.get(scouted_item.player, "Unknown")
                    item_name = self.item_names.lookup_in_slot(scouted_item.item, scouted_item.player)
                    item_desc = f"Sent {item_name} to {target_player}"
                else:
                    item_desc = f"Checked: {name}"


                # Trigger popup notification
                if hasattr(self, "overlay") and self.overlay:
                    self.overlay.show(f"{name}\n({item_desc})", category="sent")
                print(f"→ Sending location check: {name} (ID: {loc_id})")

            if newly_checked_ids:
                await self.check_locations(newly_checked_ids)

        except Exception as e:
            import traceback
            print(f"Error while checking locations: {e}")
            traceback.print_exc()  # ← shows exact line


async def main():
    print("=================================")
    print("   Ys Felghana Archipelago Client")
    print("=================================\n")

    server = input("Enter server address (example: localhost:38281): ").strip()
    if not server:
        server = "localhost:38281"

    slot_name = input("Enter your slot name: ").strip()
    if not slot_name:
        print("Slot name is required!")
        input("Press Enter to exit...")
        return

    password = input("Enter password (leave empty if none): ").strip() or None

    print("\nConnecting...\n")

    ctx = YsFelghanaContext(server, password)
    ctx.auth = slot_name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()


class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Archipelago Ys Felghana Client")
        self.root.geometry("680x520")
        self.root.configure(bg="#0F141C")

        self.overlay = NotificationOverlay(self.root)

        self.ctx: YsFelghanaContext | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None

        # --- Top Connection Bar ---
        top_bar = tk.Frame(self.root, bg="#0F141C", pady=6, padx=8)
        top_bar.pack(fill="x")

        # Server
        tk.Label(top_bar, text="Server:", fg="#88A0C0", bg="#0F141C", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 4))
        self.server_var = tk.StringVar(value="localhost:38281")
        self.server_entry = tk.Entry(top_bar, textvariable=self.server_var, bg="#161F2C", fg="#FFFFFF",
                                     insertbackground="white", relief="solid", bd=1, width=22)
        self.server_entry.pack(side="left", padx=(0, 10))

        # Slot
        tk.Label(top_bar, text="Slot:", fg="#88A0C0", bg="#0F141C", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 4))
        self.slot_var = tk.StringVar(value="PolkaYs")
        self.slot_entry = tk.Entry(top_bar, textvariable=self.slot_var, bg="#161F2C", fg="#FFFFFF",
                                   insertbackground="white", relief="solid", bd=1, width=14)
        self.slot_entry.pack(side="left", padx=(0, 10))

        # Password
        tk.Label(top_bar, text="Pass:", fg="#88A0C0", bg="#0F141C", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 4))
        self.pass_var = tk.StringVar()
        self.pass_entry = tk.Entry(top_bar, textvariable=self.pass_var, bg="#161F2C", fg="#FFFFFF",
                                   insertbackground="white", show="*", relief="solid", bd=1, width=10)
        self.pass_entry.pack(side="left", padx=(0, 10))

        # Connect Button
        self.connect_btn = tk.Button(top_bar, text="Connect", command=self._on_connect,
                                     bg="#3A82F6", fg="#FFFFFF", activebackground="#2563EB", activeforeground="#FFFFFF",
                                     relief="flat", font=("Segoe UI", 9, "bold"), padx=10)
        self.connect_btn.pack(side="right")

        # --- Tab Header Bar ---
        tab_bar = tk.Frame(self.root, bg="#182232", height=30)
        tab_bar.pack(fill="x")
        
        ap_tab = tk.Label(tab_bar, text="Archipelago", fg="#60A5FA", bg="#0F141C", 
                         font=("Segoe UI", 9, "bold"), padx=16, pady=4)
        ap_tab.pack(side="left")

        # --- Console Log View ---
        log_frame = tk.Frame(self.root, bg="#0B0F19", bd=1, relief="solid")
        log_frame.pack(fill="both", expand=True, padx=8, pady=(8, 4))

        self.log = tk.Text(log_frame, bg="#0B0F19", fg="#E2E8F0", insertbackground="white",
                           font=("Consolas", 10), wrap="word", state="disabled", bd=0)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log.yview, bg="#161F2C")
        self.log.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True, padx=4, pady=4)

        # Style tags for colored outputs
        self.log.tag_config("notice", foreground="#38BDF8")
        self.log.tag_config("sent", foreground="#FACC15")
        self.log.tag_config("received", foreground="#4ADE80")

        # --- Command Entry Bar ---
        cmd_frame = tk.Frame(self.root, bg="#0F141C", pady=4, padx=8)
        cmd_frame.pack(fill="x")

        cmd_label = tk.Label(cmd_frame, text="Command:", bg="#3A82F6", fg="#FFFFFF", 
                             font=("Segoe UI", 9, "bold"), padx=8, pady=2)
        cmd_label.pack(side="left", padx=(0, 6))

        self.cmd_var = tk.StringVar()
        self.cmd_entry = tk.Entry(cmd_frame, textvariable=self.cmd_var, bg="#161F2C", fg="#FFFFFF",
                                  insertbackground="white", relief="solid", bd=1, font=("Consolas", 10))
        self.cmd_entry.pack(side="left", fill="x", expand=True)
        self.cmd_entry.bind("<Return>", self._on_send_command)

    def write_log(self, text: str):
        def _append():
            self.log.configure(state="normal")
            
            # Highlight categories based on message content
            if text.startswith("→ Sending") or text.startswith("Sent"):
                self.log.insert("end", text + "\n", "sent")
            elif text.startswith("Received") or text.startswith("→ Successfully gave"):
                self.log.insert("end", text + "\n", "received")
            elif text.startswith("[Notice]") or text.startswith("==="):
                self.log.insert("end", text + "\n", "notice")
            else:
                self.log.insert("end", text + "\n")

            self.log.see("end")
            self.log.configure(state="disabled")
        self.root.after(0, _append)

    def _on_send_command(self, event=None):
        cmd_text = self.cmd_var.get().strip()
        if not cmd_text:
            return

        self.write_log(f"> {cmd_text}")
        self.cmd_var.set("")

        if self.ctx and self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self.ctx.send_msgs([{"cmd": "Say", "text": cmd_text}]), self._loop)

    def _on_connect(self):
        server = self.server_var.get().strip() or "localhost:38281"
        slot = self.slot_var.get().strip()
        password = self.pass_var.get().strip() or None

        if not slot:
            self.write_log("Slot name is required.")
            return

        self.connect_btn.configure(state="disabled")
        self.write_log(f"Connecting to {server} as {slot}...")

        self._thread = threading.Thread(
            target=self._run_client,
            args=(server, slot, password),
            daemon=True,
        )
        self._thread.start()

    def _run_client(self, server: str, slot: str, password: str | None):
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._async_main(server, slot, password))
        except Exception as e:
            self.write_log(f"Client error: {e}")
            import traceback
            self.write_log(traceback.format_exc())
        finally:
            self.root.after(0, lambda: self.connect_btn.configure(state="normal"))

    async def _async_main(self, server: str, slot: str, password: str | None):
        self.ctx = YsFelghanaContext(server, password)
        self.ctx.auth = slot
        self.ctx.overlay = self.overlay

        import builtins
        _print = builtins.print

        def gui_print(*args, **kwargs):
            msg = " ".join(str(a) for a in args)
            self.write_log(msg)
            _print(*args, **kwargs)

        builtins.print = gui_print

        self.ctx.server_task = asyncio.create_task(server_loop(self.ctx), name="server loop")
        self.write_log("Connected loop started. Start/load the game if you have not.")
        await self.ctx.exit_event.wait()
        await self.ctx.shutdown()

    def run(self):
        self.root.mainloop()


def launch(*args):
    colorama.init()
    
    # Flatten/convert args tuple into a list for argparse
    arg_list = list(args[0]) if args and isinstance(args[0], (list, tuple)) else list(args)
    
    parser = get_base_parser()
    parsed_args, _ = parser.parse_known_args(arg_list)
    connect_str = parsed_args.connect or "localhost:38281"

    try:
        gui = ClientGUI()
        gui.server_var.set(connect_str)
        gui.run()
    except Exception:
        import traceback
        from pathlib import Path
        Path(r"C:\ProgramData\Archipelago\ys_client_crash.txt").write_text(
            traceback.format_exc(),
            encoding="utf-8",
        )
        raise
        
if __name__ == "__main__":
    launch()
import tkinter as tk
from tkinter import *
from ttkbootstrap import Label
from ttkbootstrap import *
import ttkbootstrap as tb
from store_off import *
from menu import *
from store_tab import StoreTab
from store import *
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from ttkbootstrap import Style


class LibraryTab(tb.Frame):
    def __init__(self, parent, menu):
        super().__init__(parent)
        self.parent = parent

        # Use workbook imported from store_off.py
        owned_games = store_off()
        self.wks = owned_games.wks

        # Instance of store_tab
        self.menu = menu

        # instance of store_off
        owned_games = store_off()
        self.wks = owned_games.wks
        self.all_games = owned_games.get_all_games()

        self.favorite_games = []
        self.recent_games = []

        self.setup_library()

    def load_game_store(self, game_id):
        try:
            # Access the store tab using the menu instance
            store_tab = self.menu.store_tab
            index = self.menu.notebook.index(store_tab)
            self.menu.notebook.select(index)
            store_tab.preview_game(game_id)
        except Exception as e:
            print(f"Error navigating to store page: {e}")

    def setup_library(self):
        self.setup_game_list_layout()

    def setup_game_list_layout(self):

        # Set the grid configuration for the main container
        self.columnconfigure(0, weight=0, minsize=360)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

        # Header
        self.rowconfigure(0, weight=0)
        # TreeView
        self.rowconfigure(1, weight=1)

        # Create a container for the header elements
        header_container = tb.Frame(self)
        header_container.grid(row=0, column=0, sticky="ew", pady=5)
        header_container.columnconfigure(1, weight=1)

        # Frame for the title
        title_frame = tb.Frame(header_container)
        title_frame.grid(row=0, column=0, sticky="w")
        title_label = tb.Label(title_frame, text="My Games", font=("Unispace", "16"))
        title_label.pack(side="left", padx=8)

        # Frame for the search entry
        search_frame = tb.Frame(header_container)
        search_frame.grid(row=0, column=2, sticky="e")
        self.game_search = tb.Entry(search_frame)
        self.game_search.pack(side="right")
        self.game_search.bind("<KeyRelease>", self.on_key_release)

        # Frame for the search icon
        icon_frame = tb.Frame(header_container)
        icon_frame.grid(row=0, column=1, sticky="e")
        self.icon_img = PhotoImage(file="images/search.png")
        icon_label = tb.Label(icon_frame, image=self.icon_img)
        icon_label.pack(side="right", padx=0)

        # Frame for game info (right side)
        info_frame = tb.Frame(self)
        info_frame.columnconfigure(0, weight=1, minsize=500)
        info_frame.rowconfigure(1, weight=0)
        info_frame.grid(row=1, column=2, stick="nsew", padx=3, pady=0)

        self.setup_game_list()
        self.setup_default_info_layout(info_frame)
        self.populate_games()

    def setup_game_list(self):
        style = tb.Style()
        style.configure("Custom.Treeview", font="10", rowheight=25)
        style.configure("CategoryTitle.Treeview", font=("Unispace", 10, "bold"), background="#45484b")

        style.map("Custom.Treeview",
                  background=[("selected", "#8c8cc8")])
        style.map("CategoryTitle.Treeview",
                  background=[("selected", "#45484b"), ("!selected", "#45484b")])

        self.game_list = tb.Treeview(self, show="tree", style="Custom.Treeview")
        self.game_list.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=3)

        # Right click menu
        self.game_list.bind("<Button-3>", self.on_right_click)

        # Action when game from TreeView is selected
        self.game_list.bind("<<TreeviewSelect>>", self.on_game_select)

    def setup_default_info_layout(self, info_frame):
        # Clear contents of game info frame after selection is changed
        self.info_frame = info_frame
        for frame in self.info_frame.winfo_children():
            frame.destroy()

        # Create a label for the section
        recent_games_label = tb.Label(self.info_frame, text="Recent Games", font=("Unispace", 20))
        recent_games_label.grid(row=0, column=0, padx=20, pady=20, sticky="new")

        # Scrollable container for games
        self.games_scrollable_frame = ScrolledFrame(self.info_frame)
        self.games_scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.games_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(1, weight=1)

        self.display_recent_games(self.games_scrollable_frame)

    def display_recent_games(self, scrollable_frame):
        container = scrollable_frame

        # Display only the games in the recent games list
        for index, game_title in enumerate(self.recent_games):
            self.create_recent_widget(container, game_title, index)

        # Update the scrollable frame's canvas and scrollbar
        scrollable_frame.update_idletasks()

    def create_recent_widget(self, container, title, index):
        game_frame = tb.Frame(container)
        game_frame.grid(row=index, column=0, sticky="ew", padx=5, pady=10)
        container.grid_columnconfigure(0, weight=1)

        try:
            photo = Image.open("images/games/pong/banner.png")
            photo = photo.resize((100, 100), Image.Resampling.LANCZOS)
            game_img = ImageTk.PhotoImage(photo)
            img_label = tb.Label(game_frame, image=game_img)
            img_label.image = game_img
            img_label.grid(row=0, column=0, padx=10)
        except Exception as e:
            print(f"Failed to load image: {e}")

        # Game title
        title_label = tb.Label(game_frame, text=title, font=('Helvetica', 16))
        title_label.grid(row=0, column=1, sticky="ew", padx=10)
        game_frame.grid_columnconfigure(1, weight=1)

        # Play button
        play_button = tb.Button(game_frame, text="Play", command=lambda: self.play_game(title, container))
        play_button.grid(row=0, column=2, sticky="e", padx=10)

    def play_game(self, game_title, container):
        games_scrollable_frame = container
        print(f"Playing {game_title}")
        # Add game to the recent games list and then update the display
        self.add_to_recent_games(game_title)
        self.display_recent_games(games_scrollable_frame)

    def add_to_recent_games(self, game_title):
        # Ensure the game isn't already in the list, then add it
        if game_title not in self.recent_games:
            self.recent_games.insert(0, game_title)  # Add to the start of the list for "most recent" first
        # Optionally limit the number of recent games displayed
        # self.recent_games = self.recent_games[:5]

    def on_game_select(self, event):
        # Displays info for game depending on selection
        selected_game = self.game_list.selection()
        if selected_game:
            # Exclude category titles i.e.("Installed Games")
            if "category" in self.game_list.item(selected_game[0], "tags"):
                return

            game_title = self.game_list.item(selected_game[0], "text")
            game_data = self.get_game_by_title(game_title)
            if game_data:
                self.update_info_frame(game_data)
            else:
                print("Game data not found for:", game_title)

    def get_game_by_title(self, title):
        return next((game for game in self.all_games if game["Title"] == title), None)

    def check_button_exist(self):

        if not hasattr(self, "button_frame"):
            # Create button frame if it doesn't exist
            self.button_frame = tb.Frame(self)
            self.button_frame.grid(row=0, column=2, sticky="nw", padx=5, pady=5)

    def update_info_frame(self, game):
        # Store game_id as title for store page
        self.selected_game_id = game["Title"]

        # Clear contents of game info frame after selection is changed
        for frame in self.info_frame.winfo_children():
            frame.destroy()

        self.check_button_exist()

        # Creates and destroys back button for each frame
        def back_command():
            self.setup_default_info_layout(self.info_frame)
            self.button_frame.destroy()
            del self.button_frame

        # Button creation to go back to info page
        tb.Button(self.button_frame, text="Back",
                  command=back_command).grid(row=0, column=0, sticky="nw", padx=3)

        # Button that calls load_game_store method
        tb.Button(self.button_frame, text="Store Page",
                  command=lambda: self.load_game_store(self.selected_game_id)).grid(row=0,
                                                                                    column=1,
                                                                                    sticky="nw",
                                                                                    padx=3)

        # Display game name
        tb.Label(self.info_frame, text=game["Title"],
                 font=("Helvetica", 30)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        tb.Button(self.info_frame, text="Play", command=lambda: self.add_to_recent_games(game["Title"])).grid(row=1,
                                                                                                    column=1,
                                                                                                    sticky="nw",
                                                                                                    padx=3)


    def populate_games(self):
        # Create TreeView categories for games
        favorite_games_title = self.game_list.insert("",
                                                     "end",
                                                     text=f"Favorite Games [0]",
                                                     open=True,
                                                     tags=("category",))
        installed_games_title = self.game_list.insert("",
                                                      "end",
                                                      text=f"Installed Games [{len(self.all_games)}]",
                                                      open=True,
                                                      tags=("category",))

        # Populate all games into "installed"
        i = 0
        for game in self.all_games:
            if "Title" in game:
                self.game_list.insert(installed_games_title, "end", text=game['Title'])

        self.game_list.tag_configure("category", font=("Unispace", 10, "bold"), background="#45484b")

        # Parent ID to update number of games installed
        self.installed_games_id = installed_games_title
        self.favorite_games_id = favorite_games_title

    def on_right_click(self, event):
        # Open menu if click on entry in TreeView
        iid = self.game_list.identify_row(event.y)
        if iid:
            self.game_list.selection_set(iid)
            self.create_context_menu(iid)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def create_context_menu(self, iid):
        self.context_menu = tb.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Favorite", command=lambda : self.add_to_favorites(iid))
        self.context_menu.add_command(label="Remove from favorites", command=lambda : self.remove_favorite(iid))

    def add_to_favorites(self, iid):
        # Add a game to favorites
        game_title = self.game_list.item(iid, "text")

        games = next((game for game in self.all_games if game["Title"] == game_title), None)

        if games and games not in self.favorite_games:
            self.favorite_games.append(games)
            self.game_list.delete(iid)
            self.game_list.insert(self.favorite_games_id, "end", text=game_title)
            self.update_category_counts()

    def remove_favorite(self, iid):
        # Remove a game from favorites
        game_title = self.game_list.item(iid, "text")

        games = next((game for game in self.all_games if game["Title"] == game_title), None)

        if games:
            self.favorite_games.remove(games)
            self.game_list.delete(iid)
            self.game_list.insert(self.installed_games_id, "end", text=game_title)
            self.update_category_counts()
        else:
            # Debugging print message
            print("Game not found in favorites to remove!")

    def update_category_counts(self):
        # Keep count of games in different categories
        self.game_list.item(self.favorite_games_id, text=f"Favorite Games [{len(self.favorite_games)}]")
        self.game_list.item(self.installed_games_id, text=f"Installed Games "
                                                          f"[{len(self.all_games) - len(self.favorite_games)}]")

    def on_key_release(self, event):
        self.filter_games()

    def filter_games(self):
        # Update visible games depending on content of search entry
        search_query = self.game_search.get().lower()
        self.update_game_list(search_query)

    def update_game_list(self, search_query):
        # Clear and re-create categories while searching
        for title_id, games_list in [(self.installed_games_id, self.all_games), (self.favorite_games_id, self.favorite_games)]:
            for game_id in self.game_list.get_children(title_id):
                self.game_list.delete(game_id)
            filtered_games = [game for game in games_list if search_query.lower() in game["Title"].lower()]
            for game in filtered_games:
                self.game_list.insert(title_id, "end", text=game["Title"])
        self.update_category_counts()



import tkinter as tk
from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from store_off import *
from menu import *
from store_tab import StoreTab
from ttkbootstrap.constants import *
from PIL import ImageTk, Image 
from ttkbootstrap import Style


class LibraryTab(tb.Frame):
    def __init__(self,parent, notebook):
        super().__init__(parent)
        self.parent = parent

        # Use workbook imported from store_off.py
        owned_games = store_off()
        self.wks = owned_games.wks

        self.notebook = notebook

        # Create list of games in sheet
        self.installed_games = [row[1] for row in self.wks.iter_rows(min_row=2, values_only=True) if row[1]]
        self.favorite_games = []

        self.setup_library()

    def load_game_store(self):
        self.notebook.select(1)
        raise NotImplementedError("Will be implemented in future")

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
        info_frame.columnconfigure(0, weight=0)
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

        tk.Label(self.info_frame, text="Welcome!",
                 font=("Unispace", 20)).pack(padx=20, pady=20)

    def on_game_select(self, event):
        # Displays info for game depending on selection
        selected_game = self.game_list.selection()
        if selected_game:
            # Exclude category titles i.e("Installed Games")
            if "category" in self.game_list.item(selected_game[0], "tags"):
                return

            game = self.game_list.item(selected_game[0], "text")
            self.update_info_frame(game)

    def check_button_exist(self):

        if not hasattr(self, "button_frame"):
            # Create button frame if it doesn't exist
            self.button_frame = tb.Frame(self)
            self.button_frame.grid(row=0, column=2, sticky="nw", padx=5, pady=5)

    def update_info_frame(self, game):

        # Clear contents of game info frame after selection is changed
        for frame in self.info_frame.winfo_children():
            if not isinstance(frame, tb.Frame):
                frame.destroy()

        self.check_button_exist()

        def back_command():
            self.setup_default_info_layout(self.info_frame)
            self.button_frame.destroy()
            del self.button_frame

        # Button creation to go back to info page
        tb.Button(self.button_frame, text="Back", command=back_command).grid(row=0, column=0, sticky="nw", padx=3)

        tb.Button(self.button_frame, text="Store Page", command=self.load_game_store).grid(row=0, column=1, sticky="nw", padx=3)

        # Display game name
        tb.Label(self.info_frame, text=f"{game}", font=("Helvetica", 30)).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    def populate_games(self):
        # Create TreeView categories for games
        favorite_games_title = self.game_list.insert("",
                                                     "end",
                                                     text=f"Favorite Games [0]",
                                                     open=True,
                                                     tags=("category",))
        installed_games_title = self.game_list.insert("",
                                                      "end",
                                                      text=f"Installed Games [{len(self.installed_games)}]",
                                                      open=True,
                                                      tags=("category",))

        # Populate all games into "installed"
        for game in self.installed_games:
            self.game_list.insert(installed_games_title, "end", text=game)

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
        game_name = self.game_list.item(iid, "text")
        self.favorite_games.append(game_name)
        self.installed_games.remove(game_name)
        self.game_list.delete(iid)
        self.game_list.insert(self.favorite_games_id, "end", text=game_name)
        self.update_category_counts()

    def remove_favorite(self, iid):
        # Unfavorite a game
        game_name = self.game_list.item(iid, "text")
        self.installed_games.append(game_name)
        self.favorite_games.remove(game_name)
        self.game_list.delete(iid)
        self.game_list.insert(self.installed_games_id, "end", text=game_name)
        self.update_category_counts()


    def update_category_counts(self):
        # Keep count of games in different categories
        self.game_list.item(self.favorite_games_id, text=f"Favorite Games [{len(self.favorite_games)}]")
        self.game_list.item(self.installed_games_id, text=f"Installed Games [{len(self.installed_games)}]")

    def on_key_release(self, event):
        self.filter_games()

    def filter_games(self):
        # Update visible games depending on content of search entry
        search_query = self.game_search.get().lower()
        # matching_games = [game for game in self.games if search_query in game.lower()]
        self.update_game_list(search_query)

    def update_game_list(self, search_query):
        # Clear and re-create categories while searching
        for title_id, games_list in [(self.installed_games_id, self.installed_games), (self.favorite_games_id, self.favorite_games)]:
            for game_id in self.game_list.get_children(title_id):
                self.game_list.delete(game_id)
            filtered_games = [game for game in games_list if search_query in game.lower()]
            for game in filtered_games:
                self.game_list.insert(title_id, "end", text=game)
        self.update_category_counts()



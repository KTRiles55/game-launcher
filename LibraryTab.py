import tkinter as tk
from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from store_off import *
from store_tab import StoreTab
from ttkbootstrap.constants import *
from PIL import ImageTk, Image 
from ttkbootstrap import Style


class LibraryTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

        # Use workbook imported from store_off.py
        owned_games = store_off()
        self.wks = owned_games.wks

        # Create list of games in sheet
        self.installed_games = [row[1] for row in self.wks.iter_rows(min_row=2, values_only=True) if row[1]]
        self.favorite_games = []

        self.setup_library()

    def setup_library(self):
        # Search Frame at the top
        main_frame = tb.Frame(self)
        self.setup_left_layout()

    def setup_left_layout(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=6)

        # Search box
        search_container = tb.Frame(self)
        search_container.grid(row=0, column=0, sticky="ew", padx=3, pady=2)
        self.game_search = tb.Entry(search_container)
        self.game_search.pack(side="right")
        self.game_search.bind("<KeyRelease>", self.key_release)

        # Icon Img
        self.icon_img = PhotoImage(file="images/search.png")
        icon_label = tb.Label(search_container, image=self.icon_img)
        icon_label.pack(side="right")

        # Title
        title_frame = tb.Frame(self)
        title_label = tb.Label(self, text=" My Games", font=("Unispace", "16"), borderwidth=20, border=True)
        title_frame.grid(row=0, column=0)
        title_label.grid(row=0, column=0, sticky="nw")

        # self.visible_items = {}
        self.setup_game_list()
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
        self.game_list.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)

        # Right click menu
        self.game_list.bind("<Button-3>", self.on_right_click)

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
        self.context_menu.add_command(label="Unfavorite", command=lambda : self.remove_favorite(iid))

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

    def key_release(self, event):
        self.filter_games()

    def filter_games(self):
        # Update visible games depending on content of search entry
        search_query = self.game_search.get().lower()
        # matching_games = [game for game in self.games if search_query in game.lower()]
        self.update_treeview(search_query)

    def update_treeview(self, search_query):
        # Clear and re-create categories while searching
        for title_id, games_list in [(self.installed_games_id, self.installed_games), (self.favorite_games_id, self.favorite_games)]:
            for game_id in self.game_list.get_children(title_id):
                self.game_list.delete(game_id)
            filtered_games = [game for game in games_list if search_query in game.lower()]
            for game in filtered_games:
                self.game_list.insert(title_id, "end", text=game)
        self.update_category_counts()



import tkinter as tk
from tkinter import *
from ttkbootstrap import Label
from ttkbootstrap import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from menu import *
import openpyxl
from user import *
import shelve
from PIL import ImageTk, Image


class LibraryTab(tb.Frame):
    """A class representing the library tab in TechWiz store application with ttkbootstrap.

    Attributes:
        parent (widget): The parent widget.
        menu (object): An instance of the menu handling user interactions.
        username (tk.StringVar): The username of the current user.
        all_games (list): A list of dictionaries containing game titles.
    """

    def __init__(self, parent, menu, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username

        # Retrieve entered username as string
        self.current_user_string = self.username.get_username()
        self.current_user_var = tb.StringVar(value=self.current_user_string)
        print("Welcome " + self.current_user_string + "!")

        # Retrieve user-specific library and create dictionary
        self.owned_games = user(username=self.current_user_var.get())
        self.wks_account = self.owned_games.wks_account
        game_titles = self.owned_games.get_parsed_library()
        self.all_games = [{"Title": title} for title in game_titles]

        # Instance of store_tab
        self.menu = menu

        # Lists of user's games for each category
        self.favorite_games = []
        self.recent_games = []

        self.setup_library()
        self.load_favorites()

        # Call method when tab is changed
        self.parent.bind("<<NotebookTabChanged>>", self.on_tab_changed, add="+")

    def on_tab_changed(self, event):
        tab_index = self.parent.index("current")

        tab_title = self.parent.tab(tab_index, "text")
        # Check if tab chosen is Library Tab, then refresh
        if tab_title == "Library":
            print("Refreshing...")
            self.refresh_game_list()

    def load_game_store(self, game_id):
        try:
            # Access the store tab using the menu instance
            lib_store = self.menu.store_tab
            index = self.menu.notebook.index(lib_store)
            self.menu.notebook.select(index)

            # Load store page from game selection
            lib_store.load_window_elem(game_id)
        except Exception as e:
            print(f"Error navigating to store page: {e}")

    def setup_library(self):
        self.setup_game_list_layout()

    def setup_game_list_layout(self):

        # Set the grid configuration for the main container
        self.columnconfigure(0, weight=0, minsize=200)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)

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

        # Welcome text label and frame
        self.welcome_frame = tb.Frame(self)
        # self.welcome_frame.columnconfigure(2, weight=1)
        self.welcome_frame.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        self.welcome_label = tb.Label(self.welcome_frame,
                                      text=f"WELCOME BACK {self.current_user_string.upper()}!",
                                      font=("Unispace", "18", "bold"))
        self.welcome_label.pack(side="left")

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

        self.game_list_scroll = tb.Scrollbar(self, orient="vertical",
                                             bootstyle="light-round", command=self.game_list.yview())
        self.game_list_scroll.grid(row=1, column=0,
                                   sticky="nse")

        self.game_list.configure(yscrollcommand=self.game_list_scroll.set)

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
        self.games_scrollable_frame = ScrolledFrame(self.info_frame, autohide=True)
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
        title_label = tb.Label(game_frame, text=title, font=('Helvetica', 16, "bold"))
        title_label.grid(row=0, column=1, sticky="ew", padx=10)
        game_frame.grid_columnconfigure(1, weight=1)

        # Play button
        play_button = tb.Button(game_frame, text="Play", command=lambda: self.play_game(title, container))
        play_button.grid(row=0, column=2, sticky="e", padx=2)

    def play_game(self, game_title, container):
        games_scrollable_frame = container
        print(f"Playing {game_title}")
        # Add game to the recent games list and then update the display
        self.add_to_recent_games(game_title)
        self.display_recent_games(games_scrollable_frame)

    def add_to_recent_games(self, game_title):
        """Add a game to the list of recently played games.

        Args:
            game_title (str): The title of the game to add.
        """
        # Ensure the game isn't already in the list, then add it
        if game_title not in self.recent_games:
            self.recent_games.insert(0, game_title)
        # Optionally limit the number of recent games displayed
        # self.recent_games = self.recent_games[:5]

    def on_game_select(self, event):
        """Handle selection of a game from the game list.

        Args:
            event (Event): The event that triggered this handler.
        """
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
        """Update the information frame with details of the selected game.

        Args:
            game (dict): The game data to display.
        """
        # Store game_id as title for store page
        self.selected_game_id = game["Title"]

        # Clear contents of game info frame after selection is changed
        for frame in self.info_frame.winfo_children():
            frame.destroy()

        for frame in self.welcome_frame.winfo_children():
            frame.destroy()

        self.check_button_exist()

        # Creates and destroys back button for each frame
        def back_command():
            self.setup_default_info_layout(self.info_frame)
            self.button_frame.destroy()
            del self.button_frame

        # Button creation to go back to info page
        (tb.Button(self.button_frame, text="Back", command=back_command)
            .grid(row=0, column=0, sticky="nw", padx=3))

        # Button that calls load_game_store method
        (tb.Button(self.button_frame, text="Store Page", command=lambda: self.load_game_store(self.selected_game_id))
           .grid(row=0, column=1, sticky="nw", padx=3))

        # Display game name
        (tb.Label(self.info_frame, text=game["Title"], font=("Helvetica", 30))
            .grid(row=0, column=0, sticky="w", padx=10, pady=10))

        (tb.Button(self.info_frame, text="Play", command=lambda: self.add_to_recent_games(game["Title"]))
            .grid(row=1, column=1, sticky="nw", padx=3))

    def populate_games(self):
        self.load_favorites()
        # Create TreeView categories for games
        favorite_games_title = self.game_list.insert("",
                                                     "end",
                                                     text=f"Favorite Games [{len(self.favorite_games)}]",
                                                     open=True,
                                                     tags=("category",))
        installed_games_title = self.game_list.insert("",
                                                      "end",
                                                      text=f"Installed Games [{len(self.all_games)}]",
                                                      open=True,
                                                      tags=("category",))

        # Populate all games into "installed"
        for game in self.all_games:
            if not any(fav["Title"] == game["Title"] for fav in self.favorite_games):
                self.game_list.insert(installed_games_title, "end", text=game["Title"])

        # Populate games from Favorite Games
        for fav_game in self.favorite_games:
            if "Title" in fav_game:
                self.game_list.insert(favorite_games_title, "end", text=fav_game["Title"])

        self.game_list.tag_configure("category", font=("Unispace", 10, "bold"), background="#45484b")

        # Parent ID to update number of games installed
        self.installed_games_id = installed_games_title
        self.favorite_games_id = favorite_games_title

    def refresh_game_list(self):
        updated_game_titles = self.owned_games.get_parsed_library()
        updated_titles_dict = [{"Title": title} for title in updated_game_titles]
        updated_titles_set = {game["Title"] for game in updated_titles_dict}

        current_titles_set = {game['Title'] for game in self.all_games}

        # New titles not currently displayed
        new_titles = updated_titles_set - current_titles_set

        # Filter out the new games added
        new_games = [game for game in updated_titles_dict if game["Title"] in new_titles]
        self.all_games.extend(new_games)

        # Add new games to TreeView
        for game in new_games:
            self.game_list.insert(self.installed_games_id, "end", text=game["Title"])

        # Update game count
        self.update_category_counts()

    def on_right_click(self, event):
        """Handle right-click events to provide a context menu for game options.

        Args:
            event (Event): Right-click event.
        """
        # Open menu if click on entry in TreeView
        iid = self.game_list.identify_row(event.y)
        if iid:
            self.game_list.selection_set(iid)
            self.create_context_menu(iid)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def create_context_menu(self, iid):
        """Create a context menu for game actions.

        Args:
            iid (str): The identifier of the selected TreeView item.
        """
        self.context_menu = tb.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Favorite", command=lambda: self.add_to_favorites(iid))
        self.context_menu.add_command(label="Remove from favorites", command=lambda: self.remove_favorite(iid))
        self.context_menu.add_command(label="Delete", command=lambda: self.game_list.delete(iid))

    def add_to_favorites(self, iid):
        """Add the selected game to favorites.

        Args:
            iid (str): The identifier of the selected TreeView item.
        """
        # Add a game to favorites
        game_title = self.game_list.item(iid, "text")

        games = next((game for game in self.all_games if game["Title"] == game_title), None)

        if games and games not in self.favorite_games:
            self.favorite_games.append(games)
            self.game_list.delete(iid)
            self.game_list.insert(self.favorite_games_id, "end", text=game_title)
            self.update_category_counts()
            self.save_favorites()

    def save_favorites(self):
        with shelve.open('data/favorite.db') as db:
            db[self.current_user_string + "_favorites"] = self.favorite_games

    def load_favorites(self):
        with shelve.open("data/favorite.db") as db:
            self.favorite_games = db.get(self.current_user_string + "_favorites", [])

    def remove_favorite(self, iid):
        """Remove the selected game from favorites.

        Args:
            iid (str): The identifier of the selected TreeView item.
        """
        # Remove a game from favorites
        game_title = self.game_list.item(iid, "text")

        game_to_remove = next((game for game in self.favorite_games if game["Title"] == game_title), None)

        if game_to_remove:
            self.favorite_games.remove(game_to_remove)
            self.game_list.delete(iid)
            # Reinsert into installed games
            if any(game["Title"] == game_title for game in self.all_games):
                self.game_list.insert(self.installed_games_id, "end", text=game_title)
            self.update_category_counts()
            self.save_favorites()
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
        """Updates game list in order to simulate a search
        Args:
            search_query (str): Search query string entered into search entry field.
        """
        for title_id in [self.installed_games_id, self.favorite_games_id]:
            for game_id in self.game_list.get_children(title_id):
                self.game_list.delete(game_id)

        favorite_titles = set(game['Title'] for game in self.favorite_games)

        # Clear and re-create categories while searching
        for game in self.all_games:
            if search_query.lower() in game['Title'].lower():  # Check if game matches search query
                if game['Title'] in favorite_titles:
                    # Insert into favorites if it's a favorite game and matches the search
                    self.game_list.insert(self.favorite_games_id, "end", text=game['Title'])
                else:
                    # Otherwise, insert into installed games
                    self.game_list.insert(self.installed_games_id, "end", text=game['Title'])

        self.update_category_counts()

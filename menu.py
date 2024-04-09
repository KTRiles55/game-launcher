from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import launcher
from PIL import ImageTk, Image


class Menu(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_widget()

    def create_widget(self):
        notebook_style = tb.Style()
        tab_style = tb.Style()
        tab_style.configure("TNotebook.Tab", font=("Unispace", "18", "bold"))
        notebook_style.configure("custom.TNotebook", padding=[0,0], tabmargins=[0,0,0,0], tabposition="nsew")
        notebook = tb.Notebook(self, style="custom.TNotebook")

        # Tabs
        home_tab = HomeTab(notebook)
        library_tab = LibraryTab(notebook)
        store_tab = StoreTab(notebook)
        settings_tab = SettingsTab(notebook)

        # Adding Tabs
        notebook.add(home_tab, text="Home")
        notebook.add(store_tab, text="Store")
        notebook.add(library_tab, text="Library")
        notebook.add(settings_tab, text="Settings")

        notebook.pack(expand=True, fill=BOTH)


class HomeTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent


class LibraryTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent


class StoreTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

        self.setup_layout()
    def setup_layout(self):
        # Search Frame at the top
        search_frame = tb.Frame(self)
        search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.columnconfigure(0, weight=1)  # Make the search frame expand with the window
        self.setup_search_frame(search_frame)

        # Game Frame below the search frame
        game_frame = tb.Frame(self)
        game_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.rowconfigure(1, weight=1)  # Make the game frame expand with the window
        self.setup_game_frames(game_frame)

    def render_img(self, frame, path, r, c):
        #Must prevent garbarge collection
        img_obj =  ImageTk.PhotoImage(Image.open("images/" + path))
        img_lbl = tb.Label(frame, image=img_obj)
        img_lbl.image = img_obj
        img_lbl.grid(row=r, column=c, padx=20)

    def setup_search_frame(self, parent):
        # Here you can add widgets to the search_frame
        search_label = tb.Label(parent, text="Search:")
        search_entry = tb.Entry(parent, bootstyle="secondary")

        search_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        search_entry.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        parent.columnconfigure(1, weight=1)

    def setup_game_frames(self, parent):
        # Split the game area into two frames
        game_frame1 = tb.Frame(parent, bootstyle="secondary")
        game_frame2 = tb.Frame(parent, bootstyle="secondary")

        game_frame1.grid(row=0, column=0, sticky="nsew", padx=5, pady=6)
        game_frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=6)

        # Make both game frames expand equally
        parent.columnconfigure([0, 1], weight=1)
        # Allow game frames to expand vertically
        parent.rowconfigure(0, weight=1)

        # Add content into game frames
        self.generate_game_widgets([game_frame1, game_frame2])

    def generate_game_widgets(self, frames):
        # Game widget locations
        game_widgets = []
        genres = ["MMO", "RPG", "Survival", "Simulations"]
        images = ["green.png"]

        j = 0
        for frame in frames:
            frame.grid_columnconfigure(0, weight=1)
            for i in range(3):
                game_widget = tb.Frame(frame, bootstyle="bg")
                game_widget.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
                self.render_img(game_widget, images[0], 1, 0)
                tb.Label(game_widget, text="Title").grid(row=0, column=0, padx=5, pady=5)
                tb.Label(game_widget, text="Developer").grid(row=0, column=5, padx=5, pady=5)
                tb.Label(game_widget, text="Price: $$$").grid(row=1, column=1)
                tb.Label(game_widget, text="Tags:").grid(row=2, column=1, pady=(0, 10))
                # Generate tags
                for k, genre in enumerate(genres):
                    tb.Label(game_widget, text=genre).grid(row=2, column=2+k, padx=5, pady=(0, 10))
                tb.Button(game_widget, text="View", bootstyle="primary").grid(row=1, column=5)
                tb.Button(game_widget, text="Add to Cart", bootstyle="primary").grid(row=1, column=4)
                game_widgets.append(game_widget)
                j += 1


class SettingsTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent





from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image 
from store import *
import math
from ttkbootstrap import Style

class StoreTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.store = store()
        self.shared_tag = self.store.get_all_games()

        
        self.max_widgets = 10
        self.current_page = 1
        self.pointer_start = 0
        if(len(self.shared_tag) >= self.max_widgets):
            self.pointer_end = self.max_widgets
        else: 
            self.pointer_end = len(self.shared_tag)



        self.setup_layout()

    def increment_page(self, game_frame):
        list_len = len(self.shared_tag)
        increment = self.max_widgets 
        remaining = (list_len - self.pointer_end)
        if((remaining > 0) and (remaining  < self.max_widgets)):
            #Special case for when the game widgets are less than layout
            print("special case")
            self.current_page += 1
            self.pointer_start = self.pointer_end
            increment = remaining 
        elif(list_len  == self.pointer_end):
            #When reached end of page
            print("End of page")
            increment =0
        else:
            self.pointer_start = self.pointer_end
        self.pointer_end += increment
        #print("pointer_stary=" + str(self.pointer_start)+ "pointer_end=" + str(self.pointer_end) + "remaining=" + str(remaining) + "increment=" + str(increment))
        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame)


    def decrement_page(self, game_frame):
        list_len = len(self.shared_tag)
        decrement = self.max_widgets
        previous = self.pointer_start
        if((previous > 0) and (previous  < self.max_widgets)):
            # Special case for when the game widgets are less than layout
            self.current_page += 1
            self.pointer_end = self.pointer_start
            decrement = self.pointer_start 
        elif(self.pointer_start == 0):
            # When reached end of page
            decrement =0
        else:
            self.pointer_end = self.pointer_start
        self.pointer_start -= decrement
        
        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame)

    
    def render_img(self, frame, path, r, c):
        #Must prevent garbarge collection
        img_obj =  ImageTk.PhotoImage(Image.open("images/" + path))
        img_lbl = tb.Label(frame, image=img_obj)
        img_lbl.image = img_obj
        img_lbl.grid(row=r, column=c, padx=20)

    def get_tags(self, selected, game_frame):
        
        self.shared_tag = self.store.get_games_sharing_tag(selected.get())

        #Reset list pointers
        self.pointer_start = 0
        if(len(self.shared_tag) >= self.max_widgets):
            self.pointer_end = self.max_widgets
        else: 
            self.pointer_end = len(self.shared_tag)

        self.setup_game_frames(game_frame)

    def destroy_frames(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def setup_layout(self):
        # Search Frame at the top
        scrollable_frame = ScrolledFrame(self, autohide=False, bootstyle="secondary")
        scrollable_frame.grid(sticky="nsew")
        search_frame = tb.Frame(self)
        search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.columnconfigure(0, weight=1)  # Make the search frame expand with the window


        # Game Frame below the search frame
        game_frame = tb.Frame(scrollable_frame, bootstyle="secondary")
        scrollable_frame.grid(row=1, column=0, sticky="nsew")
        game_frame.grid(sticky="nsew")
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.rowconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)  # Make the game frame expand with the window
        

        self.setup_search_frame(search_frame, game_frame)
        self.setup_game_frames(game_frame)

    def setup_search_frame(self, parent, game_frame):
        # Here you can add widgets to the search_frame
        tags =  ["RPG", "Simulation", "Strategy", "Multiplayer", "Sandbox", "Puzzle"]
        selected_tag = StringVar()
        search_label = tb.Label(parent, text="Search:")
        search_entry = tb.Entry(parent, bootstyle="secondary")
        category_lbl =  tb.Label(parent, text="Categories")
        category_drop = tb.OptionMenu(parent, selected_tag, *tags, command = lambda tags: [self.get_tags(selected_tag, game_frame)])
        cart_btn = tb.Button(parent, text="Cart", command = lambda: self.destroy_frames(game_frame))
        left_arrow = tb.Button(parent, text="<", command = lambda: self.decrement_page(game_frame))
        right_arrow = tb.Button(parent, text=">", command = lambda: self.increment_page(game_frame))

        search_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        search_entry.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        category_lbl.grid(row=0, column=2, padx=5)
        category_drop.grid(row=0, column=3, padx=5)
        cart_btn.grid(row=0, column=4, padx=10)
        left_arrow.grid(row=0, column=5)
        right_arrow.grid(row=0, column=6)

        parent.columnconfigure(1, weight=1)

    def setup_game_frames(self, parent):
        # Split the game area into two frames
        game_frame1 = tb.Frame(parent, bootstyle="secondary")
        game_frame2 = tb.Frame(parent, bootstyle="secondary")

        game_frame1.grid(row=0, column=0, sticky="nse", padx=5, pady=6)
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
        genres =  ["RPG", "Simulation", "Strategy", "Multiplayer", "Sandbox", "Puzzle"]
        images = ["green.png"]

        j=0 
        frame = frames[0]
       
        for i in range(self.pointer_start, self.pointer_end):
            game_widget = tb.Frame(frame, bootstyle="bg")
            game_widget.grid(row=i+j, column=0, sticky="nsew", padx=5, pady=5)
            self.render_img(game_widget, images[0], 1, 0)
            tb.Label(game_widget, text=self.shared_tag[i]["Title"]).grid(row=0, column=0, padx=5, pady=5)
            tb.Label(game_widget, text=self.shared_tag[i]["Developer"]).grid(row=0, column=5, padx=5, pady=5)
            tb.Label(game_widget, text="Price: " + str(self.shared_tag[i]["Price"])).grid(row=1, column=1)
            tb.Label(game_widget, text="Tags:").grid(row=2, column=1, pady=(0, 10))
            # Generate tags
            for k, genre in enumerate(genres):
                tb.Label(game_widget, text=genre).grid(row=2, column=2+k, padx=5, pady=(0, 10))
            tb.Button(game_widget, text="View", bootstyle="primary").grid(row=1, column=5)
            tb.Button(game_widget, text="Add to Cart", bootstyle="primary").grid(row=1, column=4)
            game_widgets.append(game_widget)
            j += 1
            #alternating between frames 
            if((j%2) == 1):
                frame = frames[1]
            else:
                frame = frames[0]



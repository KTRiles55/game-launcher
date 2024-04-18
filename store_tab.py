from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image 
from store import *
from store_off import *
from checkout_page import *
import math
from ttkbootstrap import Style


class StoreTab(tb.Frame):
    def __init__(self,parent, user):
        super().__init__(parent)
        self.parent = parent
        self.grid(sticky="nsew")
        self.user =user
        print(self.user.get_game_details())

        self.store = store_off()
        self.shared_tag = self.store.get_all_games()
        self.cart = [] 

        self.max_widgets = 10
        self.current_page = 1
        self.pointer_start = 0
        if(len(self.shared_tag) >= self.max_widgets):
            self.pointer_end = self.max_widgets
        else: 
            self.pointer_end = len(self.shared_tag)

        self.setup_layout()

    def update_cart_button(self, parent, game_frame, scrollable):
        total_items = len(self.cart)
        # If not empty cart than display
        if(len(self.cart) > 0):
            cart_btn = tb.Button(parent, text= str(total_items) + " Cart", bootstyle="success", command = lambda: self.run_checkout(parent, game_frame, scrollable))
            cart_btn.grid(row=0, column=1, sticky="nse")

    def add_to_cart(self, game):
        in_cart = False
        for i in range(len(self.cart)):
            if(self.cart[i]["Title"]) == game["Title"]:
                in_cart = True
                break

        if not (in_cart):
            self.cart.append(game)
        else:
            print("Game already in cart")

    def run_checkout(self, search_frame, game_frame, scrollable):
        search_frame.destroy()
        game_frame.destroy()
        checkout_page(self, scrollable, self.cart)
        
        #scrollable.destroy()
        #self.destroy_frames(game_frame)

    def update_page_num(self,lbl):
        #Change page number
        page_num = str(math.ceil(self.pointer_end/self.max_widgets)) + "/" + (str(int(math.ceil(len(self.shared_tag)+1)/self.max_widgets)))
        lbl.config(text=page_num)

    def increment_page(self,page_num_lbl,  game_frame, search_frame, scrollable):
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

        self.update_page_num(page_num_lbl)

        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame, search_frame, scrollable)

    def decrement_page(self, page_num_lbl, game_frame, search_frame, scrollable):
        list_len = len(self.shared_tag)
        decrement = self.max_widgets
        previous = self.pointer_start
        if((previous > 0) and (previous  < self.max_widgets)):
            #Special case for when the game widgets are less than layout
            self.current_page += 1
            self.pointer_end = self.pointer_start
            decrement = self.pointer_start 
        elif(self.pointer_start == 0):
            #When reached end of page
            decrement =0
        else:
            self.pointer_end = self.pointer_start
        self.pointer_start -= decrement

        self.update_page_num(page_num_lbl)

        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame, search_frame, scrollable)

    def render_img(self, frame, path, r, c):
        #Must prevent garbarge collection
        img_obj = ImageTk.PhotoImage(Image.open("images/" + path))
        img_lbl = tb.Label(frame, image=img_obj)
        img_lbl.image = img_obj
        img_lbl.grid(row=r, column=c, padx=20)

    def get_tags(self, selected, game_frame, page_num_lbl, scrollable, search_frame):
        
        self.shared_tag = self.store.get_games_sharing_tag(selected.get())

        #Reset list pointers
        self.pointer_start = 0
        if(len(self.shared_tag) >= self.max_widgets):
            self.pointer_end = self.max_widgets
        else: 
            self.pointer_end = len(self.shared_tag)

        self.update_page_num(page_num_lbl)

        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame, search_frame, scrollable)

    def destroy_frames(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        #print(frame)

    def setup_layout(self):
        # Search Frame at the top
        main_frame = tb.Frame(self)
        search_frame = tb.Frame(self)
        search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        scrollable_frame = ScrolledFrame(self, autohide=False, bootstyle="secondary")
        scrollable_frame.grid(row=1, column=0)

        # Game Frame below the search frame
        game_frame = tb.Frame(scrollable_frame, bootstyle="secondary")
        game_frame.grid(sticky="nsew")
        scrollable_frame.grid(row=1, column=0, sticky="nsew")
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.rowconfigure(1, weight=1)
        
        self.columnconfigure(0, weight=1)  # Make the search frame expand with the window
        self.rowconfigure(1, weight=1)  # Make the game frame expand with the window
        
        #check if cart is empty when returning from checkout
        self.update_cart_button(search_frame, game_frame, scrollable_frame)

        self.setup_game_frames(game_frame, search_frame, scrollable_frame)
        self.setup_search_frame(search_frame, game_frame, search_frame, scrollable_frame)

    def setup_search_frame(self, parent, game_frame, search_frame, scrollable):
        # Here you can add widgets to the search_frame
        tags =  ["Category", "RPG", "Simulation", "Strategy", "Multiplayer", "Sandbox", "Puzzle"]
        page_num = str(math.ceil(self.pointer_end/self.max_widgets))
        total_items = str(len(self.cart))

        selected_tag = StringVar()
        searching = StringVar()
        search_label = tb.Label(parent, text="Search:")
        search_entry = tb.Entry(parent, textvariable=searching)
        category_lbl = tb.Label(parent, text="Categories")
        back_btn = tb.Button(parent, text="Back", bootstyle="outline")
        category_drop = tb.OptionMenu(parent, selected_tag, *tags, command = lambda tags: [self.get_tags(selected_tag, game_frame, page_num_lbl, scrollable, search_frame)])
        page_num_lbl = tb.Label(parent, text=page_num + "/" + str(int(math.ceil(len(self.shared_tag)+1)/self.max_widgets)))
        left_arrow = tb.Button(parent, text="<", command = lambda: self.decrement_page(page_num_lbl,game_frame, parent, scrollable))
        right_arrow = tb.Button(parent, text=">", command = lambda: self.increment_page(page_num_lbl,game_frame, parent, scrollable))

        back_btn.grid(row=-0, column=0, sticky="nw")
        search_label.grid(row=0, column=2, sticky="w")
        search_entry.grid(row=0, column=3, sticky="nw")
        category_lbl.grid(row=0, column=4, padx=5)
        category_drop.grid(row=0, column=5, padx=5)
        page_num_lbl.grid(row=0, column=6, padx=10)
        left_arrow.grid(row=0, column=7)
        right_arrow.grid(row=0, column=8)

        parent.columnconfigure(1, weight=1)

        # Create a binding on the entry box
        search_entry.bind("<Return>", lambda event: self.search(searching.get(), parent, game_frame, scrollable,))

    def search(self, entry, search_frame, parent, scrollable):
        self.shared_tag=self.store.get_related_search(entry)
        #Updates pointers but max related games in a page is set to 10
        self.pointer_start = 0
        self.pointer_end = len(self.shared_tag)
        self.destroy_frames(parent)
        self.setup_game_frames( parent, search_frame, scrollable)
        print(self.shared_tag)

    def setup_game_frames(self, parent, search_frame, scrollable):
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
        self.generate_game_widgets( parent, [game_frame1, game_frame2], search_frame, scrollable)

    def generate_game_widgets(self, parent, frames, search_frame, scrollable):
        # Game widget locations
        game_widgets = []
        images = ["green.png"]

        j=0 
        frame = frames[0]
       
        for i in range(self.pointer_start, self.pointer_end):
            game_widget = tb.Frame(frame, bootstyle="bg")
            game_widget.grid(row=i+j, column=0, sticky="nsew", padx=5, pady=5)
            self.render_img(game_widget, images[0], 1, 0)
            title_temp = tb.Label(game_widget, text=self.shared_tag[i]["Title"])
            title_temp.config(font=("Helvetica", 12))
            title_temp.grid(row=0, column=0, padx=5, pady=5)
            tb.Label(game_widget, text=self.shared_tag[i]["Developer"]).grid(row=0, column=5, padx=5, pady=5)
            tb.Label(game_widget, text="$" + str(self.shared_tag[i]["Price"])).grid(row=1, column=1)
            # Generate tags
            k =0
            for tag in (self.shared_tag[i]["Tags"]):
                tb.Label(game_widget, text=tag).grid(row=2, column=2+k, padx=5, pady=(0, 10))
                k += 1
            tb.Button(game_widget, text="View", bootstyle="primary", command= lambda i=i: [print(self.shared_tag[i]["Title"]), self.preview_game(i, search_frame, parent, scrollable)]).grid(row=1, column=5)
            tb.Button(game_widget, text="Add to Cart", bootstyle="primary", command= lambda i=i: [self.add_to_cart(self.shared_tag[i]), self.update_cart_button(search_frame, parent, scrollable)]).grid(row=1, column=4)
            game_widgets.append(game_widget)
            j += 1
            # alternating between frames
            if((j%2) == 1):
                frame = frames[1]
            else:
                frame = frames[0]


    def preview_game(self, id, search_frame, game_frame, scrollable):
        #render_img(self, frame, path, r, c)
        fill = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Cursus in hac habitasse platea dictumst quisque sagittis purus sit. Viverra justo nec ultrices dui. Fermentum odio eu feugiat pretium nibh ipsum. Scelerisque mauris pellentesque pulvinar pellentesque habitant. Commodo sed egestas egestas fringilla phasellus. Quis eleifend quam adipiscing vitae proin. Augue mauris augue neque gravida in fermentum et sollicitudin. Varius vel pharetra vel turpis nunc. Orci phasellus egestas tellus rutrum tellus pellentesque eu. Sollicitudin tempor id eu nisl nunc mi ipsum faucibus. Nulla aliquet enim tortor at auctor urna nunc. Eu feugiat pretium nibh ipsum consequat nisl vel pretium lectus. Sodales ut eu sem integer vitae justo. Odio pellentesque diam volutpat commodo sed egestas egestas fringilla phasellus. Sit amet est placerat in egestas erat imperdiet sed. Sed arcu non odio euismod. Lorem ipsum dolor sit amet consectetur adipiscing elit. Donec ac odio tempor orci dapibus. Vulputate eu scelerisque felis imperdiet proin fermentum."
        game_frame.destroy()
        self.destroy_frames(search_frame)
        back_btn = tb.Button(search_frame, text="Back", bootstyle="outline", command=lambda: self.setup_layout())
        back_btn.grid(row=0, column=0, sticky="nsew")
        
        game_title = tb.Frame(scrollable, bootstyle="bg")
        banner_frame = tb.Frame(scrollable, bootstyle="bg")
        body_frame = tb.Frame(scrollable, bootstyle="bg")
        scrollable.config(bootstyle="bg")
        describe_frame = tb.Text(body_frame,width=100)
        describe_frame.config(font=("Helvetica", 12))
        support_frame = tb.Text(body_frame)
        support_frame.config(font=("Helvetica", 12))

    
        
        banner_frame.grid(row=0, column=0, sticky= "ns")
        game_title.grid(row=1,column=0, sticky="ns")
        body_frame.grid(row=2, column=0, sticky= "ns")
        self.render_img(banner_frame, "games/pong/banner.png", 0, 0)
        describe_frame.grid(row=0, column=0, sticky="nsew")
        describe_frame.insert(END, fill)
        support_frame.grid(row=0, column=1,sticky="nsew")

        title = tb.Label(game_title, text = self.shared_tag[id]["Title"])
        title.config(font=("Helvetica", 20))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        #Support frame filler
        tag_lbl = tb.Label(support_frame, text="Tags: ")
        tag_lbl.config(font=("Helvetica", 10))
        tag_lbl.grid(row=0, column=0, padx=5, pady=(0, 10))
        i = 1
        for tag in (self.shared_tag[id]["Tags"]):
            temp_tag = tb.Label(support_frame, text=tag, bootstyle="light")
            temp_tag.config(font=("Courier", 10))
            temp_tag.grid(row=0, column=0+i, padx=5, pady=(0, 10))
            i += 1
        
        release_lbl = tb.Label(support_frame, text="Release Date: " )
        release_lbl.config(font=("Helvetica", 10))
        release_lbl.grid(row=1, column=0, padx=5,  pady=(0, 10))
        date_lbl = tb.Label(support_frame, text=str(self.shared_tag[id]["Release_Date"]))
        date_lbl.config(font=("Courier", 10))
        date_lbl.grid(row=1, column=1, padx=5,  pady=(0, 10))

        cart_btn = tb.Button(support_frame, text="Add to Cart", bootstyle="success", command=lambda: [self.add_to_cart(self.shared_tag[id]), self.setup_layout()])
        cart_btn.grid(row=2, column=1, padx=5,  pady=(0, 10), columnspan = 2, sticky="ns")










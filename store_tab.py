from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image 
from store import *
from checkout_page import *
import math
import pydoc
from ttkbootstrap import Style

class StoreTab(tb.Frame):
    """
    Authors: Sofia Castro
    Contributor(s): Narek Asaturyan
    """
    def __init__(self,parent, user, default_game_title=None):
        super().__init__(parent)
        self.parent = parent
        self.grid(sticky="nsew")
        self.user = user

        self.default_game_title = default_game_title
        if self.default_game_title:
            self.preview_default_game()
    
        self.store = store()
        self.games = self.store.get_all_games()
        self.cart = [] 
        self.filters = {"Category": "All", "lowest_price": 0, "highest_price": 100 }
        

        self.max_widgets = 10
        self.current_page = 1
        self.pointer_start = 0
        if(len(self.games) >= self.max_widgets):
            self.pointer_end = self.max_widgets
        else: 
            self.pointer_end = len(self.games)

        #self.setup_layout()
        #print(self.games)
        self.setup_layout()

    def reset_cart(self):
        self.cart = []

    def update_cart_button(self, parent, game_frame, scrollable):
        """
            Updates the count for items in cart
            args:
            parent, game_frame, scrollable are all tb.Frame
        """
        total_items = len(self.cart)
        #If not empty cart than display
        if(len(self.cart) > 0):
            cart_btn = tb.Button(parent, text= "(" + str(total_items) + ")" + " Cart", bootstyle="success", command = lambda: self.run_checkout(parent, game_frame, scrollable))
            cart_btn.grid(row=0, column=1, padx=10, sticky="nse")

        

    def add_to_cart(self, game):
        """
            Updates cart if game not in cart
            args:
            game (dictionary)
        """
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
        """
            Updates the frames displayed
            args:
            search_frame (tb.Frame), game_frame(tb.Frame), scrollable(tb.ScrollableFrame)
        """

        search_frame.destroy()
        game_frame.destroy()
        checkout_page(self, scrollable, self.cart, self.user)
        
        #scrollable.destroy()
        #self.destroy_frames(game_frame)
        

    def update_page_num(self,search_frame):
        #Change page number
        """
            Updates the page count based on the maximum widgets per page

            args:
            search_frame (tb.Frame)
        """
        max_num = int(math.ceil(len(self.games)+1)/self.max_widgets)
        if(max_num == 0):
            max_num += 1

        page_num = str(math.ceil(self.pointer_end/self.max_widgets)) + "/" + (str(max_num))
        page_num_lbl = tb.Label(search_frame, text=page_num)
        page_num_lbl.grid(row=0, column=7, sticky="nsew")


    def increment_page(self, game_frame, search_frame, scrollable):
        """
            Ascends the games list to show games to be displayed next and changes widgets accordingly

            args:
            search_frame (tb.Frame), game_frame(tb.Frame), scrollable(tb.ScrollableFrame)
        """
        list_len = len(self.games)
        increment = self.max_widgets 
        remaining = (list_len - self.pointer_end)
        if((remaining > 0) and (remaining  < self.max_widgets)):
            #Special case for when the game widgets are less than layout
            self.current_page += 1
            self.pointer_start = self.pointer_end
            increment = remaining 
        elif(list_len  == self.pointer_end):
            #When reached end of page
            increment =0
        else:
            self.pointer_start = self.pointer_end
        self.pointer_end += increment


        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame, search_frame, scrollable)
        self.update_page_num(search_frame)


    def decrement_page(self, game_frame, search_frame, scrollable):
        """
            Decesends the games list to show games to be displayed next and changes widgets accordingly

            args:
            search_frame (tb.Frame), game_frame(tb.Frame), scrollable(tb.ScrollableFrame)
        """
        list_len = len(self.games)
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


        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame, search_frame, scrollable)
        self.update_page_num(search_frame)


    def render_img(self, frame, path, r, c):
        """
            Displays an image to a frame

            args:
            frame (tb.Frame), path(String), r (int), c(int)
        """
        #Must prevent garbarge collection
        img_obj = ImageTk.PhotoImage(Image.open("images/games/" + path))
        img_lbl = tb.Label(frame, image=img_obj)
        img_lbl.image = img_obj
        img_lbl.grid(row=r, column=c, padx=20)

    def filterate(self, game_frame, scrollable, search_frame):
        """
            Reads the current filters inputted

            args:
            search_frame (tb.Frame), game_frame(tb.Frame), scrollable(tb.ScrollableFrame)
        """
        self.games = []
        unfiltered = self.store.get_games_sharing_tag(self.filters["Category"])
        low_price = self.filters["lowest_price"]
        high_price = self.filters["highest_price"]
        
        #sorts by price
        i = 0
        for i in range(len(unfiltered)):
            game_price = unfiltered[i]["Price"]
            if(game_price <= high_price) and (game_price >= low_price):
                self.games.append(unfiltered[i])
        print(self.filters)


        #Reset list pointers
        self.pointer_start = 0
        if(len(self.games) >= self.max_widgets):
            self.pointer_end = self.max_widgets
        else: 
            self.pointer_end = len(self.games)


        self.destroy_frames(game_frame)
        self.setup_game_frames(game_frame, search_frame, scrollable)
        self.update_page_num(search_frame)
        

    def destroy_frames(self, frame):
        """
            Destroys all the children widgets

            args:
            frame(tb.Frame)
        
        """

        #Destroy children widgets
        for widget in frame.winfo_children():
            widget.destroy()
        #print(frame)

    def setup_layout(self):      
        # Search Frame at the top
        search_frame = tb.Frame(self)
        search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        scrollable_frame = ScrolledFrame(self, autohide=False)
        scrollable_frame.grid(row=1, column=0)
        


        # Game Frame below the search frame
        game_frame = tb.Frame(scrollable_frame)
        game_frame.grid(sticky="nsew")
        scrollable_frame.grid(row=1, column=0, sticky="nsew")
        scrollable_frame.columnconfigure(0, weight=0)
        scrollable_frame.rowconfigure(1, weight=0)
        
        self.columnconfigure(0, weight=1)  # Make the search frame expand with the window
        self.rowconfigure(1, weight=1)  # Make the game frame expand with the window
        

        self.setup_game_frames(game_frame, search_frame, scrollable_frame)
        self.setup_search_frame(search_frame, game_frame,scrollable_frame)

        #check if cart is empty when returning from checkout
        self.update_cart_button(search_frame, game_frame, scrollable_frame)
        


    def setup_search_frame(self, parent, game_frame, scrollable):
        # Here you can add widgets to the search_frame
        page_num = str(math.ceil(self.pointer_end/self.max_widgets))
        total_items = str(len(self.cart))

        selected_tag = StringVar()
        searching = StringVar()
        search_label = tb.Label(parent, text="Search:")
        search_entry = tb.Entry(parent, textvariable=searching, bootstyle="secondary")
        left_arrow = tb.Button(parent, text="<", command = lambda: self.decrement_page(game_frame, parent, scrollable))
        right_arrow = tb.Button(parent, text=">", command = lambda: self.increment_page(game_frame, parent, scrollable))
        #listbox = Listbox(parent)
        

        search_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        search_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)


        search_label.grid(row=0, column=2, sticky="w")
        search_entry.grid(row=0, column=3, sticky="nw")
        left_arrow.grid(row=0, column=6)
        right_arrow.grid(row=0, column=8)

        parent.columnconfigure(1, weight=1)

        self.update_page_num(parent)
        # Create a binding on the entry box
        search_entry.bind("<Return>", lambda event: self.search_games(searching.get(), parent, game_frame, scrollable,))

    def search_games(self, entry, search_frame, parent, scrollable):
        self.games=self.store.get_related_search(entry)
        #Updates pointers but max related games in a page is set to 10
        self.pointer_start = 0
        self.pointer_end = len(self.games)
        self.destroy_frames(parent)
        self.setup_game_frames( parent, search_frame, scrollable)
        self.update_page_num(search_frame)
        print(self.games)
        


    def setup_game_frames(self, parent, search_frame, scrollable):
        # Split the game area into two frames
        filter_frame = tb.Frame(parent, width=25, bootstyle="bg")
        game_frame1 = tb.Frame(parent, bootstyle="secondary")
        game_frame2 = tb.Frame(parent, bootstyle="secondary")

        filter_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        game_frame1.grid(row=0, column=1, sticky="nsew", padx=5, pady=6)
        game_frame2.grid(row=0, column=2, sticky="nsew", padx=5, pady=6)

        # Make both game frames expand equally
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        # Allow game frames to expand vertically
        parent.rowconfigure(0, weight=1)

        # Add content into game frames
        self.setup_filter_frame(filter_frame, parent, search_frame, scrollable)
        self.generate_game_widgets( parent, [game_frame1, game_frame2], search_frame, scrollable)
    
    def setup_filter_frame(self, parent, game_frame, search_frame, scrollable):
        tags =  ["Category", "All", "RPG", "Simulation", "Strategy", "Multiplayer", "Sandbox", "Puzzle", "Indie", "RTS", "Shooter"]
        low_price = IntVar()
        low_price.set(self.filters["lowest_price"])
        high_price = IntVar()
        high_price.set(self.filters["highest_price"])
        selected_tag = StringVar()
        
        category_lbl =  tb.Label(parent, text="Categories")
        category_lbl.config(text=self.filters["Category"], font=("Courier", 10))
        category_drop = tb.OptionMenu(parent, selected_tag, *tags, bootstyle="outline", command = lambda tags: [self.set_category(selected_tag.get()), self.filterate(game_frame, scrollable, search_frame)])
        selected_tag.set("Categories")
        price_lbl = tb.Label(parent, text="Price Range")
        price_lbl.config(font=("Courier", 10))
        price_val = tb.Label(parent)
        low_lbl = tb.Label(parent, text="Lowest $")
        high_lbl = tb.Label(parent, text="Highest $")
        lower_entry = tb.Entry(parent, textvariable=low_price, width=5)
        upper_entry = tb.Entry(parent, textvariable=high_price, width=5)
        price_enter = tb.Button(parent, text="Enter", command = lambda: [self.set_prices(low_price.get(), high_price.get()), self.filterate( game_frame, scrollable, search_frame) ])
        gift_lbl = tb.Label(parent, text="Activate a Product")
        gift_lbl.config(font=("Helvetica", 10))
        activate_btn = tb.Button(parent, text="Activate", bootstyle="success", command=lambda: self.run_gift_window())

        category_lbl.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
        category_drop.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        price_lbl.grid(row=2, column=0, padx=5, pady=(20,0), sticky="nsew")
        low_lbl.grid(row=3, column=0, padx=5,  pady=(10,0), sticky="nsew")
        high_lbl.grid(row=3, column=1, padx=5,  pady=(10,0), sticky="nsew")
        lower_entry.grid(row=4, column=0, padx=5, pady=(10,0), sticky="nsew")
        upper_entry.grid(row=4, column=1, padx=5, pady=(10,0), sticky="nsew")
        price_enter.grid(row=5, column=0, columnspan=2, padx=5, pady=(10,0), sticky="nsew")
        gift_lbl.grid(row=6, column=0, padx=5, pady=5, sticky="sew")
        activate_btn.grid(row=6, column=1, padx=5, pady=5, sticky="sew")
        
    def run_gift_window(self):
        gift_win = tb.Toplevel(self)
        gift_win.title("")
        gift_win.geometry('400x400')
        gift_win.minsize(400, 400)
        gift_win.maxsize(400,400)
        input = StringVar()

        lbl = tb.Label(gift_win, text="Enter your code.")
        lbl.config(font=("Helvetica", 12))
        en = tb.Entry(gift_win, textvariable=input)
        warning = tb.Label(gift_win, text="Invalid Code", bootstyle="danger")
        warning.config(font=("Helvetica", 10))
        confirm_btn = tb.Button(gift_win, text="Confirm", bootstyle="success", command=lambda: self.check_code(gift_win, warning, input.get()))

        lbl.grid(row=0, padx=5, pady=10,  column=0)
        en.grid(row=1, padx=5, pady=10, column=0)
        confirm_btn.grid(row=2, padx=5, pady=10, column=0)

    def check_code(self, parent, warning, input):
        game = self.store.validate_gift(input)
        if(game == None):
            warning.config(text="Invalid Code", bootstyle="danger")
        else:
            title = game["Title"]
            in_lib = self.user.check_inlibrary(title)
            if(in_lib == False):
                self.user.update_library(title)
                warning.config(text=title + " was added to your library", bootstyle="success")
            else:
                warning.config(text="Already in library", bootstyle="success")
            
        warning.grid(row=3, column=0, padx=5, pady=10)

    def set_category(self, selected):
        self.filters["Category"] =selected
        
    def set_prices(self,low,high):
        self.filters["lowest_price"] = low
        self.filters["highest_price"]= high
    

    def generate_game_widgets(self, parent, frames, search_frame, scrollable):
        # Game widget locations
        """
            Generates the widgets for current pointers

            args:
            parent (tb.Frames), frames (tb.Frames), search_frame (tb.Frames), scrollable (tb.ScrollableFrames)
        
        """
        # Store Instances of window elements in this method to use outside scope
        self.search = search_frame
        self.parent = parent
        self.frames = frames
        self.scroll = scrollable

        game_widgets = []
        images = ["green.png"]

        j=0 
        frame = frames[0]
        l = 0
        for i in range(self.pointer_start, self.pointer_end):
            game_widget = tb.Frame(frame, bootstyle="bg")
            game_widget.grid(row=i+j, column=0, sticky="nsew", padx=5, pady=5)
            self.render_img(game_widget, images[0], 1, 0)
            title_temp = tb.Label(game_widget, text=self.games[i]["Title"])
            title_temp.config(font=("Helvetica", 12))
            title_temp.grid(row=0, column=0, padx=5, pady=5)
            tb.Label(game_widget, text=self.games[i]["Developer"]).grid(row=0, column=4, padx=5, pady=5)
            tb.Label(game_widget, text="$" + str(self.games[i]["Price"])).grid(row=1, column=1)
            tb.Label(game_widget, text= "Released: " + str(self.games[i]["Release_Date"])).grid(row=3, column=0)
            # Generate tags
            k =0
            for tag in (self.games[i]["Tags"]):
                tb.Label(game_widget, bootstyle="light", text=tag).grid(row=2, column=2+k, padx=5, pady=(0, 10))
                k += 1
            tb.Button(game_widget, text="View", bootstyle="primary", command= lambda i=i: [print(self.games[i]), self.preview_game(i, search_frame, parent, scrollable)]).grid(row=1, column=4, padx=5)
            tb.Button(game_widget, text="Add to Cart", bootstyle="primary", command= lambda i=i: [self.add_to_cart(self.games[i]), self.update_cart_button(search_frame, parent, scrollable)]).grid(row=1, column=3, padx=5)
            game_widgets.append(game_widget)
            j += 1
            #alternating between frames 
            if((j%2) == 1):
                frame = frames[1]
            else:
                frame = frames[0]
            if(l < 2):
                l += 1


    
    def preview_game(self, game_id, search_frame, game_frame, scrollable):
        """
            Displays the frames to display game details

            args:
            game_date_or_id (String), search_frame (tb.Frame), game_frame (tb.Frame), scrollable (tb.ScrollableFrame)
        """

        if isinstance(game_id, int):
            game_date = self.games[game_id]
        else:
            game_date = game_id

        self.game_date_or_id = game_id

        #render_img(self, frame, path, r, c)
        fill = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Cursus in hac habitasse platea dictumst quisque sagittis purus sit. Viverra justo nec ultrices dui. Fermentum odio eu feugiat pretium nibh ipsum. Scelerisque mauris pellentesque pulvinar pellentesque habitant. Commodo sed egestas egestas fringilla phasellus. Quis eleifend quam adipiscing vitae proin. Augue mauris augue neque gravida in fermentum et sollicitudin. Varius vel pharetra vel turpis nunc. Orci phasellus egestas tellus rutrum tellus pellentesque eu. Sollicitudin tempor game_date_or_id eu nisl nunc mi ipsum faucibus. Nulla aliquet enim tortor at auctor urna nunc. Eu feugiat pretium nibh ipsum consequat nisl vel pretium lectus. Sodales ut eu sem integer vitae justo. Odio pellentesque diam volutpat commodo sed egestas egestas fringilla phasellus. Sit amet est placerat in egestas erat imperdiet sed. Sed arcu non odio euismod. Lorem ipsum dolor sit amet consectetur adipiscing elit. Donec ac odio tempor orci dapibus. Vulputate eu scelerisque felis imperdiet proin fermentum."
        game_frame.destroy()
        self.destroy_frames(search_frame)
        back_btn = tb.Button(search_frame, text="Back", bootstyle="outline", command=lambda: [self.destroy_frames(search_frame), self.setup_layout()])
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
        self.render_img(banner_frame, "pong/banner.png", 0, 0)
        describe_frame.grid(row=0, column=0, sticky="nsew")
        describe_frame.insert(END, fill)
        support_frame.grid(row=0, column=1,sticky="nsew")

        title = tb.Label(game_title, text = self.games[game_id]["Title"])
        title.config(font=("Helvetica", 20))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        #Support frame filler
        tag_lbl = tb.Label(support_frame, text="Tags: ")
        tag_lbl.config(font=("Helvetica", 10))
        tag_lbl.grid(row=0, column=0, padx=5, pady=(0, 10))
        i = 1
        for tag in (self.games[game_id]["Tags"]):
            temp_tag = tb.Label(support_frame, text=tag, bootstyle="light")
            temp_tag.config(font=("Courier", 10))
            temp_tag.grid(row=0, column=0+i, padx=5, pady=(0, 10))
            i += 1
        
        release_lbl = tb.Label(support_frame, text="Release Date: " )
        release_lbl.config(font=("Helvetica", 10))
        release_lbl.grid(row=1, column=0, padx=5,  pady=(0, 10))
        date_lbl = tb.Label(support_frame, text=str(self.games[game_id]["Release_Date"]))
        date_lbl.config(font=("Courier", 10))
        date_lbl.grid(row=1, column=1, padx=5,  pady=(0, 10))

        cart_btn = tb.Button(support_frame, text="Add to Cart", bootstyle="success", command=lambda: [self.add_to_cart(self.games[game_id]), self.setup_layout()])
        cart_btn.grid(row=2, column=1, padx=5,  pady=(0, 10), columnspan = 2, sticky="ns")

    def load_window_elem(self, game_id):
        game_id_elem = game_id
        search_elem = self.search
        parent_elem = self.parent
        scroll_elem = self.scroll

        # Check for game title and return the ID
        for game in self.games:
            if game["Title"] == game_id_elem:
                game_index = game["ID"] - 1
                try:
                    print(f"Loading store page for: {game_id_elem}")
                    self.preview_game(game_index, search_elem, parent_elem, scroll_elem)
                except Exception as e:
                    print(f"Game with title '{game_id_elem}' not found.")
                    print(f"Unable to load game page: {e}")
                    return None
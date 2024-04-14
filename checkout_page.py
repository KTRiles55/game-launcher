from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image 
from store import *
from store_off import *
from store_tab import *
import math
from ttkbootstrap import Style

class checkout_page(tb.Frame):
    def __init__(self, parent, scrollable_frame, cart):
        super().__init__(parent)
        self.parent = parent
        self.cart = cart


        self.grid()
        self.setup_layout(scrollable_frame)

    def render_img(self, frame, path, r, c):
        #Must prevent garbarge collection
        img_obj =  ImageTk.PhotoImage(Image.open("images/" + path))
        img_lbl = tb.Label(frame, image=img_obj)
        img_lbl.image = img_obj
        img_lbl.grid(row=r, column=c, padx=20)

    
    def destroy_frames(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def remove_game(self, title):
        for i in range(len(self.cart)):
            if(self.cart[i]["Title"] == title):
                self.cart.pop(i) 
                break

        if(len(self.cart) == 0):
            self.run_store()

        

    def run_store(self):
        self.destroy()
        self.parent.setup_layout()

    def setup_layout(self, scrollable):
        scrollable.rowconfigure(0, weight=1)
        scrollable.rowconfigure(1, weight=1)
        scrollable.rowconfigure(2, weight=1)
        scrollable.columnconfigure(0, weight=1)
        scrollable.config( bootstyle="secondary")
        self.grid(sticky="nsew")
        scrollable.grid(sticky="nsew")
        navigate_frame = tb.Frame( scrollable, bootstyle="bg")
        title_frame = tb.Frame(scrollable,  bootstyle="bg")
        #splits preview into to two
        preview_frame = tb.Frame( scrollable, bootstyle="secondary")
        game_frame = tb.Frame(preview_frame, bootstyle="secondary")
        order_frame = tb.Frame(preview_frame, bootstyle="bg")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        navigate_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.grid(row=1, column=0, sticky="nsew")
        preview_frame.grid(row=2, column=0, sticky="nsew")

        
        
        game_frame.grid(row=0, column=0, sticky="nsew")
        order_frame.grid(row=0, column=1, sticky="nsew")

        self.setup_title(title_frame, "Shopping Cart")
        self.setup_navigation(navigate_frame)
        self.setup_preview(preview_frame, game_frame, order_frame, title_frame)



    def setup_title(self, parent, title):
        cart_lbl = tb.Label(parent, bootstyle="success")
        cart_lbl.config(font=("Helvetica", 18), text=title)
  
        
        cart_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


    def setup_navigation(self, parent):
        back_btn = tb.Button(parent, text="Back", command= lambda: self.run_store())

        back_btn.grid(sticky="w") 
    
    def setup_preview(self,parent, game_frame, order_frame, title_frame):
        self.generate_cart(game_frame, order_frame, title_frame)
        self.generate_total(order_frame)

    def calculate_subtotal(self):
        total = 0
        for i in range(0, len(self.cart)):
            total +=  self.cart[i]["Price"]
        return round(total,2)

    def generate_total(self, frame):
        
        order_title = tb.Label(frame, text="Order Summary")
        order_title.config(font=("Helvetica", 18))

        subtotal_lbl = tb.Label(frame, text="Subtotal")
        subtotal_lbl.config(font=("Helvetica", 12))

        subtotal = str(self.calculate_subtotal())
        subtotal_val = tb.Label(frame, text="$" +subtotal)
        subtotal_val.config(font=("Helvetica", 12))

        order_title.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        subtotal_lbl.grid(row=1, column=0,  padx=10, pady=5, sticky="nsew")
        subtotal_val.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        

    def generate_cart(self, frame, order_frame, title_frame):
        game_widgets = []
        images = ["green.png"]
        count = 0

        items_num = len(self.cart)
        for i in range(items_num):
            game_widget = tb.Frame(frame, bootstyle="bg")
            game_widget.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            self.render_img(game_widget, images[0], 1, 0)
            title_temp = tb.Label(game_widget, text=self.cart[i]["Title"])
            title_temp.config(font=("Helvetica", 12))
            title_temp.grid(row=0, column=0, padx=5, pady=5)
            tb.Label(game_widget, text=self.cart[i]["Developer"]).grid(row=0, column=5, padx=5, pady=5)
            tb.Label(game_widget, text="$" + str(self.cart[i]["Price"])).grid(row=1, column=1)
            tb.Button(game_widget, text="Remove", bootstyle="success", command=lambda i=i: [print(self.cart), self.remove_game(self.cart[i]["Title"]), self.destroy_frames(order_frame), self.generate_total(order_frame), self.destroy_frames(frame), self.generate_cart(frame, order_frame, title_frame)]).grid(row=2, column=2, padx=5, pady=5)
            game_widgets.append(game_widget)
            count += 1
        
        next_btn = tb.Button(frame, text="Next",  command= lambda: self.display_payment_entries(frame, title_frame), bootstyle="success")
        next_btn.grid(row=count, column=1, sticky="nsew", padx=5, pady=5)

    
    def display_payment_entries(self, parent, title_frame):
        self.destroy_frames(parent)
        self.destroy_frames(title_frame)
        self.setup_title(title_frame, "Payment Method")
        parent.config(bootstyle="bg")
        fname_lbl = tb.Label(parent, text="First Name", bootstyle="bg")
        fname_lbl.configure(font=("Helvetica", 12))
        lname_lbl = tb.Label(parent, text="Last Name", bootstyle="bg")
        lname_lbl.configure(font=("Helvetica", 12))
        fname_en = tb.Entry(parent)
        lname_en = tb.Entry(parent)

        fname_lbl.grid(row=0, column=0, padx=5, sticky="nsw")
        lname_lbl.grid(row=0, column=1, padx=5, sticky="nsw")
        fname_en.grid(row=1, column=0, padx=5,sticky="nsw")
        lname_en.grid(row=1, column=1, padx=5, sticky="nsw")


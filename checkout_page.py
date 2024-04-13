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

    def run_store(self):
        self.destroy()
        self.parent.setup_layout()

    def setup_layout(self, scrollable):
        scrollable.rowconfigure(0, weight=1)
        scrollable.columnconfigure(0, weight=1)
        scrollable.grid(sticky="nsew")
        navigate_frame = tb.Frame( scrollable, bootstyle="bg")

        #splits preview into to two
        preview_frame = tb.Frame( scrollable, bootstyle="secondary")
        game_frame = tb.Frame(preview_frame, bootstyle="secondary")
        order_frame = tb.Frame(preview_frame, bootstyle="secondary")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        navigate_frame.grid(row=0, column=0, sticky="nsew")
        preview_frame.grid(row=1, column=0, sticky="nsew")

        
        
        game_frame.grid(row=0, column=0, sticky="nsew")
        order_frame.grid(row=0, column=1, sticky="nsew")

        self.setup_navigation(navigate_frame)
        self.setup_preview(preview_frame, game_frame, order_frame)

    def render_img(self, frame, path, r, c):
        #Must prevent garbarge collection
        img_obj =  ImageTk.PhotoImage(Image.open("images/" + path))
        img_lbl = tb.Label(frame, image=img_obj)
        img_lbl.image = img_obj
        img_lbl.grid(row=r, column=c, padx=20)

    def setup_navigation(self, parent):
        back_btn = tb.Button(parent, text="Back", command= lambda: self.run_store())

        back_btn.grid(sticky="w") 
    
    def setup_preview(self,parent, game_frame, order_frame):
        self.generate_cart(game_frame)
        self.generate_total(order_frame)

    def calculate_subtotal(self):
        total = 0
        for i in range(0, len(self.cart)):
            total += self.cart[i]["Count"] * self.cart[i]["Price"]
        return round(total,2)

    def generate_total(self, frame):
        
        title = tb.Label(frame, text="Order Summary")
        title.config(font=("Helvetica", 18))

        subtotal_lbl = tb.Label(frame, text="Subtotal")
        subtotal_lbl.config(font=("Helvetica", 12))

        subtotal = str(self.calculate_subtotal())
        subtotal_val = tb.Label(frame, text=subtotal)
        subtotal_val.config(font=("Helvetica", 12))

        title.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        subtotal_lbl.grid(row=1, column=0,  padx=10, pady=5, sticky="nsew")
        subtotal_val.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        

    def generate_cart(self, frame):
        game_widgets = []
        images = ["green.png"]

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
            tb.Label(game_widget, text="Count: " + str(self.cart[i]["Count"])).grid(row=2, column=1)
            game_widgets.append(game_widget)

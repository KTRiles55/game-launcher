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
        self.init_purchase_types()
        #print(self.cart)

    def change_copy_status(self, game, status):
        #"Digital Copy", "Hard Copy"
        if(status == "Digital Copy"):
            game["Digital_Copy"] = True
        else: 
            game["Digital_Copy"] = False
        #print(self.cart)

    def change_recipient(self, game, status):
        #"For myself", "As a gift"]
        if(status == "For myself"):
            game["For_Myself"] = True
        else:
            game["For_Myself"] = False
        #print(self.cart)

    def init_purchase_types(self):
        #default initializes purchase type to digital and for myself
        for i in range(len(self.cart)):
            if (self.cart[i].get("Digital_Copy") == None):
                self.cart[i]["Digital_Copy"] = True
            if (self.cart[i].get("For_Myself") == None):
                self.cart[i]["For_Myself"] = True

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
        order_frame = tb.LabelFrame(preview_frame)
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
        self.preview_cart(game_frame, order_frame, title_frame)
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

        

    def preview_cart(self, frame, order_frame, title_frame):
        type = ["Digital Copy","Digital Copy", "Hard Copy"]
        recipient = ["For myself","For myself", "As a gift"]
        game_widgets = []
        images = ["green.png"]
        count = 0

        items_num = len(self.cart)
    
        for i in range(items_num):
            selected_recipient = StringVar()
            selected_copy = StringVar()
            game_widget = tb.Frame(frame, bootstyle="bg")
            game_widget.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            self.render_img(game_widget, images[0], 1, 0)
            title_temp = tb.Label(game_widget, text=self.cart[i]["Title"])
            title_temp.config(font=("Helvetica", 12))
            title_temp.grid(row=0, column=0, padx=5, pady=5)
            tb.Label(game_widget, text=self.cart[i]["Developer"]).grid(row=0, column=5, padx=5, pady=5)
            tb.Label(game_widget, text="$" + str(self.cart[i]["Price"])).grid(row=1, column=1)
            c = i
            recipient_options = tb.OptionMenu(game_widget, selected_recipient, *recipient, bootstyle="outline", command=lambda i=i: self.change_recipient(self.cart[c], selected_recipient.get()))
            copy_type_options = tb.OptionMenu(game_widget,selected_copy, *type, bootstyle="outline", command=lambda i=i: self.change_copy_status(self.cart[c], selected_copy.get()))
            recipient_options.grid(row=2, column=2, sticky="nse", padx=10)
            copy_type_options.grid(row=2, column=3, sticky="nse", padx=10)

            tb.Button(game_widget, text="Remove", bootstyle="success", command=lambda i=i: [print(self.cart), self.remove_game(self.cart[i]["Title"]), self.destroy_frames(order_frame), self.generate_total(order_frame), self.destroy_frames(frame), self.preview_cart(frame, order_frame, title_frame)]).grid(row=1, column=2, padx=5, pady=5)
            game_widgets.append(game_widget)
            count += 1
        
        next_btn = tb.Button(frame, text="Continue",  command= lambda: self.display_payment_entries(frame, title_frame), bootstyle="success")
        next_btn.grid(row=count, column=0, sticky="nsew", padx=5, pady=5)

    
    def display_payment_entries(self, parent, title_frame):
        
        months = ["--","01", "02","03","04","05","06","07","08","09","10","11","12"]
        years = ["----"]
        countries = ["United States", "Canada"]
        states = ["California"]
        for i in range (2024, 2050):
            years.append(i)
        selected_month = StringVar()
        selected_year = StringVar()
        selected_countries = StringVar()
        selected_state = StringVar()
        self.destroy_frames(parent)
        self.destroy_frames(title_frame)
        self.setup_title(title_frame, "Payment Method")
        parent.config(bootstyle="bg")

        #Setup frame entry
        bill_frame = tb.LabelFrame(parent, text="Billing Information")
        pay_frame = tb.LabelFrame(parent, text="Payment Information")
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)

        #Customize payment frame
        card_lbl = tb.Label(pay_frame, text="Card number")
        card_lbl.configure(font=("Helvetica", 10))
        card_en = tb.Entry(pay_frame)
        expire_lbl = tb.Label(pay_frame, text="Expiration date")
        expire_lbl.configure(font=("Helvetica", 10))
        expire_month_en = tb.OptionMenu(pay_frame, selected_month, *months, bootstyle="outline")
        expire_year_en = tb.OptionMenu(pay_frame, selected_year, *years, bootstyle="outline")
        secure_num_lbl = tb.Label(pay_frame, text="Security Code")
        secure_num_en = tb.Entry(pay_frame)


        #Customize billing frame
        fname_lbl = tb.Label(bill_frame, text="First Name", bootstyle="bg")
        fname_lbl.configure(font=("Helvetica", 10))
        lname_lbl = tb.Label(bill_frame, text="Last Name", bootstyle="bg")
        lname_lbl.configure(font=("Helvetica", 10))
        fname_en = tb.Entry(bill_frame)
        lname_en = tb.Entry(bill_frame)
        city_lbl = tb.Label(bill_frame, text="City", bootstyle="bg")
        city_lbl.configure(font=("Helvetica", 10))
        address_lbl = tb.Label(bill_frame, text="Address", bootstyle="bg")
        address_lbl.configure(font=("Helvetica", 10))
        state_lbl = tb.Label(bill_frame, text="State", bootstyle="bg")
        state_lbl.configure(font=("Helvetica", 10))
        zip_lbl = tb.Label(bill_frame, text="Zip Code", bootstyle="bg")
        zip_lbl.configure(font=("Helvetica", 10))
        country_lbl = tb.Label(bill_frame, text="Country", bootstyle="bg")
        country_lbl.configure(font=("Helvetica", 10))
        city_en = tb.Entry(bill_frame)
        address_en = tb.Entry(bill_frame)
        zip_en = tb.Entry(bill_frame)
        country_en = tb.OptionMenu(bill_frame, selected_countries, *countries, bootstyle="outline")
        state_en = tb.OptionMenu(bill_frame, selected_state, *states, bootstyle="outline")
        next_btn = tb.Button(bill_frame,text="Continue", command=lambda: [self.destroy_frames(parent),self.setup_title(title_frame, "Purchase complete. Thank you!"), self.display_receipt(parent,title_frame)], bootstyle="success")

        #Layout payment frame
        pay_frame.grid(row=0, column=0,  pady=10, sticky="nsew")
        card_lbl.grid(row=0, column=0, padx=5, sticky="nsw")
        card_en.grid(row=1, column=0, padx=5, pady=(0,10),sticky="nsw")
        expire_lbl.grid(row=0, column=1, padx=10, sticky="nsew")
        expire_month_en.grid(row=1, column=1, padx=10,  sticky="nsew")
        expire_year_en.grid(row=1, column=2, padx=10, sticky="nsw")
        secure_num_lbl.grid(row=0, column=3, padx=10, sticky="nsw")
        secure_num_en.grid(row=1, column=3, padx=10, sticky="nse")

        #Layout billing frame
        bill_frame.grid(row=1, column= 0, pady=10, sticky="nsew")
        fname_lbl.grid(row=0, column=0, padx=20, sticky="nsw")
        lname_lbl.grid(row=0, column=1, padx=20, sticky="nsw")
        fname_en.grid(row=1, column=0, padx=20,sticky="nsew")
        lname_en.grid(row=1, column=1, padx=20, sticky="nsew")

        city_lbl.grid(row=2, column=0, padx=20,pady=(15,0), sticky="nsw")
        address_lbl.grid(row=2, column=1, padx=20,pady=(15,0), sticky="nsw")
        city_en.grid(row=3, column=0, padx=20,pady=(0,15), sticky="nsew")
        address_en.grid(row=3, column=1, padx=20,pady=(0,15), sticky="nsew")

        state_lbl.grid(row=4, column=0, padx=20,pady=(15,0), sticky="nsw")
        zip_lbl.grid(row=4, column=1, padx=20,pady=(15,0), sticky="nsw")
        state_en.grid(row=5, column=0, padx=20,pady=(0,15), sticky="nsew")
        zip_en.grid(row=5, column=1, padx=20,pady=(0,15), sticky="nsew")

        country_lbl.grid(row=6, column=0, padx=20,pady=(15,0), sticky="nsw")
        country_en.grid(row=7, column=0, padx=20,pady=(0,15), sticky="nsew")

        next_btn.grid(row=8, column=1, padx=20, pady=20, sticky="nse")

 
    def display_receipt(self, parent, title_frame):
        game_widgets = []
        images = ["green.png"]
        code = "123-4567-890"
        count = 0
        title = tb.Label(parent, text="Your purchases.")
        title.configure(font=("Helvetica", 16))
        title.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        items_num = len(self.cart)
        #Displays game and code if gift option
        for i in range(0, items_num):
            selected_recipient = StringVar()
            selected_copy = StringVar()
            game_widget = tb.Frame(parent, bootstyle="bg")
            game_widget.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)
            self.render_img(game_widget, images[0], 1, 0)
            title_temp = tb.Label(game_widget, text=self.cart[i]["Title"])
            title_temp.config(font=("Helvetica", 12))
            title_temp.grid(row=0, column=0, padx=5, pady=5)
            if(self.cart[i]["For_Myself"] == False):
                code_temp = tb.Label(game_widget, text="Code: " + code,bootstyle="light")
                code_temp.config(font=("Helvetica", 12))
                code_temp.grid(row=i+3, column=0, sticky="nsew", padx=5, pady=5)

        #Empties cart
        self.cart.clear()
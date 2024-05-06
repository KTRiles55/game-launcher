from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image 
from store import *
from LibraryTab import *
from store_tab import *
import user
import string
import random
import math
from ttkbootstrap import Style

class checkout_page(tb.Frame):
    def __init__(self, parent, scrollable_frame, cart, user):
        super().__init__(parent)
        self.parent = parent
        self.cart = cart
        self.user = user
        self.purchase_status = False
        self.store = store()
        self.init_purchase_types()

        self.grid()
        self.setup_layout(scrollable_frame)
        
        #print(self.cart)

    def change_copy_status(self, game, status):
        #type = ["Digital Copies","Digital Copies", "Hard Copies"]
        #recipient = ["For myself","For myself", "As gifts"]
        if(status == "Digital Copies"):
            game["Digital_Copy"] = True
        else: 
            game["Digital_Copy"] = False
        

    def change_recipient(self, game, status):
        title = game["Title"]
        if(status == "For myself"):
            if(self.user.check_inlibrary(title) == True):
                game["For_Myself"] = True
            else:
                game["For_Myself"] = False
                print("A game is already your library")
        else:
            game["For_Myself"] = False
        
        
    def init_purchase_types(self):
        #default initializes purchase type to digital and for myself
        for i in range(len(self.cart)):
            self.cart[i]["Digital_Copy"] = True
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
        if(self.purchase_status == True):
            self.parent.reset_cart()
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
        type = ["Digital Copies","Digital Copies", "Hard Copies"]
        recipient = ["For myself","For myself", "As gifts"]
        game_widgets = []
        images = ["green.png"]
        selection = []
        for i in range(len(self.cart)):
            selection.append("For myself")
        #Counter for number of widgets, to place continue
        row_count = 0

        items_num = len(self.cart)
        selected_recipient = StringVar()
        selected_copy = StringVar()
        
        for i in range(items_num):
            selected_recipient = StringVar()
            selected_copy = StringVar()
            if(self.cart[i]["For_Myself"] == False):
                selected_copy.set("As gifts")
            game_widget = tb.Frame(frame, bootstyle="bg")
            game_widget.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            self.render_img(game_widget, images[0], 1, 0)
            title_temp = tb.Label(game_widget, text=self.cart[i]["Title"])
            title_temp.config(font=("Helvetica", 12))
            title_temp.grid(row=0, column=0, padx=5, pady=5)
            tb.Label(game_widget, text=self.cart[i]["Developer"]).grid(row=0, column=5, padx=5, pady=5)
            tb.Label(game_widget, text="$" + str(self.cart[i]["Price"])).grid(row=1, column=1)
            recipient_options = tb.OptionMenu(game_widget, selected_recipient, *recipient, bootstyle="outline", command=lambda  recipient, i=i: self.change_recipient(self.cart[i], recipient))
            #copy_type_options = tb.OptionMenu(game_widget, selected_copy, *type, bootstyle="outline", command=lambda type, i=i: self.change_copy_status(self.cart[i], type))
            recipient_options.grid(row=2, column=1, sticky="nse", padx=10)
            #copy_type_options.grid(row=2, column=2, sticky="nse", padx=10)
            #selected_recipient.set("For myself")
            #selected_copy.set("Digital Copies")

            tb.Button(game_widget, text="Remove", bootstyle="success", command=lambda i=i: [ self.remove_game(self.cart[i]["Title"]), self.destroy_frames(order_frame), self.generate_total(order_frame), self.destroy_frames(frame), self.preview_cart(frame, order_frame, title_frame)]).grid(row=1, column=2, padx=5, pady=5)
            game_widgets.append(game_widget)
            row_count += 1
        
        
        next_btn = tb.Button(frame, text="Continue",  command= lambda: [print(self.cart), self.check_cartinfo(row_count, frame, title_frame)], bootstyle="success")
        next_btn.grid(row=row_count, column=0, sticky="nsew", padx=5, pady=10)
    
    def check_cartinfo(self,row_count, frame, title_frame):
        for i in range(len(self.cart)):
            game = self.cart[i]
            title = game["Title"]
            print(title)
            if((self.user.check_inlibrary(title) == True) and (game["For_Myself"] == True)):
                warn_lbl = tb.Label(frame, text="You own a game in the cart. Gift it to continue.")
                warn_lbl.config(font=("Courier", 10), bootstyle="danger")
                warn_lbl.grid(row=row_count+1, column=0)
                print("Game owned")
                return

        self.display_payment_entries(frame, title_frame)
    
    def display_payment_entries(self, parent, title_frame):
        
        months = ["--","01", "02","03","04","05","06","07","08","09","10","11","12"]
        years = ["----"]
        countries = ["United States", "United States","Canada"]
        states = ["California", "California",]
        for i in range (2024, 2050):
            years.append(i)
        card_num = StringVar()
        expire_month = StringVar()
        expire_year = StringVar()
        country = StringVar()
        state = StringVar()
        fname = StringVar()
        lname = StringVar()
        address = StringVar()
        zip = StringVar()
        city = StringVar()
        secure_num = StringVar()
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
        card_en = tb.Entry(pay_frame, textvariable=card_num)
        expire_lbl = tb.Label(pay_frame, text="Expiration date")
        expire_lbl.configure(font=("Helvetica", 10))
        expire_month_en = tb.OptionMenu(pay_frame, expire_month, *months, bootstyle="outline")
        expire_year_en = tb.OptionMenu(pay_frame, expire_year, *years, bootstyle="outline")
        secure_num_lbl = tb.Label(pay_frame, textvariable=secure_num, text="Security Number")
        secure_num_en = tb.Entry(pay_frame)


        #Customize billing frame
        fname_lbl = tb.Label(bill_frame, text="First Name", bootstyle="bg")
        fname_lbl.configure(font=("Helvetica", 10))
        lname_lbl = tb.Label(bill_frame, text="Last Name", bootstyle="bg")
        lname_lbl.configure(font=("Helvetica", 10))
        fname_en = tb.Entry(bill_frame, textvariable=fname)
        lname_en = tb.Entry(bill_frame, textvariable=lname)
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
        city_en = tb.Entry(bill_frame, textvariable=city)
        address_en = tb.Entry(bill_frame, textvariable=address)
        zip_en = tb.Entry(bill_frame, textvariable=zip)
        country_en = tb.OptionMenu(bill_frame, country, *countries, bootstyle="outline")
        state_en = tb.OptionMenu(bill_frame, state, *states, bootstyle="outline")
        warning_lbl = tb.Label(bill_frame, text="An entry is missing", bootstyle="danger")
        warning_lbl.config(font=("Courier", 10))
        next_btn = tb.Button(bill_frame, text="Continue",  command= lambda: self.check_entries( parent, title_frame, entries, warning_lbl), bootstyle="success")

        #Layout payment frame
        pay_frame.grid(row=0, column=0,  pady=10, sticky="nsew")
        card_lbl.grid(row=0, column=0, padx=5, sticky="nsw")
        card_en.grid(row=1, column=0, padx=5, pady=(0,10),sticky="nsw")
        expire_lbl.grid(row=0, column=1, padx=10, sticky="nsew")
        expire_month_en.grid(row=1, column=1, padx=10,  sticky="nsew")
        expire_year_en.grid(row=1, column=2, padx=10, sticky="nsw")
        secure_num_lbl.grid(row=0, column=2, padx=10, sticky="nsw")
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
        next_btn.grid(row=9, column=1, padx=20, pady=20, sticky="nse")

        entries = [card_num,
        expire_month,
        expire_year,
        country,
        state,
        fname,
        lname,
        address,
        zip,
        city]
        



    def check_entries(self, parent, title_frame, entries, warning_lbl):
        #Only checks if empty
        for entry in enumerate(entries):
            #entry is in tuple form
            if len(entry[1].get()) == 0:
                warning_lbl.grid(row=8, column=1, padx=20, pady=20, sticky="nse") 
                return
        self.destroy_frames(parent)
        self.setup_title(title_frame, "Purchase complete. Thank you!")
        self.display_receipt(parent,title_frame)
 
    def generate_giftcodes(self):
        for i in range(len(self.cart)):
            #Length of code
            N = 7
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
            if(self.cart[i]["For_Myself"] == False):
                self.cart[i]["Code"] = code
            else:
                self.cart[i]["Code"] = None

    def display_receipt(self, parent, title_frame):
        game_widgets = []
        images = ["green.png"]
        count = 0
        title = tb.Label(parent, text="Your purchases.")
        title.configure(font=("Helvetica", 16))
        title.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.generate_giftcodes()
        

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
                code_temp = tb.Label(game_widget, text="Gift Code: " + self.cart[i]["Code"],bootstyle="light")
                code_temp.config(font=("Helvetica", 12))
                code_temp.grid(row=i+3, column=0, sticky="nsew", padx=5, pady=5)

        print(self.cart)
        #Empties cart
        for i in range(len(self.cart)):
            item = self.cart[i]
            print("(-) " + item["Title"])
            if(item["For_Myself"] == True):
                title = item["Title"]
                print(title + "added to library")
                self.user.update_library(title)
            else:
                code = item["Code"]    
                title = item["Title"]
                self.store.append_codes(title, code)

        self.cart = []
        self.purchase_status = True

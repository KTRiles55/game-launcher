from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap import Style, Label
from ttkbootstrap.constants import *
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFilter

class ProfileTab(tb.Frame):
    def __init__(self,parent):  
        super().__init__(parent)
        self.parent = parent
        self.profileFrame = tb.Frame(self)
        self.profileFrame.pack(expand=True, fill="both")
        
        # converts image into profile sprite
        with Image.open("cat.jpg").convert("RGBA") as profile:
             profile = profile.resize((240, 200)) 
             sprite = self.createSprite(profile)   
             sprite = sprite.resize((400, 340))
             icon = ImageTk.PhotoImage(sprite)
             profileLbl = tb.Label(self.profileFrame, image=icon, borderwidth=20)
             profileLbl.image = icon
             profileLbl.grid(row=3, column=3)
        
        accountNameLbl = tb.Label(self.profileFrame, text="MewMaster34", font=("Verdana", "25", "bold"), foreground="#ffffff")
        accountNameLbl.grid(row=4,column=3)
        friends = { "Fred", "Billy", "Joel", "Ned", "Sally" }
        self.loadFriendWidget(friends, self.profileFrame)
        
        # add bio widget
        bioFrame = tb.Frame(self.profileFrame, width=60, height=40)
        bioFrame.grid(row=3, column=4)
        bioText = tb.Text(bioFrame, width=40, height=10, font=("Verdana", "13"))
        bioLbl = tb.Label(bioFrame, text="About Me", font=("Verdana", "20", "bold"), anchor='w', foreground='#ffffff')
        bioText.configure(bg='#000000', fg='#ffffff')
        bioLbl.pack()
        bioText.pack()
       
             
    def createSprite(self, image):
        # Crops image into circular sprite format

        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((20, 0, 220, 200), 255)
        n_sprite = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        n_sprite.putalpha(mask)
        
        return n_sprite
        

    def loadFriendWidget(self, friends, frame):
        # generate widget for friend list
        
        friendsWidget = tb.Frame(frame, height=200, width=100, borderwidth=10)
        friendsWidget.grid(row=3, column=5, sticky="nsew")
        friendsScroll = tb.Scrollbar(friendsWidget, orient="vertical", bootstyle = "secondary")
        
        searchStyle = tb.Style()
        searchStyle.configure('search.TEntry', fieldbackground='#000000', bootstyle='dark')
        friendSearchEn = tb.Entry(friendsWidget, width=35, foreground='#ffffff', style='search.TEntry')
        friendSearchEn.pack() 
        
        searchIcon = ImageTk.PhotoImage(Image.open("search.png").convert("RGBA").resize((20, 20)))
        searchWidget = tb.Button(friendSearchEn, image=searchIcon, bootstyle='dark')
        searchWidget.image = searchIcon
        searchWidget.place(relx=0.83, rely=0)        

        friendsScroll.pack(side=LEFT, fill=Y) 
        friends = { "Fred", "Billy", "Joel", "Ned", "Sally" } 
        self.listFriends(friendsWidget, friendsScroll, friends)
        
        friendListLbl = tb.Label(frame, text="Friends", font=("Verdana", "20", "bold"), foreground="#ffffff")
        friendListLbl.grid(row=2, column=5)
        

    def listFriends(self, widget, scroll_bar, friends):
        # add friends into list
        friendsList = Listbox(widget, yscrollcommand=scroll_bar.set)
        friendsList.configure(background="#000000", foreground="#ffffff", highlightbackground="#ffffff", font=("Verdana", "15", "bold"), width=12, borderwidth=20)
        for f in friends:
            friendsList.insert(END, f)
            
        friendsList.pack(side=LEFT, fill=Y)
        scroll_bar.config(command=friendsList.yview)
      


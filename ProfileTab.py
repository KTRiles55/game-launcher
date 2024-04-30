import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap import Label, Style
from user import user
from ttkbootstrap.constants import *
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFilter
import os

class ProfileTab(tb.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user

        # Create main frame
        self.main_frame = tb.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Create profile frame
        self.profile_frame = tb.Frame(self.main_frame)
        self.profile_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Load default image
        self.load_default_image()

        # Get Username
        self.current_user = self.user.get_username()

        # Add account name label
        self.accountNameLbl = tb.Label(self.profile_frame, text=self.current_user, font=("Verdana", "25", "bold"), foreground="#ffffff")
        self.accountNameLbl.pack(side=tk.TOP, padx=10, pady=10)

        # Add button to upload image
        upload_button = tb.Button(self.profile_frame, text="Upload Image", command=self.upload_image)
        upload_button.pack(side=tk.TOP, padx=10, pady=10)

        # Create about me frame
        self.about_me_frame = tb.Frame(self.main_frame)
        self.about_me_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add "About Me" label
        self.bioLbl = tb.Label(self.about_me_frame, text="About Me", font=("Verdana", "20", "bold"), anchor='w', foreground='#ffffff')
        self.bioLbl.pack(side=tk.TOP, anchor='w', padx=10, pady=(10, 0))

        # Add "About Me" text entry
        self.bioText = tb.Text(self.about_me_frame, width=40, height=10, font=("Verdana", "13"))
        self.bioText.configure(bg='#000000', fg='#ffffff')
        self.bioText.pack(side=tk.TOP, anchor='w', padx=10, pady=(0, 5))

        # Add button to save "About Me" text
        save_button = tb.Button(self.about_me_frame, text="Save", command=self.save_about_me)
        save_button.pack(side=tk.TOP, anchor='w', padx=10, pady=(0, 10))

        # Initialize about me label
        self.about_me_label = None

        # Create friends frame
        self.friends_frame = tb.Frame(self.main_frame)
        self.friends_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Add "Friends" label
        self.friendListLbl = tb.Label(self.friends_frame, text="Friends", font=("Verdana", "20", "bold"), foreground="#ffffff")
        self.friendListLbl.pack(side=tk.TOP, padx=10, pady=(10, 0))

        # Add friend list
        self.load_friend_widget()
        
        # Manage friend requests

        #self.user.sendFriendRequest("Tom")      // for testing
        friendRequests = self.user.listFriendRequests()
        friendIcon = ImageTk.PhotoImage(Image.open("images/friendIcon.png").convert('RGBA').resize((48, 40)))        
     
        fRequestBtn = tb.Button(self.friends_frame, image=friendIcon, bootstyle='dark', command = lambda: self.displayFriendRequests(friendRequests))
        fRequestBtn.image = friendIcon
        fRequestBtn.pack(side=tk.TOP, anchor='e', padx=10, pady=(0, 5))
        #self.displayFriendRequests(friendRequests)     // work in progress

    def load_default_image(self):
        # Load default image
        self.image_path = "images/profile.png"
        if os.path.exists(self.image_path):
            profile = Image.open(self.image_path).convert("RGBA")
        else:
            profile = Image.open("images/cat.jpg").convert("RGBA")
        profile = profile.resize((240, 200))
        sprite = self.create_sprite(profile)
        sprite = sprite.resize((400, 340))
        self.icon = ImageTk.PhotoImage(sprite)
        self.profileLbl = tb.Label(self.profile_frame, image=self.icon, borderwidth=20)
        self.profileLbl.image = self.icon
        self.profileLbl.pack(side=tk.TOP, padx=10, pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with Image.open(file_path).convert("RGBA") as profile:
                profile = profile.resize((240, 200))
                sprite = self.create_sprite(profile)
                sprite = sprite.resize((400, 340))
                self.icon = ImageTk.PhotoImage(sprite)
                self.profileLbl.config(image=self.icon)
                self.profileLbl.image = self.icon
                self.save_image(profile)

    def save_image(self, profile):
        profile.save(self.image_path)

    def create_sprite(self, image):
        # Crops image into circular sprite format
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((20, 0, 220, 200), 255)
        n_sprite = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        n_sprite.putalpha(mask)
        return n_sprite

    def load_friend_widget(self):
        # Add friend list
        self.friendsWidget = tb.Frame(self.friends_frame, height=200, width=100, borderwidth=10)
        self.friendsWidget.pack(side=tk.TOP, fill=tk.Y)

        # Add friend list scrollbar
        self.friendsScroll = tb.Scrollbar(self.friendsWidget, orient="vertical", bootstyle="secondary")
        self.friendsScroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add friend search entry
        self.friendSearchEn = tb.Entry(self.friendsWidget, width=35, foreground='#ffffff', style='search.TEntry')
        self.friendSearchEn.pack()

        # Add search button
        searchIcon = ImageTk.PhotoImage(Image.open("images/search.png").convert("RGBA").resize((20, 20)))
        searchWidget = tb.Button(self.friendSearchEn, image=searchIcon, bootstyle='dark')
        searchWidget.image = searchIcon
        searchWidget.place(relx=0.83, rely=0)

        # Add friend list box
        self.friendsList = tk.Listbox(self.friendsWidget, yscrollcommand=self.friendsScroll.set)
        self.friendsList.configure(background="#000000", foreground="#ffffff", highlightbackground="#ffffff", font=("Verdana", "15", "bold"), width=12, borderwidth=20)
        self.friendsList.pack(side=tk.LEFT, fill=tk.Y)
        self.friendsScroll.config(command=self.friendsList.yview)

        # Populate friend list with sample friends
        friends = self.user.getParsedFriendsList()
        for friend in friends:
            self.friendsList.insert(tk.END, friend)


    def displayFriendRequests(self, friendRequests):
        friendRequestWindow = tb.Toplevel(self, title='Friend Requests', size=(100, 200), minsize=(100, 200), maxsize=(100, 200), iconbitmap = "images/empty.ico", topmost=True)


    def save_about_me(self):
        about_me_text = self.bioText.get("1.0", tk.END).strip()
        if about_me_text:
            with open("about_me.txt", "w") as f:
                f.write(about_me_text)
                messagebox.showinfo("Success", "About Me saved successfully!")
                self.display_about_me(about_me_text)
                self.bioText.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please enter some text for About Me!")

    def display_about_me(self, about_me_text):
        # Destroy previous about me label if exists
        if self.about_me_label:
            self.about_me_label.destroy()

        # Add about me label
        self.about_me_label = tb.Label(self.about_me_frame, text=about_me_text, font=("Verdana", "13"), anchor='w', wraplength=300, justify=tk.LEFT)
        self.about_me_label.pack(side=tk.TOP, padx=10, pady=(0, 5))

def main():
    # Create the main window
    root = tk.Tk()  
    root.title("Profile")

    # Apply ttkbootstrap style
    style = Style(theme="darkly")

    # Create a notebook (tabbed interface)
    notebook = tb.Notebook(root)

    # Create the profile tab and add it to the notebook
    profile_tab = ProfileTab(notebook)
    notebook.add(profile_tab, text="Profile")

    # Pack the notebook and run the Tkinter event loop
    notebook.pack(expand=True, fill="both")
    root.mainloop()

if __name__ == "__main__":
    main()

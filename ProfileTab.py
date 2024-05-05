import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import ttkbootstrap as tb
from ttkbootstrap import Label, Style
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFilter
import os

class ProfileTab(tb.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.user_folder = f"userdata/{self.user.get_username()}"
        os.makedirs(self.user_folder, exist_ok=True)
        self.about_me_file = f"{self.user_folder}/about_me.txt"  # Unique file for each user
        self.image_path = f"{self.user_folder}/profile.png"  # Unique profile photo for each user
        self.friends_list_file = f"{self.user_folder}/friends_list.txt"

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

        # Load the "About Me" text when the application starts
        self.load_about_me()

        # Create friends frame
        self.friends_frame = tb.Frame(self.main_frame)
        self.friends_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Add "Friends" label
        self.friendListLbl = tb.Label(self.friends_frame, text="Friends", font=("Verdana", "20", "bold"), foreground="#ffffff")
        self.friendListLbl.pack(side=tk.TOP, padx=10, pady=(10, 0))

        # Add friend list
        self.load_friend_widget()

        # Add invite friend button
        self.add_invite_button()

        # Add add friend button
        self.add_friend_button()

    def load_default_image(self):
        # Load default image
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

    def save_about_me(self):
        about_me_text = self.bioText.get("1.0", tk.END).strip()
        if about_me_text:
            with open(self.about_me_file, "w") as f:
                f.write(about_me_text)
            messagebox.showinfo("Success", "About Me saved successfully!")
            self.display_about_me(about_me_text)
            self.bioText.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please enter some text for About Me!")

    def load_about_me(self):
        try:
            with open(self.about_me_file, "r") as f:
                about_me_text = f.read()
                self.display_about_me(about_me_text)
        except FileNotFoundError:
            pass  # No previous "About Me" text saved

    def display_about_me(self, about_me_text):
        # Destroy previous about me label if exists
        if self.about_me_label:
            self.about_me_label.destroy()

        # Add about me label
        self.about_me_label = tb.Label(self.about_me_frame, text=about_me_text, font=("Verdana", "13"), anchor='w', wraplength=300, justify=tk.LEFT)
        self.about_me_label.pack(side=tk.TOP, padx=10, pady=(0, 5))

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

        # Load friend list from file
        self.load_friends_list()

    def load_friends_list(self):
        try:
            with open(self.friends_list_file, "r") as f:
                for line in f:
                    self.friendsList.insert(tk.END, line.strip())
        except FileNotFoundError:
            pass  # No previous friends list saved

    def add_invite_button(self):
        # Add invite friend button
        invite_button = tb.Button(self.friendsWidget, text="Invite Friend", command=self.send_friend_invite)
        invite_button.pack(side=tk.TOP, padx=10, pady=(0, 10))

    def send_friend_invite(self):
        messagebox.showinfo("Friend Invite Sent", "Friend Invite Sent")

    def add_friend_button(self):
        # Add add friend button
        add_friend_button = tb.Button(self.friendsWidget, text="Add Friend", command=self.add_friend)
        add_friend_button.pack(side=tk.TOP, padx=10, pady=(0, 10))

    def add_friend(self):
        friend_name = simpledialog.askstring("Add Friend", "Enter the name of the friend:")
        if friend_name:
            confirm = messagebox.askyesno("Confirmation", f"Add {friend_name} as a friend?")
            if confirm:
                self.friendsList.insert(tk.END, friend_name)
                messagebox.showinfo("Success", f"{friend_name} added as a friend.")
                self.save_friends_list()  # Save the updated friend list
            else:
                messagebox.showinfo("Cancelled", "Friend addition cancelled.")

    def save_friends_list(self):
        friends = self.friendsList.get(0, tk.END)
        with open(self.friends_list_file, "w") as f:
            for friend in friends:
                f.write(friend + "\n")

def main():
    # Create the main window
    root = tk.Tk()  
    root.title("Profile")

    # Apply ttkbootstrap style
    style = Style(theme="darkly")

    # Create a notebook (tabbed interface)
    notebook = tb.Notebook(root)

    # Create the profile tab and add it to the notebook
    profile_tab = ProfileTab(notebook, user=None)  # No need to pass user argument here
    notebook.add(profile_tab, text="Profile")

    # Pack the notebook and run the Tkinter event loop
    notebook.pack(expand=True, fill="both")
    root.mainloop()

if __name__ == "__main__":
    main()

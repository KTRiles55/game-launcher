from store_tab import *
from LibraryTab import *
from SettingsTab import *
from ProfileTab import *


class Menu(tb.Frame):
    """
    Author: Narek Asaturyan
    Version: 1.3
    """
    def __init__(self, parent, page, username):
        super().__init__(parent)
        self.parent = parent
        self.user = username
        self.page = page

        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_widget()
        
    def create_widget(self):
        notebook_style = tb.Style()
        tab_style = tb.Style()
        tab_style.configure("TNotebook.Tab", font=("Unispace", "18", "bold"))
        notebook_style.configure("custom.TNotebook", padding=[0,0], tabmargins=[0,0,0,0], tabposition="nsew")
        self.notebook = tb.Notebook(self, style="custom.TNotebook")

        # Tabs
        self.library_tab = LibraryTab(self.notebook, self, self.user)
        self.store_tab = StoreTab(self.notebook, self.user)
        self.profile_tab = ProfileTab(self.notebook, self.user)  
        self.settings_tab = SettingsTab(self.notebook, self.page, self.parent) 

        # Adding Tabs
        self.notebook.add(self.library_tab, text="Library")
        self.notebook.add(self.store_tab, text="Store")
        self.notebook.add(self.profile_tab, text="Profile")
        self.notebook.add(self.settings_tab, text="Settings")

        self.notebook.pack(expand=True, fill=BOTH)
from store_tab import *
from FriendsTab import *
from LibraryTab import *
from SettingsTab import *



class Menu(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_widget()

    def create_widget(self):
        notebook_style = tb.Style()
        tab_style = tb.Style()
        tab_style.configure("TNotebook.Tab", font=("Unispace", "18", "bold"))
        notebook_style.configure("custom.TNotebook", padding=[0,0], tabmargins=[0,0,0,0], tabposition="nsew")
        notebook = tb.Notebook(self, style="custom.TNotebook")

        # Tabs
        friends_tab = FriendsTab(notebook)
        library_tab = LibraryTab(notebook)
        store_tab = StoreTab(notebook)
        settings_tab = SettingsTab(notebook)

        # Adding Tabs
        notebook.add(library_tab, text="Library")
        notebook.add(store_tab, text="Store")
        notebook.add(friends_tab, text="Friends")
        notebook.add(settings_tab, text="Settings")

        notebook.pack(expand=True, fill=BOTH)








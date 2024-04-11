from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import launcher
from ttkbootstrap.scrolled import ScrolledFrame
from store_tab import *
from PIL import ImageTk, Image


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
        home_tab = HomeTab(notebook)
        library_tab = LibraryTab(notebook)
        store_tab = StoreTab(notebook)
        settings_tab = SettingsTab(notebook)

        # Adding Tabs
        notebook.add(home_tab, text="Home")
        notebook.add(store_tab, text="Store")
        notebook.add(library_tab, text="Library")
        notebook.add(settings_tab, text="Settings")

        notebook.pack(expand=True, fill=BOTH)


class HomeTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent


class LibraryTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent



class SettingsTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent





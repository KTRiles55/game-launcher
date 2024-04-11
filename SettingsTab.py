from tkinter import *
from ttkbootstrap import Label
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import ImageTk, Image 
from ttkbootstrap import Style

class SettingsTab(tb.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
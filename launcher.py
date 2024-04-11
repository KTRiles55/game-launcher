from menu import *
from ctypes import windll, byref, sizeof, c_int


class Launcher(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("")
        self.geometry('1400x844')
        self.minsize(1400, 844)
        self.iconbitmap("images/empty.ico")

        # Applying the custom window attribute for the border color
        HWND = windll.user32.GetParent(self.winfo_id())
        DWMWA_ATTRIBUTE = 35
        COLOR = 0x201f1e
        windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

        # Widgets
        self.menu = Menu(self)

        # Run program
        self.mainloop()

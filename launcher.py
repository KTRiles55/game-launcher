from menu import *
from user import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class Launcher(tb.Toplevel):
    """
    Author: Narek Asaturyan
    Version: 1.3
    """
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.user = username
        
        self.title("")
        self.geometry('1400x844+200+100')
        self.minsize(1400, 844)
        self.iconbitmap("images/empty.ico")

        # Applying the custom window attribute for the border color
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = 0x201f1e
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

        # Widgets
        self.menu = Menu(self, self.parent, self.user)

        # Run program
        self.mainloop()
        
    def logOut(self):
        self.parent.run_login()
        self.destroy()
import tkinter as tk
import ttkbootstrap as tb
from account import *
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Icon
from user import *
import gspread
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass 


class login_window(tb.Toplevel):
    """
    A class representing the login interface for the game launcher. 
    Each user must enter their own exisiting account credentials, which are stored in the database. 
    New users can choose to register a new account by clicking a widget on the page.

    Attributes:
        parent (tkinter widget): Parent widget for this frame.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.warningLbl = ""

        self.geometry("500x400")
        #self.config(bg="#493d5e")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.iconbitmap("images/empty.ico")
        self.title("")


        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = 0x201f1e
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def verify(self, username, password, nameEn, passwordEn):
        """
            Params:
             input strings for username and password; entry objects for username and password.
             
            verifies if account information matches registered data in database
        """
        existing_acc = account(username, password, None)
        if (self.warningLbl != ""):
            self.warningLbl.destroy()

        wks = self.parent.accessAccountData()
        if (existing_acc.is_authentic(wks) == True):
            self.user = user(username)
            self.destroy()
            self.parent.run_launcher(self.user)

        else:
            #display error message for misinput
            self.warningLbl = self.parent.displayErrorMessage(self, self.warningLbl, "Incorrect username/password entered.\nPlease re-enter login credentials.")
            self.warningLbl.pack()

            #empties entries
            nameEn.delete(0, 'end')
            passwordEn.delete(0, 'end')
            

    def page(self):
        """
            loads up login gui
        """
        username=tb.StringVar()
        password=tb.StringVar()  

        loginTitle = tb.Label(self, text="Login")
        loginTitle.pack(pady=10)
        loginTitle.config(font=("Courier", 20))
         
        entryFrame = tb.Frame(self, borderwidth=10)
        entryFrame.pack()

        nameLbl = tb.Label(entryFrame, text="Username")
        nameLbl.grid(row=0,  column=0, pady=15)

        passwordLbl = tb.Label(entryFrame, text="Password")
        passwordLbl.grid(row=1,  column=0, pady=15)

        nameEn = tb.Entry(entryFrame, textvariable = username)
        nameEn.grid(row=0,  column=1)

        passwordEn = tb.Entry(entryFrame, show="*", textvariable = password)
        passwordEn.grid(row=1,  column=1)

        loginBtn = tb.Button(entryFrame, text="Log In", command = lambda: [self.verify(username, password, nameEn, passwordEn)])
        loginBtn.grid(row=2, column=1, pady=15)

        registerBtn = tb.Button(entryFrame, text="Register", command = lambda: [self.parent.run_register(), self.destroy()])
        registerBtn.grid(row=2, column=0)
        
        exitBtn = tb.Button(entryFrame, text="Exit app", command = lambda: self.parent.quitApp())
        exitBtn.grid(row=3, column=6)
import tkinter as tk
import ttkbootstrap as tb
from account import *
from ttkbootstrap.constants import *
import gspread
from ctypes import windll, byref, sizeof, c_int


class login_window(tb.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.geometry("500x400")
        #self.config(bg="#493d5e")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.iconbitmap("images/empty.ico")
        self.title("")


        HWND = windll.user32.GetParent(self.winfo_id())
        DWMWA_ATTRIBUTE = 35
        COLOR = 0x5e3d49
        windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

    def verify(self, username, password, nameEn, passwordEn, controller):
        # checks if login information is registered in database
        existing_acc = account(username, password, None)
        warninglbl = ""
        wks = controller.accessAccountData()
        if (existing_acc.is_authentic(wks) == True):
            self.destroy()
            self.parent.run_launcher()
            
        else:
            warninglbl = tk.Label(self, text="Incorrect username/password entered.\nPlease re-enter login credentials.")
            #displays warning
            warninglbl.pack()

            #empties entries
            nameEn.delete(0, 'end')
            passwordEn.delete(0, 'end')
            

    def page(self, controller):

        username=tb.StringVar()
        password=tb.StringVar()

        loginTitle = tb.Label(self, text="Login")
        loginTitle.pack(pady=10)
        loginTitle.config(font=("Courier", 20))

        entryFrame = tb.Frame(self, borderwidth=10)
        entryFrame.pack()

        warningFrame = tb.Frame(self)
        warningFrame.pack()

        nameLbl = tb.Label(entryFrame, text="Username")
        nameLbl.grid(row=0,  column=0, pady=15)

        passwordLbl = tb.Label(entryFrame, text="Password")
        passwordLbl.grid(row=1,  column=0, pady=15)

        warningLbl = tb.Label(warningFrame)
        warningLbl.pack_forget()

        nameEn = tb.Entry(entryFrame, textvariable = username)
        nameEn.grid(row=0,  column=1)

        passwordEn = tb.Entry(entryFrame, show="*", textvariable = password)
        passwordEn.grid(row=1,  column=1)

        loginBtn = tb.Button(entryFrame, text="Log In", command = lambda: [self.verify(username, password, nameEn, passwordEn, controller)])
        loginBtn.grid(row=2, column=1, pady=15)

        registerBtn = tb.Button(entryFrame, text="Register", command = lambda: [self.parent.run_register(), self.destroy()])
        registerBtn.grid(row=2, column=0)
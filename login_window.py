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

    def verify(self, username, password, nameEn, passwordEn, warningLbl):
        if(True):
            self.destroy()
            self.parent.run_launcher()
        else:
            #displays warning
            warningLbl.pack()

            #empties entries
            nameEn.delete(0, 'end')
            passwordEn.delete(0, 'end')

    def page(self):

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

        loginBtn = tb.Button(entryFrame, text="Log In", command = lambda: [self.verify(username, password, nameEn, passwordEn, warningLbl)])
        loginBtn.grid(row=2, column=1, pady=15)

        registerBtn = tb.Button(entryFrame, text="Register", command = lambda: [self.parent.run_register(), self.destroy()])
        registerBtn.grid(row=2, column=0)


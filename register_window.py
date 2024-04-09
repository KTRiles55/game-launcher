import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ctypes import windll, byref, sizeof, c_int
import gspread
import re
from account import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class register_window(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.account = account()

        # Window size and title
        self.geometry("500x600")
        self.minsize(500, 600)
        self.maxsize(500, 600)
        self.iconbitmap("images/empty.ico")
        self.title("")

        # Window title color
        HWND = windll.user32.GetParent(self.winfo_id())
        DWMWA_ATTRIBUTE = 35
        COLOR = 0x5e3d49
        windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

    def check(self):
        self.parent.run_login()

    def page(self):
        loginTitle = tb.Label(self, text="Register")
        loginTitle.pack(pady=10)
        loginTitle.config(font=("Courier", 20))

        entryFrame = tb.Frame(self, borderwidth=10, relief="groove")
        entryFrame.pack(pady=20)

        nameLbl = tb.Label(entryFrame, text="Username", font=("Courier", 12))
        nameLbl.grid(row=1, column=0, padx=5, pady=10)

        emailLbl = tb.Label(entryFrame, text="Email", font=("Courier", 12))
        emailLbl.grid(row=2, column=0, padx=5, pady=10)

        passwordLbl = tb.Label(entryFrame, text="Password", font=("Courier", 12))
        passwordLbl.grid(row=3, column=0, padx=5, pady=10)

        nameEn = tb.Entry(entryFrame)
        nameEn.grid(row=1, column=1)

        self.email_entry = tb.Entry(entryFrame)  # Define email_entry
        self.email_entry.grid(row=2, column=1)

        passwordEn = tb.Entry(entryFrame, show="*")
        passwordEn.grid(row=3, column=1)

        backBtn = tb.Button(entryFrame, text="Back", command = lambda: [self.parent.run_login(), self.withdraw()])
        backBtn.grid(row=4, column=0, pady=10)

        submitBtn = tb.Button(entryFrame, text="Create an Account", command = lambda: [self.check(), self.withdraw()])
        submitBtn.grid(row=4, column=1, padx=5, pady=10)



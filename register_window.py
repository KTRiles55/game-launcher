import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import gspread
import re
from account import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


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
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = 0x201f1e
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def check(self, name, password, email, controller):
        #Logic for checking if info exist
        new_acc = account(name, password, email)
        warningLbl = ""
        wks = controller.accessAccountData()         

        # Create new account if it does not exist
        if ((new_acc.findUsername(wks) == None) and (new_acc.findPassword(wks) == None) and (new_acc.findEmail(wks) == None)):
            new_acc.create_newuser(wks)
            confirmLbl = tk.Label(self, text="You have successfully created a new account!\nPlease immediately check your email inbox to verify this account.")
            confirmLbl.place(anchor='center', relx=1, rely=0)
            returntoLogBtn = tk.Button(self, text="Return to Login", bg="#888a86", activebackground="#a8aba6", command = lambda: [controller.run_login(), self.destroy()])
            returntoLogBtn.place(anchor='center', relx=1, rely=1)
    
        elif (new_acc.findUsername(wks) != None):
            warningLbl = tk.Label(self, text="This account name is already used!")
    
        elif (new_acc.findPassword(wks) != None):
            warningLbl = tk.Label(self, text="This password is already used!")
    
        elif (new_acc.findEmail(wks) != None):
            warningLbl = tk.Label(self, text="This email is already used!")
            
        #self.send_confirmation_email(email.get())  # Send confirmation email
        controller.run_login()

    def page(self, controller):
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

        email_entry = tb.Entry(entryFrame)  # Define email_entry
        email_entry.grid(row=2, column=1)

        passwordEn = tb.Entry(entryFrame, show="*")
        passwordEn.grid(row=3, column=1)

        backBtn = tb.Button(entryFrame, text="Back", command = lambda: [self.parent.run_login(), self.withdraw()])
        backBtn.grid(row=4, column=0, pady=10)

        submitBtn = tb.Button(entryFrame, text="Create an Account", command = lambda: [self.check(nameEn, passwordEn, email_entry, controller), self.withdraw()])
        submitBtn.grid(row=4, column=1, padx=5, pady=10)
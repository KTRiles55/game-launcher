import tkinter as tk
import ttkbootstrap as tb
from email_sender import send_confirmation_email
from ttkbootstrap.constants import *
import openpyxl
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
    """
    A class representing the registration interface for creating a new account, which is accessible via the login interface.
    New users can enter new account credentials, while following a specific set of rules listed for each entry.
    This class will alert the user if account information already exists in the database or is invalid.

    Attributes:
        parent (tkinter widget): Parent widget for this frame.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.warningLbl = ""

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

    def check(self, name, password, email, nameEn, passEn, emailEn, frame): 
        """
            Params:
             input strings for name, password and email address
            
            verifies existing account info 
        """
        new_acc = account(name.get(), password.get(), email.get())
        wks = self.parent.accessAccountData()

        if (self.warningLbl != ""):
            self.warningLbl.destroy()

        # Determines valid account information
        if (new_acc.is_valid(name.get(), email.get(), password.get()) == False):

            self.warningLbl = self.parent.displayErrorMessage(self, self.warningLbl, "* New account credentials are invalid. *\n* Please re-enter user information/fill in empty fields. *")
            self.warningLbl.pack()

        elif (new_acc.is_valid(name.get(), email.get(), password.get()) == True):
            # Create new account if it does not exist
            if ((new_acc.findUsername(wks) == None) and (new_acc.findPassword(wks) == None) and (new_acc.findEmail(wks) == None)):
                new_acc.create_newuser()  
                frame.destroy()
                
                confirmLbl = tk.Label(self, text="You have successfully created a new account!\nPlease immediately check your email inbox to verify this account.")
                confirmLbl.pack()
                returntoLogBtn = tk.Button(self, text="Return to Login", bg="#888a86", activebackground="#a8aba6", command = lambda: [self.parent.run_login(), self.destroy()])
                returntoLogBtn.pack()
                send_confirmation_email(email.get())  # Send confirmation email
  
            elif (new_acc.findUsername(wks) != None):
                self.warningLbl = self.parent.displayErrorMessage(self, self.warningLbl, "* This username is already used! *")
                self.warningLbl.pack()

            elif (new_acc.findPassword(wks) != None):
                self.warningLbl = self.parent.displayErrorMessage(self, self.warningLbl, "* This password is already used! *")
                self.warningLbl.pack()

            elif (new_acc.findEmail(wks) != None):
                self.warningLbl = self.parent.displayErrorMessage(self, self.warningLbl, "* This email is already used! *")
                self.warningLbl.pack()
                
        #empties entries
        nameEn.delete(0, 'end')
        passEn.delete(0, 'end')
        emailEn.delete(0, 'end')

    def page(self):
        """
            loads up register gui
        """
        loginTitle = tb.Label(self, text="Register")
        loginTitle.pack(pady=10)
        loginTitle.config(font=("Courier", 20))


        entryFrame = tb.Frame(self, borderwidth=10, relief="groove")
        entryFrame.pack(pady=20)

        username=tb.StringVar()
        password=tb.StringVar()
        email=tb.StringVar()  
        
        nameLbl = tb.Label(entryFrame, text="Username", font=("Courier", 12)) 
        nameLbl.grid(row=1, column=0, padx=5, pady=10)

        emailLbl = tb.Label(entryFrame, text="Email", font=("Courier", 12)) 
        emailLbl.grid(row=2, column=0, padx=5, pady=10)
        
        passwordLbl = tb.Label(entryFrame, text="Password", font=("Courier", 12))
        passwordLbl.grid(row=3, column=0, padx=5, pady=10)

        nameEn = tb.Entry(entryFrame, textvariable=username)
        nameEn.grid(row=1, column=1, ipadx=20)

        email_entry = tb.Entry(entryFrame, textvariable=email)  # Define email_entry
        email_entry.grid(row=2, column=1, ipadx=20)

        passwordEn = tb.Entry(entryFrame, textvariable=password)
        passwordEn.grid(row=3, column=1, ipadx=20)

        userNameReqLbl = tb.Label(entryFrame, text="-Username requires 5-20 characters, starting\n with ONLY alphabetical characters, including\nunderscores, but can also be followed by numerical\ncharacters.\n")
        passWordReqLbl = tb.Label(entryFrame, text="-Password requires 10-25 characters, containing\n at least one special character(#, $, %, &, @,...etc..),\nat least one capital alphabetical character, and at\nleast 1 numerical character.")
        userNameReqLbl.grid(row=6, column=1)
        passWordReqLbl.grid(row=7, column=1)

        backBtn = tb.Button(entryFrame, text="Back", command = lambda: [self.parent.run_login(), self.withdraw()])
        backBtn.grid(row=10, column=0, pady=10)

        submitBtn = tb.Button(entryFrame, text="Create an Account", command = lambda: self.check(username, password, email, nameEn, passwordEn, email_entry, entryFrame))
        submitBtn.grid(row=4, column=1, padx=5, pady=10)

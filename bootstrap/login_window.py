import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.style import *
import gspread 


class login_window(tk.Tk):
    def verify(self):
        self.quit()

    def page(self, style):
        self.geometry("500x400")
        self.minsize(500, 400)
        self.maxsize(500, 400)
    


        
        
        loginTitle = tb.Label(self, text="Login", )
        loginTitle.pack(pady=10)
        loginTitle.config(font=("Courier", 16))

        entryFrame = tb.Frame(self, bootstyle= "default", relief="groove", )
        entryFrame.pack(pady=20,padx=40)

        nameLbl = tb.Label(entryFrame, text="Username")
        nameLbl.grid(row=0,  column=0, pady=15)

        passwordLbl = tb.Label(entryFrame, text="Password")
        passwordLbl.grid(row=1,  column=0, pady=15)

        nameEn = tb.Entry(entryFrame)
        nameEn.grid(row=0,  column=1)

        passwordEn = tb.Entry(entryFrame,show="*")
        passwordEn.grid(row=1,  column=1)

        loginBtn = tb.Button(entryFrame, text="Log In",bootstyle= "primary",  command = lambda: self.verify())
        loginBtn.grid(row=2, column=1, pady=15)

        registerBtn = tb.Button(entryFrame, text="Register",)
        registerBtn.grid(row=2, column=0)


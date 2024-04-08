import tkinter as tk
import ttkbootstrap as tb
from account import *
from ttkbootstrap.constants import *
import gspread
from ctypes import windll, byref, sizeof, c_int


class login_window(tb.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def verify(self,controller, account_wks):
        self.destroy()
        controller.login_pressed(account_wks)

    def page(self, controller, account_wks):
        self.geometry("500x400")
        self.config(bg="#493d5e")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.iconbitmap("empty.ico")
        self.title("")

        HWND = windll.user32.GetParent(self.winfo_id())
        DWMWA_ATTRIBUTE = 35
        COLOR = 0x5e3d49
        windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

        loginTitle = tb.Label(self, text="Login")
        loginTitle.pack(pady=10)
        loginTitle.config(font=("Courier", 20), background="#493d5e", foreground="white")

        entryFrame = tb.Frame(self, borderwidth=10, relief="groove")
        entryFrame.pack()

        nameLbl = tb.Label(entryFrame, text="Username", font=("Courier", 12))
        nameLbl.grid(row=0,  column=0, pady=15)

        passwordLbl = tb.Label(entryFrame, text="Password", font=("Courier", 12))
        passwordLbl.grid(row=1,  column=0, pady=15)

        nameEn = tb.Entry(entryFrame)
        nameEn.grid(row=0,  column=1)

        passwordEn = tb.Entry(entryFrame, show="*")
        passwordEn.grid(row=1,  column=1)

        loginBtn = tb.Button(entryFrame, text="Log In", command = lambda: [self.verify(controller, account_wks)])
        loginBtn.grid(row=2, column=1, pady=15)

        registerBtn = tb.Button(entryFrame, text="Register", command = lambda: [controller.register_pressed(account_wks), self.destroy()])
        registerBtn.grid(row=2, column=0)



if __name__ == "__main__":
    app = login_window()
    app.mainloop()

        



import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ctypes import windll, byref, sizeof, c_int
import gspread
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class register_window(tb.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check(self, controller, account_wks, email_entry):
        # Logic for checking if info exists
        # Send confirmation email
        self.send_confirmation_email(email_entry.get())
        controller.return_to_login(account_wks)

    def send_confirmation_email(self, email):
        # Email configuration
        sender_email = "TechWizardsCSUN@outlook.com"
        sender_password = "Comp380CSUN"
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587

        # Message configuration
        subject = "Account Creation Confirmation"
        message = "Hello User, \n\nYour account has been successfully created! \n\nThank you for choosing TechWizards! "

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject

        # Attach message to container
        msg.attach(MIMEText(message, 'plain'))

        # Start SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())

        print("Confirmation email sent to", email)

    def page(self, controller, account_wks):
        self.geometry("500x600")
        self.config(bg="#4a464d")
        self.minsize(500, 600)
        self.maxsize(500, 600)
        self.iconbitmap("empty.ico")
        self.title("")

        # Title Bar Color
        HWND = windll.user32.GetParent(self.winfo_id())
        DWMWA_ATTRIBUTE = 35
        COLOR = 0x4d464a
        windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

        loginTitle = tb.Label(self, text="Register", background="#4a464d", foreground="white")
        loginTitle.pack(pady=10)
        loginTitle.config(font=("Courier", 14))

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

        backBtn = tb.Button(entryFrame, text="Back", command=lambda: [controller.return_to_login(account_wks), self.withdraw()])
        backBtn.grid(row=4, column=0, pady=10)

        submitBtn = tb.Button(entryFrame, text="Create an Account", command = lambda: [self.check(controller, account_wks, self.email_entry), self.withdraw(),])
        submitBtn.grid(row=4, column=1, padx=5, pady=10)



import ttkbootstrap as tb
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import gspread
# Assuming login_window, register_window, and launcher have been similarly updated to use ttkbootstrap
from login_window import login_window
from register_window import register_window
from launcher import Launcher


class Main(tb.Window):

    def register_pressed(self, account_wks):
        register = register_window()
        register.page(self, account_wks)

    def return_to_login(self, account_wks):
        login = login_window()
        login.page(self, account_wks)

    def login_pressed(self, account_wks):
        Launcher((1400, 900))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = Style(theme="techwiz")
        Style.load_user_themes(style, "themes.json")

        sa = gspread.service_account(filename="database_key.json")
        account_sheet = sa.open("accountTest")

        account_wks = account_sheet.worksheet("accountInfo")
        login = login_window()

        login.page(self, account_wks)
        self.withdraw()

if __name__ == "__main__":
    app = Main()
    app.mainloop()



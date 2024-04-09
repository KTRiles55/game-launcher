import ttkbootstrap as tb
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import gspread
from login_window import login_window
from register_window import register_window
from launcher import Launcher


class Main(tb.Window):

    def set_theme(self):
        Style.load_user_themes(Style(), "themes.json")

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

        Style.load_user_themes(Style(), "themes.json")
        Style().theme_use("techwiz_theme")

        sa = gspread.service_account(filename="database_key.json")
        account_sheet = sa.open("accountTest")

        account_wks = account_sheet.worksheet("accountInfo")
        login = login_window()

        login.page(self, account_wks)
        self.withdraw()


main = Main()
main.mainloop()



import ttkbootstrap as tb
import gspread
from login_window import *
from register_window import *
from launcher import *

class Main(tb.Window):

    def set_theme(self):
        Style.load_user_themes(Style(), "themes.json")

    def run_register(self):
        register = register_window(self)
        register.page(self)

    def run_login(self):
        login = login_window(self)
        login.page(self)

    def run_launcher(self):
        self.launcher = Launcher(self)
        
     # opens google sheets database
    def accessAccountData(self):
        sa = gspread.service_account(filename="database_key.json")
        account_sheet = sa.open("accountTest")
        account_wks = account_sheet.worksheet("accountInfo")
        return account_wks


    def __init__(self):
        super().__init__()

        Style.load_user_themes(Style(), "themes.json")
        Style().theme_use("techwiz_theme")

        login = login_window(self)
        login.page(self)
        self.withdraw()


main = Main()
main.mainloop()
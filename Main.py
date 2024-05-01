import ttkbootstrap as tb
from ttkbootstrap.icons import Icon
import openpyxl
from login_window import *
from register_window import *
from launcher import *
import pydoc


class Main(tb.Window):

    def set_theme(self):
        Style.load_user_themes(Style(), "themes.json")

    def run_register(self):
        register = register_window(self)
        register.page()

    def run_login(self):
        login = login_window(self)
        login.page()

    def run_launcher(self, username):
        self.username = username
        self.launcher = Launcher(self, self.username)  
        
     # opens google sheets database
    def accessAccountData(self): 
        
        path = "database_offline.xlsx"
        wb_obj = openpyxl.load_workbook(path) 
        wks = wb_obj["accountInfo"] 
        
        return wks 

     # shows error symbol for every misinput entry
    def displayErrorMessage(self, page, warningMessage, statement):
        errorIcon = tk.PhotoImage(data=Icon.error)
        warningMessage = tk.Label(page, text=statement, image=errorIcon, compound='left')
        warningMessage.image = errorIcon       
        return warningMessage
    
    # closes app
    def quitApp(self):
        self.quit()    

    def __init__(self):
        super().__init__()

        Style.load_user_themes(Style(), "themes.json")
        Style().theme_use("techwiz_theme")

        login = login_window(self)
        login.page()
        self.withdraw()


main = Main()
main.mainloop()
pydoc.writedoc('tech_wiz_launcher')
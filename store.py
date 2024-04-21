import gspread
import re


# ID	Title	Developer	Price	Tags	Image
class store():

    def __init__(self):
        sa = gspread.service_account(filename="database_key.json")
        sh = sa.open("accountTest")

        self.wks = sh.worksheet("store")


    def sort_prices():
        pass
    
    def get_all_games(self):
        all_games = self.wks.get_all_records()
        return all_games

    def get_games_sharing_tag(self, selected):
        #return list of games with the same category 
        games = []
        count = 0 
        col_count = 31
        for i in range(1, col_count):
            tags = self.get_tags(i)
            if(selected in tags):
                games.append({})
                games[count]["Title"] =  self.get_title(i)
                games[count]["Developer"] =  self.get_dev(i)
                games[count]["Price"] =  self.get_price(i)
                count += 1


        return games

    

    def get_game(self,input):
        #gets specific game based on searchbar
        pass

    def get_ID():
        pass 

    def get_title(self,row):
        column = 2
        title = self.wks.cell(row, column).value
        return title
        

    def get_dev(self,row):
        column = 3
        dev = self.wks.cell(row, column).value
        return dev

    def get_price(self,row):
        column = 4
        price = self.wks.cell(row, column).value
        return price

    def get_tags(self,row):
        column = 5
        tag = self.wks.cell(row, column).value
        return tag

    def generate_ID(self,row):
        pass
    


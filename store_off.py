import openpyxl 

class store_off():
    def __init__(self):
        path = "database_offline.xlsx"
        wb_obj = openpyxl.load_workbook(path)
        self.wks = wb_obj["store"]



    def get_all_games(self):
        #return list of games with the same category 
        games = []
        count = 0 
        col_count = 31
        for i in range(1, col_count-1):
            games.append({})
            games[i-1]["Title"] =  self.get_title(i+1)
            games[i-1]["Developer"] =  self.get_dev(i+1)
            games[i-1]["Price"] =  self.get_price(i+1)
            games[i-1]["Tags"] =  self.get_parsed_tags(i+1)

        return games

    def get_games_sharing_tag(self, selected):
        #return list of games with the same category 
        games = []
        count = 0 
        col_count = 31
        for i in range(1, col_count-1):
            tags = self.get_tags(i+1)
            if(selected in tags):
                games.append({})
                games[count]["Title"] =  self.get_title(i+1)
                games[count]["Developer"] =  self.get_dev(i+1)
                games[count]["Price"] =  self.get_price(i+1)
                games[count]["Tags"] =  self.get_parsed_tags(i+1)
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

    
    def get_parsed_tags(self,row):
        column = 5
        tag = self.wks.cell(row, column).value
        parsed_tags = tag.split(",")
        return parsed_tags




import openpyxl 


class user():
    def __init__(self, username):
        path = "database_offline.xlsx"
        self.wb_obj = openpyxl.load_workbook(path)
        self.wks_account = self.wb_obj["accountInfo"]
        self.wks_store = self.wb_obj["store"]

        self.username = username
 
    def find_row(self):
        """
            returns:
            the row the username belongs to (int)
        """
        name = ""
        row = 0
        row_count = 14
        for i in range(1, row_count-1):
            name = self.wks_account.cell(i, 1).value
            if(name == self.username.get()):
                return i
        return 1

    def get_username(self):
        """
            returns:
            username (string)
        """
        return self.username.get()

    def get_password(self):
        """
            returns:
            user's password (string)
        """
        password = self.wks_account.cell(self.find_row(), 2).value
        return password

    def get_email(self):
         """
            returns:
            user's email (string)
        """
        email = self.wks_account.cell(self.find_row(), 3).value
        return get_email

    def get_parsed_library(self):
        #Library section of database format ex: The Witcher 3: Wild Hunt/Civilization VI/Half-Life: Alyx/Command & Conquer/Doom
        #Gets library only as titles
        """
            returns:
            titles of games belonging to the user
        """
        library = self.wks_account.cell(self.find_row(),4).value
        if(library != None):
            parsed_library = library.split("/")
            return parsed_library
        return []

    def update_library(self, new):
        """
            args:
            title of a game (string)
            updates the users library by appending the string in the cell with the title a purchase
        
        """
        library = self.wks_account.cell(self.find_row(),4).value
        if(library != None):
            self.wks_account.cell(self.find_row(),4).value +=  "/" + new 
        else:
            self.wks_account.cell(self.find_row(),4).value = new
        self.wb_obj.save("database_offline.xlsx")
 
    
    def get_game_details(self):
        #Get games in library in dictionary format
        """
            returns:
            user's library in a list with each game as a dictionary
        """

        titles = self.get_parsed_library()
        library = []
        count = 0 
        row_count = 31
        for title in titles:
            for i in range(1, row_count-1):
                cell_title = self.wks_store.cell(i+1, 2).value 
                if (title == cell_title):
                    library.append({})
                    library[count]["Title"] =  self.wks_store.cell(i+1, 2).value
                    library[count]["Developer"] =  self.wks_store.cell(i+1, 3).value
                    library[count]["Price"] =  self.wks_store.cell(i+1, 4).value
                    tags = self.wks_store.cell(i+1, 5).value
                    parsed_tags = tags.split(",")
                    library[count]["Tags"] =  parsed_tags
                    library[count]["Release_Date"] = self.wks_store.cell(i+1, 6).value
                    count += 1
        return library
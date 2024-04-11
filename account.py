# class for user account
import gspread 


class account():

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def is_valid_username(username):
        pass

    def is_valid_email(email):
        pass

    def is_valid_password(password):
        pass

    def is_valid(username, email, password):
        #verifies if registration format
        if(is_valid_username(username) and is_valid_email(email) and is_valid_password(password)):
            return True
        else:
            return False

    def is_authentic(self, wks):
        #verifies if login info is in database
        userCell = self.findUsername(wks)
        passwCell = self.findPassword(wks)
        
        #if user information is unidentified
        if ((userCell == None) or (passwCell == None)):
            return False
        
        return True
               

    def find_sheet(self, wks):
        #finds the accounts associated spreadsheet 
        user = user.findUsername(self.username, wks)
        acc_sheet = wks.row_values(user)
        return acc_sheet
    

    def findUsername(self, wks):
        return wks.find(self.username.get())
    

    def findPassword(self, wks):
        return wks.find(self.password.get())


    def findEmail(self, wks):
        return wks.find(self.email.get())
            

    def create_newuser(self, wks):
        #creates instance of user 
        wks.append_row([self.username.get(), self.password.get(), self.email.get()])

    
    def update_user(new_username, new_password, new_email, username, password, email, wks):
        # updates account info
        row_entries = wks.get_all_values()
        for row in row_entries:
            for key, value in enumerate(row):
                if (value == username):
                   row[key] = new_username
                   row[key+1] = new_password
                   row[key+2] = new_email 
                   wks.update(row_entries)
                   
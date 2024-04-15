# class for user account
import gspread 
import re


class account():

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def is_valid_username(self, username):
        #checks if username is valid
        name_pattern = re.compile(r'^([a-zA-Z_]+[0-9]*){5,20}$')
        if (name_pattern.search(username.get()) == None):
            return False 
        return True

    def is_valid_email(self, email):
        #checks if email is valid
        email_pattern = re.compile(r'[a-zA-Z\.-_\+]+@[a-zA-z-]+\.(com|org|net|gov)')
        if (email_pattern.search(email.get()) == None):
            return False
        return True

    def is_valid_password(self, password): 
        #checks if password is valid
        passw_pattern1 = re.compile(r'^(\S){10,25}$')
        passw_pattern2 = re.compile(r'\w*\W+\w*[A-Z]+\w*[0-9]+\w*')
        if ((passw_pattern1.search(password.get()) == None) or (passw_pattern2.search(password.get()) == None)):
            return False 
        return True

    def is_valid(self, username, email, password):
        #verifies if registration format
        if(self.is_valid_username(username) and self.is_valid_email(email) and self.is_valid_password(password)):
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
                   
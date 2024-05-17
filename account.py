# class for user account
import openpyxl
import pandas as pd
import re


# class for user account
class account():
    """
    A class representing the user's account. This class directly interacts with the spreadsheets database to fetch
    account information from a single row on the spreadsheet when given either username, password or email input. 
    It also returns results based on whether the given input is valid or not.

    Author: Kenneth Riles

    Attributes:
        parent (tkinter widget): Parent widget for this frame.
    """
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def is_valid_username(self, username):
        """
            Params:
             username as string
            Returns:
             boolean
             
            checks if username is valid
        """
        name_pattern = re.compile(r'_*[a-zA-Z]+_*[0-9]*') 
        if (name_pattern.search(username) == None) or (re.search(r'\w{5,20}', username) == None):
            return False 
        return True

    def is_valid_email(self, email):  
        """
            Params:
             email as string
            Returns:
             boolean
             
            checks if email is valid
        """
        
        email_pattern = re.compile(r'[a-zA-Z]+[\.-_\+]*@[a-zA-z-]+\.(com|org|net|gov|edu)')
        if (email_pattern.search(email) == None):
            return False
        return True

    def is_valid_password(self, password): 
        """
            Params:
             password as string
            Returns:
             boolean
             
            checks if password is valid
        """        

        passw_pattern1 = re.compile(r'^(\S){10,25}$')
        if ((passw_pattern1.search(password) == None) or ((re.search(r'\W+',password) == None) or (re.search(r'[A-Z]+',password) == None) or (re.search(r'\d+',password) == None))):
            return False 
        return True

    def is_valid(self, username, email, password):
        """
            Params:
             input strings for username, email and password
            Returns:
             boolean
             
            checks if account info is valid
        """
        
        if(self.is_valid_username(username) and self.is_valid_email(email) and self.is_valid_password(password)):
            return True
        else:
            return False

    def is_authentic(self, wks):
        """
            Params:
             pointer to Google worksheet database
            Returns:
             boolean
             
            verifies if account info is already stored in database
        """
        
        if ((self.username != "") and (self.password != "")):
            userCell = self.findUsername(wks)
            passwCell = self.findPassword(wks)
        
            #if user information is unidentified
            if ((userCell != None) and (passwCell != None) and (userCell == passwCell)):
                return True
        
        return False
               


    def searchRows(self, wks, column, data):
        for cell in wks[column]:
            if (cell.value == data):
                return cell.row 
            
        return None
    
        
    def findUsername(self, wks):
        """
            Params:
             pointer to Google worksheet database
            Returns:
             username cell number (int)
        """
       
        return self.searchRows(wks, 'A', self.username)
    

    def findPassword(self, wks):
        """
            Params:
             pointer to Google worksheet database
            Returns:
             password cell number (int)
        """
     
        return self.searchRows(wks, 'B', self.password)


    def findEmail(self, wks):
        """
            Params:
             pointer to Google worksheet database
            Returns:
             email cell number (int)
        """
        return self.searchRows(wks, 'C', self.email)
            

    def create_newuser(self): 
        """
            Params:
             pointer to Google worksheet database
            
            adds new instance of user onto next empty row in database
        """
        path="database_offline.xlsx"
        new_account = pd.DataFrame({'Username': [self.username], 'Password': [self.password], 'Email': [self.email]})
        excelWrite = pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='overlay')
        excelRead = pd.read_excel(path)
        new_account.to_excel(excelWrite, sheet_name='accountInfo', header=False, startrow=len(excelRead)+1, index=False)
        excelWrite._save()

    
    def update_user(self, new_username, new_password, new_email, wks):
        """
            Params:
             input strings for new_username, new_password and new_email; pointer to Google worksheet database
            
            searches for existing user cell and updates its contents 
        """
        row_entries = wks.get_all_values()
        for row in row_entries:
            for key, value in enumerate(row):
                if (value == self.username):
                   row[key] = new_username
                   row[key+1] = new_password
                   row[key+2] = new_email 
                   wks.update(row_entries)
                   
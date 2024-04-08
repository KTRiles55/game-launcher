import gspread




class account():

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

    def is_authentic(username, password):
        #verifies if login info is in database
        pass



    def find_sheet(username):
        #finds the accounts associated spreadsheet
        pass

    def create_newuser(username, library=[]):
        #creates instance of user 
        #either pass the wks or all the account info
        pass



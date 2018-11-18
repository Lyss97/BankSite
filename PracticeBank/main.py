import webapp2
import os
import jinja2
import logging
from models import *
import base64
#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

gUsername = ''

class LoginPage(webapp2.RequestHandler):
    def get(self):

        start_template = jinja_current_dir.get_template("templates/login.html")
        encrypt()
        self.response.write(start_template.render())

    def post(self):
        end_template = jinja_current_dir.get_template("templates/mainmenu.html")
        self.response.write(end_template.render())
class RegPage(webapp2.RequestHandler):
    def get(self):
        end_template = jinja_current_dir.get_template("templates/register.html")
        self.response.write(end_template.render())
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")


        bool = UniqueUser(username)
        bool2 = newUser(username, password)
        if bool == True and bool2 == True:
            fname = self.request.get("first_name")
            password =  base64.b64encode(password)
            acc = BankAcc(user_name = username, pass_word = password, savings = 0, checking = 0)
            acc.put()
            msg1 = "Thanks for registering " + fname + ", please sign in."
            dict = {"msg1": msg1}

            end_template = jinja_current_dir.get_template("templates/login.html")
            self.response.write(end_template.render(dict))
        elif bool == False:
            msg1 = "Username is already taken, please choose another."
            dict = {"msg1": msg1}
            end_template = jinja_current_dir.get_template("templates/register.html")
            self.response.write(end_template.render(dict))
        elif bool2 == False:
            msg1 = "New user info does not meet requirements"
            dict = {"msg1": msg1}
            end_template = jinja_current_dir.get_template("templates/register.html")
            self.response.write(end_template.render(dict))

class MainMenu(webapp2.RequestHandler):

    def post(self):
        username = self.request.get('user_name')
        password = self.request.get('pass_word')
        global gUsername
        gUsername = username

        bool = ValidLogin(username,password)
        if bool == True:
            end_template = jinja_current_dir.get_template("templates/mainmenu.html")
            dict = {"name": gUsername}
            self.response.write(end_template.render(dict))
        else:
            msg1 = "Username or Password is incorrect, please try again."
            dict = {"msg1": msg1}
            end_template = jinja_current_dir.get_template("templates/login.html")
            self.response.write(end_template.render(dict))
class MainMenu2(webapp2.RequestHandler):

    def post(self):
            end_template = jinja_current_dir.get_template("templates/mainmenu.html")
            self.response.write(end_template.render())

class Deposit(webapp2.RequestHandler):
    def post(self):
            Amt = self.request.get("dep_amt")
            type = "checking"
            balance = CheckBalance(gUsername, type)
            bool = depToAcc(gUsername, Amt, type)
            if bool == False:
                msg1 = "Enter an amount that is greater than zero "
                dict = {"msg1" : msg1}
                end_template = jinja_current_dir.get_template("templates/mainmenu.html")
                self.response.write(end_template.render(dict))
            else:
                transaction = " ADDED to "
                dict = {"amount": Amt, "transaction": transaction}
                end_template = jinja_current_dir.get_template("templates/transaction.html")
                self.response.write(end_template.render(dict))


class depositAmt(webapp2.RequestHandler):
    def post(self):
            Amt = self.request.get("dep_amt")
            type = "saving"
            balance = CheckBalance(gUsername, type)
            bool = depToAcc(gUsername, Amt, type)
            if bool == False:
                msg1 = "Enter an amount that is greater than zero "
                dict = {"msg1" : msg1}
                end_template = jinja_current_dir.get_template("templates/mainmenu.html")
                self.response.write(end_template.render(dict))
            else:
                transaction = " ADDED to "
                dict = {"amount": Amt, "transaction": transaction}
                end_template = jinja_current_dir.get_template("templates/transaction.html")
                self.response.write(end_template.render(dict))



class Withdraw(webapp2.RequestHandler):
    def post(self):
        Amt = self.request.get("with_amt")
        type = "checking"
        balance = CheckBalance(gUsername, type)

        bool = withdFromAcc(gUsername, Amt, balance, type)
        if bool == False:
            msg1 = "Amount is not valid. "
            dict = {"msg1" : msg1}
            end_template = jinja_current_dir.get_template("templates/mainmenu.html")
            self.response.write(end_template.render(dict))
        else:
            transaction = " SUBTRACTED from "
            dict = {"amount": Amt, "transaction": transaction}
            end_template = jinja_current_dir.get_template("templates/transaction.html")
            self.response.write(end_template.render(dict))

class withdrawAmt(webapp2.RequestHandler):
    def post(self):
        Amt = self.request.get("with_amt")
        type = "saving"
        balance = CheckBalance(gUsername, type)

        bool = withdFromAcc(gUsername, Amt, balance, type)
        if bool == False:
            msg1 = "Amount is not valid. "
            dict = {"msg1" : msg1}
            end_template = jinja_current_dir.get_template("templates/mainmenu.html")
            self.response.write(end_template.render(dict))
        else:
            transaction = " SUBTRACTED from "
            dict = {"amount": Amt, "transaction": transaction}
            end_template = jinja_current_dir.get_template("templates/transaction.html")
            self.response.write(end_template.render(dict))
class Balance(webapp2.RequestHandler):
    def post(self):
        savings = getSavings(gUsername)
        checking = getChecking(gUsername)
        dict = {"savings" : savings, "checking"  : checking}
        end_template = jinja_current_dir.get_template("templates/balance.html")
        self.response.write(end_template.render(dict))
class TransferBal(webapp2.RequestHandler):
    def post(self):

        from_acc = self.request.get('type')
        to_acc = self.request.get('type2')
        amt = self.request.get('amt')
        balance = CheckBalance(gUsername, from_acc)
        bool = withdFromAcc(gUsername, amt, balance, from_acc)
        success = ""
        error = ""
        if bool != False:
            bool2 = depToAcc(gUsername, amt, to_acc)
            logging.info("this is bool2")
            logging.info(bool2)
            if bool2 == True:
                success = "Transaction was successful"
            else:
                error = "Can not transfer this amount"
        else:
            error = "Can not transfer this amount"
        savings = getSavings(gUsername)
        checking = getChecking(gUsername)
        dict = {"savings" : savings, "checking"  : checking, "success" : success, "error": error}
        end_template = jinja_current_dir.get_template("templates/balance.html")
        self.response.write(end_template.render(dict))

class Transfer(webapp2.RequestHandler):
    def post(self):

        end_template = jinja_current_dir.get_template("templates/transfer.html")
        self.response.write(end_template.render())

'''
class Trans(webapp2.RequestHandler):
    def post(self):
        deposit = self.request.get("dep_amnt")

        withdraw = self.request.get("with_amnt")
        balance = CheckBalance(gUsername)
'''

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/register', RegPage),
    ('/mainmenu',MainMenu),
    ('/depPage', Deposit),
    ('/withPage', Withdraw),
    #('/trans', Trans),
    ('/mm2', MainMenu2),
    ('/withdraw', withdrawAmt),
    ('/deposit', depositAmt),
    ('/balance', Balance),
    ('/transfer', Transfer),
    ('/transbal', TransferBal),


], debug=True)

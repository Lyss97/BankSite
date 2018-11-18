import base64
from google.appengine.ext import ndb

import logging

class BankAcc(ndb.Model):
    user_name = ndb.StringProperty(required = True)
    pass_word = ndb.StringProperty(required = True)
    savings = ndb.IntegerProperty(required = False)
    checking = ndb.IntegerProperty(required = False)

def ValidLogin(userr, pw):
    bool = False
    sup = BankAcc.query().fetch()
    for item in sup:
        password = base64.b64decode(item.pass_word)
        if password == pw and item.user_name == userr:
            return True
    return bool

def CheckBalance(userr, type):
    sup = BankAcc.query().fetch()
    if type == 'checking':
        for item in sup:
            if item.user_name == userr:
                balance = item.checking
                return balance
    else:
        for item in sup:
            if item.user_name == userr:
                balance = item.savings
                return balance

def UniqueUser(userr):
    bool = True
    sup = BankAcc.query().fetch()
    for item in sup:
        if item.user_name == userr:
            return False
    return bool

def newUser(user, password):
    sup = BankAcc.query().fetch()
    if len(password) > 4 and len(password) <= 8 and len(user) > 4 and len(user) <= 8 :
        specialed = ['!', '@', '#', '$', '%', '^', '&', '*', '?']
        result = any(item in specialed for item in password)
        if result:
            return True
        else:
            return False
    else:
        return False
def depToAcc(user, amnt, type):
    sup = BankAcc.query().fetch()
    if int(amnt) < 0:
        return False
    elif type == 'checking':
        for item in sup:
            if item.user_name == user:
                item.checking = item.checking  + int(amnt)
                item.put()
    else:
        for item in sup:
            if item.user_name == user:
                item.savings = item.savings  + int(amnt)
                item.put()

def withdFromAcc(user, amnt, balance, type):
    sup = BankAcc.query().fetch()
    if int(amnt) > balance or int(amnt) < 0:
        return False
    elif type == 'checking':
        for item in sup:
            if item.user_name == user:
                item.checking = item.checking  - int(amnt)
                item.put()
    else:
        for item in sup:
            if item.user_name == user:
                item.savings = item.savings  - int(amnt)
                item.put()

def encrypt():
    #A Reverse Cipher progra

    logging.info(base64.b64encode("password"))
    logging.info(base64.b64decode("cGFzc3dvcmQ="))



def somethingElse():
    message =  'Hello'
    translated = ''
    i = len(message)  -  1
    while  i >=  0 :
             translated = translated + message[i]
             i  =  i  - 1
    logging.info(translated)

def getSavings(user):
    sup = BankAcc.query().fetch()
    for item in sup:
        if item.user_name == user:
            savings = item.savings
            return savings
def getChecking(user):
    sup = BankAcc.query().fetch()
    for item in sup:
        if item.user_name == user:
            checking = item.checking
            return checking

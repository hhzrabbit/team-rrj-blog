#Manages the account info tables in the db
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O



''' 
1. authenticate: authenticate credentials
2. register: make sure username not used
'''

from hashlib import sha1

#authenticate user returns true if authentication worked
def authenticate(user,password):

    f="testerDB.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok

    correctLogin = False #Default to false; login info correct?
    passHash = sha1(password).hexdigest()#hash it
    checkUser = 'SELECT * FROM users WHERE username=="%s";' % (user)  #checks if the user is in the database
    c.execute(checkUser)
    print 'status of stuff'  #debugging stuff
    l = c.fetchone() #listifies the results
    
    
    #==========================================================
    db.commit() #save changes
    db.close()  #close database
    return "yolo"

def register(user,password,pwd):
    
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok

    theError = ""
    if (password == pwd):
        passHash = sha1(password).hexdigest()#hash it
        if (user in usrpwd.keys()):
            theError = "This username is already registered."
        else:
            if ("," in user):
                theError = "Username has invalid character (a comma)."
            else:
                #with open('data/userCsv.csv','a') as csv:
                #csv.write(user + "," + passHash + "\n")#add row in csv
                theError = "Your account was successfully created!"
                usrpwd[user] = passHash#add entry in dict
    else:
        theError = "passwords did not match"
    #==========================================================
    db.commit() #save changes
    db.close()  #close database
    return theError

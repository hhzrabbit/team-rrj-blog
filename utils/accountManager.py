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

    isLogin = False #Default to false; login info correct?
    loginStatusMessage = "" #what's wrong
    passHash = sha1(password).hexdigest()#hash it
    
    checkUser = 'SELECT * FROM users WHERE username=="%s";' % (user)  #checks if the user is in the database
    c.execute(checkUser)
    print 'status of stuff'  #debugging stuff
    l = c.fetchone() #listifies the results
    if l == None:
        isLogin = False 
        loginStatusMessage = "user does not exist"
    elif l[1] == passHash:
        isLogin = True 
        loginStatusMessage = "login info correct"
    else:
        isLogin = False 
        loginStatusMessage = "wrong password"
    print loginStatusMessage
    #==========================================================
    db.commit() #save changes
    db.close()  #close database
    return isLogin
#returns true if register worked
def register(user,password,pwd):    #user-username, password-password, pwd-retype
    
    f="testerDB.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok

    isRegister = False #defualt not work
    registerStatus = ""


    checkUser = 'SELECT * FROM users WHERE username=="%s";' % (user)  #checks if the user is in the database
    c.execute(checkUser)
    print 'status of stuff'  #debugging stuff
    l = c.fetchone() #listifies the results

    if l != None:
        isRegister = False
        registerStatus = "username taken"
    elif (password != pwd):
        isRegister = False
        registerStatus = "passwords do not match"
    elif (password == pwd):
        #get latest id
        getLatestID = "SELECT userID FROM users"
        c.execute(getLatestID)
        l = c.fetchall()
        #print max(l)[0] + 1 #debugging the tuple insanity

        passHash = sha1(password).hexdigest()#hash it
        insertUser = 'INSERT INTO users VALUES ("%s","%s",%d);' % (user,passHash,max(l)[0]+1) #sqlite code for inserting new user
        c.execute(insertUser)
        
        #debugging: check table
        print "Table"
        c.execute('SELECT * FROM users;')
        print c.fetchall()

        isRegister = True
        registerStatus = "user %s registered!" % (user)
    print registerStatus
    #==========================================================
    db.commit() #save changes
    db.close()  #close database
    return isRegister

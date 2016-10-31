#!/usr/bin/python
''' Register​: insert account into user table
2. Create​: insert story into stories table
3. Contribute​: insert record of edit into edit_logs table
ii. edit existing entries in the tables
1. Contribute​: edit story in stories table
iii. fetch data from the tables
1. Register​: make sure username not used
2. Login​: authenticate credentials
3. Feed​: pull last edit of stories user has not contributed to
a. looks at edit_logs table to see which stories the user has
contributed to
b. pulled stories can be sorted by time of creation, time of last edit, or
title
4. History​: pull full stories user has contributed to
a. looks at edit_logs table to see which stories the user has
contributed to
b. pulled stories can be sorted by time of creation, time of last edit,
time of user’s edit, or title
c. for search bar: pulls stories where title matches search query
5. Contribute​: pull last edit of the story the user is contributing to
'''
from hashlib import sha1


def authenticate(user,password):
    inIt = False
    passHash = sha1(password).hexdigest()#hash it
    #SELECT username in 
    if (user in usrpwd.keys()):
        if (passHash == usrpwd[user]):
            inIt = True
    return inIt

def register(user,password,pwd):
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
    return theError
    

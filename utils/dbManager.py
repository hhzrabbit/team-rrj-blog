#!/usr/bin/python
import time
'''
block comment describing the contents of this file
'''
import sqlite3   #enable control of an sqlite database


#testing purposes
  #p = """INSERT INTO stories VALUES("%s","%s","%s", %d, %d, %d)""" %("the Title", "the full Story", "Story", 0,0, 0)

  #c.execute(p)

def createStory(title, newEntry, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    origTime = time.time()
    fullStory = newEntry
    lastEdit = fullStory
    getLatestID = "SELECT storyId FROM stories"
    c.execute(getLatestID)
    l = c.fetchall()
    if l: #if list not empty, there are stories already
        storyId = max(l)[0]+1
    else:
        storyId = 0

    p = """INSERT INTO stories VALUES ("%s","%s","%s", %d, %d, %d)""" %(title, fullStory, lastEdit, origTime, origTime, storyId)
    c.execute(p)
    userId = getUserId(username)
    p = """INSERT INTO edit_logs VALUES (%d,%d,%d)""" %(userId,storyId,origTime)
    c.execute(p)
    db.commit()
    db.close()
    return 1

#return the userId from the username
def getUserId(username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    getId = """SELECT userId FROM users WHERE username == "%s" """ % (username)
    c.execute(getId)

    ans = c.fetchone()[0]

    db.commit()
    db.close()
    return ans

#get storyId from it's title -- this may or may not be useful
def getStoryId(title):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops
    
    p = """SELECT storyId FROM stories WHERE title == %s""" %(title)
    c.execute(p)
    ans = c.fetchone()

    db.commit()
    db.close()
    return ans

#returns whole story of story whose storyId was given
def getWholeStory(storyId):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = """SELECT fullStory FROM stories WHERE storyId == %s""" %(storyId)
    c.execute(p)

    ans = c.fetchone()
    db.commit()
    db.close()
    return ans


#returns last entry of story whose storyId was given
def getLastEnry(storyId):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = """SELECT lastEntry FROM stories WHERE storyId == %s""" %(storyId)
    c.execute(p)

    ans = c.fetchone()
    db.commit()
    db.close()
    return ans
# ^^ we dont use this and it doesnt work


#returns all necessary components to edit a story
def getEditStats(storyId):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops
    print "this is the storyId"
    
    print storyId, "hi"
    print "\n\n\n\n\n\n"
    p = """SELECT title, lastEdit FROM stories WHERE storyId == %s""" %(storyId)
    c.execute(p)

    stats = c.fetchone()
    db.commit()
    db.close()
    ans = []
    ans.append( stats[0] )
    ans.append( stats[1] )
    ans.append( storyId )
    return ans

#-------------------------------not really needed---------------------------    
#returns list of all full stories
def getAllWholeStory():
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = """SELECT fullStory FROM stories"""
    c.execute(p)

    ans = c.fetchall()
    db.commit()
    db.close()
    return ans
    
#returns list of all last entries
def getAllLastEntry():
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = """SELECT lastEntry FROM stories"""
    c.execute(p)

    ans = c.fetchall()
    db.commit()
    db.close()
    return ans

#-----------------------------------------------------------------------------

#testing insertion
  #p = """INSERT INTO stories VALUES("%s", "%s", "%s", %d, %d, %d)""" %("this is title", "this is","is",0,0,0)

  #c.execute(p)

#createStory("this is the title","this is the new entry","anya")
#createStory("hi all","beginning of story","software")
#createStory("im creating another story","this is the beginning of my new story","anya")

#update the full story, last edit, and latest time
#connect story submission with user
def updateStory(storyId, newEdit, userId):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    #updating stories table
    p = """UPDATE stories SET lastEdit = "%s" WHERE storyId == %d"""%(newEdit, storyId)
    c.execute(p)
    #makes tuple into a string -- wholeStory = ''.join(getWholeStory(storyId))
    wholeStory = getWholeStory(storyId)[0]
    wholeStory += " HOW DO WE GET A NEW LINE HERE " + newEdit
    p = """UPDATE stories SET fullStory = "%s" WHERE storyId == %d"""%(wholeStory, storyId)
    c.execute(p)
    nowTime = time.time()
    p = """UPDATE stories SET latestTime = %d WHERE storyId == %d"""%(nowTime,storyId)
    c.execute(p)
    #updating edit_logs table
    p = """INSERT INTO edit_logs VALUES(%d,%d,%d)""" %(userId, storyId,nowTime)
    c.execute(p)
    db.commit()
    db.close()
#testing updateStory
    #updateStory(1,"this is a new edit", 0)

#to return a chronological list with most recent first of all the stories that the person has edited already
#if flag 0 - by date, if flag 1 - by title
def doneStories(username, flag):
    if flag == 0:
        retVal = dSortDate(username)
    else:
        retVal = dSortTitle(username)
    return retVal

#helper for sorting by date        
def dSortDate(username):      
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    userId = getUserId(username)
    p = """SELECT storyId,time FROM edit_logs WHERE userId == %d"""%(userId)
    c.execute(p)
    totalTuple = c.fetchall()
    theIds = list(totalTuple)#make tuple a list -- easier to work with
    order = sorted(theIds, key=getKey)
    finalList = []
    for story in order:
        p = """SELECT title,latestTime,fullStory FROM stories WHERE storyId == %d"""%(story[0])
        c.execute(p)
        totes = c.fetchall()
        theWhole = []
        for i in totes:
            theWhole.append(list(i))
        finalList.append(theWhole[0])
    return finalList
    db.commit()
    db.close()

#helper for sorting by title
def dStoryTitle(username):
    return "not there yet"

#to return a tuple of the stories that the person has not edited (just the last entry would be displayed)

def undoneStories(username, flag):
    if flag == 0:
        retVal = uSortDate(username)
    else:
        retVal = uSortTitle(username)
    return retVal

def uSortDate(username):    
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    userId = getUserId(username)
    print "userId:", userId, "\n\n\n\n\n"
    p = """SELECT storyId FROM edit_logs WHERE userId == %d"""%(userId)
    c.execute(p)
    badOne = c.fetchall()
    print "badOne:", badOne, "\n\n\n\n\n"
    p = """SELECT storyId,origTime FROM stories"""
    c.execute(p)
    allOne = c.fetchall()
    print "allOne:", allOne, "\n\n\n\n\n"
    theIds = []
    alreadyCompleted = False
    for one in allOne:
        print 6
        for storyId in badOne:
            if one[0] == storyId[0]:
                print "found", one[0]
                alreadyCompleted = True
               # break
        if not alreadyCompleted:
            theIds.append(one)
        alreadyCompleted = False
    #theIds = list(totalTuple)#make tuple a list -- easier to work with
    order = sorted(theIds, key=getKey)
    print order
    finalList = []
    for story in order:
        p = """SELECT title,latestTime,lastEdit,storyId FROM stories WHERE storyId == %d"""%(story[0])
        c.execute(p)
        totes = c.fetchall()
        theWhole = []
        for i in totes:
            theWhole.append(list(i))
        finalList.append(theWhole[0])
    print "finalList:", finalList, "\n\n\n\n\n"
    return finalList
    db.commit()
    db.close()

def uStoryTitle(username):
    return "not there yet"

#helper fxn for sorting a 2d list
def getKey(item):
    return item[1]#returns second entry


#testing purposes
#print doneStories("anya")
#print undoneStories("anya")


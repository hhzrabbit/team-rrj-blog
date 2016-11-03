#!/usr/bin/python
import time
'''
block comment describing the contents of this file
'''
import sqlite3   #enable control of an sqlite database
f = "database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#testing purposes
  #p = """INSERT INTO stories VALUES("%s","%s","%s", %d, %d, %d)""" %("the Title", "the full Story", "Story", 0,0, 0)

  #c.execute(p)

def createStory(title, newEntry, username):
    origTime = time.time()
    fullStory = newEntry
    lastEdit = fullStory
    getLatestID = "SELECT storyId FROM stories"
    c.execute(getLatestID)
    l = c.fetchall()
    storyId = max(l)[0]+1

    p = """INSERT INTO stories VALUES ("%s","%s","%s", %d, %d, %d)""" %(title, fullStory, lastEdit, origTime, origTime, storyId)
    c.execute(p)
    userId = getUserId(username)
    p = """INSERT INTO edit_logs VALUES (%d,%d,%d)""" %(userId,storyId,origTime)
    c.execute(p)

#return the userId from the username
def getUserId(username):
    getId = """SELECT userId FROM users WHERE username == "%s" """ %(username)
    c.execute(getId)
    return c.fetchone()[0]

#get storyId from it's title -- this may or may not be useful
def getStoryId(title):
    p = """SELECT storyId FROM stories WHERE title == %s""" %(title)
    c.execute(p)
    return c.fetchone()

#returns whole story of story whose storyId was given
def getWholeStory(storyId):
    p = """SELECT fullStory FROM stories WHERE storyId == %s""" %(storyId)
    c.execute(p)
    return c.fetchone()
    
#returns last entry of story whose storyId was given
def getLastEnry(storyId):
    p = """SELECT lastEntry FROM stories WHERE storyId == %s""" %(storyId)
    c.execute(p)
    return c.fetchone()
#-------------------------------not really needed---------------------------    
#returns list of all full stories
def getAllWholeStory():
    p = """SELECT fullStory FROM stories"""
    c.execute(p)
    return c.fetchall()
    
#returns list of all last entries
def getAllLastEntry():
    p = """SELECT lastEntry FROM stories"""
    c.execute(p)
    return c.fetchall()
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
    #updating stories table
    p = """UPDATE stories SET lastEdit = "%s" WHERE storyId == %d"""%(newEdit, storyId)
    c.execute(p)
    #makes tuple into a string -- wholeStory = ''.join(getWholeStory(storyId))
    wholeStory = getWholeStory(storyId)[0]
    wholeStory += " " + newEdit
    p = """UPDATE stories SET fullStory = "%s" WHERE storyId == %d"""%(wholeStory, storyId)
    c.execute(p)
    nowTime = time.time()
    p = """UPDATE stories SET latestTime = %d WHERE storyId == %d"""%(nowTime,storyId)
    c.execute(p)
    #updating edit_logs table
    p = """INSERT INTO edit_logs VALUES(%d,%d,%d)""" %(userId, storyId,nowTime)
    c.execute(p)

#testing updateStory
    #updateStory(1,"this is a new edit", 0)

#to return a chronological list with most recent first of all the stories that the person has edited already

def doneStories(username):
    userId = getUserId(username)
    p = """SELECT storyId,time FROM edit_logs WHERE userId == %d"""%(userId)
    c.execute(p)
    totalTuple = c.fetchall()
    theIds = list(totalTuple)#make tuple a list -- easier to work with
    order = sorted(theIds, key=getKey)
    finalList = []
    for story in order:
        p = """SELECT fullStory FROM stories WHERE storyId == %d"""%(story[0])
        c.execute(p)
        newThing = c.fetchone()[0]
        finalList.append(newThing)
    return finalList

#to return a tuple of the stories that the person has not edited (just the last entry would be displayed)

def undoneStories(username):
    userId = getUserId(username)
    p = """SELECT storyId,time FROM edit_logs WHERE userId != %d"""%(userId)
    c.execute(p)
    totalTuple = c.fetchall()
    theIds = list(totalTuple)#make tuple a list -- easier to work with
    order = sorted(theIds, key=getKey)
    finalList = []
    for story in order:
        p = """SELECT lastEdit FROM stories WHERE storyId == %d"""%(story[0])
        c.execute(p)
        newThing = c.fetchone()[0]
        finalList.append(newThing)
    return finalList

#helper fxn for sorting a 2d list
def getKey(item):
    return item[1]#returns second entry


#testing purposes
  #print doneStories("anya")
  #print undoneStories("anya")

    
db.commit()
db.close()

#!/usr/bin/python
import time
'''
block comment describing the contents of this file
'''
import sqlite3   #enable control of an sqlite database
f = "database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

def createStory(title, newEntry, username):
    origTime = time.time()
    fullStory = newEntry
    lastEdit = fullStory
    getLatestID = "SELECT storyId FROM stories"
    c.execute(getLatestID)
    l = c.fetchall()
    storyId = max(l)[0]+1

    p = "INSERT INTO stories VALUES (%s,%s,%s,%d,%d)" %(theTitle, fullStory, lastEdit, origTime,storyId)
    c.execute(p)
    getUserId = "SELECT userId FROM users WHERE username == %s" %(username)
    c.execute(getUserId)
    userId = c.fetchone()
    
    p = "INSERT INTO edit_logs VALUES (%d,%d,%d)"%(userId,storyId,origTime)
    c.execute(p)

db.commit()
db.close()

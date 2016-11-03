#!/usr/bin/python
'''
block comment describing the contents of this file
'''
import sqlite3   #enable control of an sqlite database
f = "database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#------------------------create tables---------------------------------------
q = "CREATE TABLE users (username TEXT, password TEXT, userId INTEGER)"
c.execute(q)

q="CREATE TABLE stories (title TEXT,fullStory TEXT,lastEdit TEXT, origTime INTEGER,latestTime INTEGER, storyId INTEGER)"
c.execute(q)

q="CREATE TABLE edit_logs (userId INTEGER, storyId INTEGER, time INTEGER)"
c.execute(q)
#add random stuff for testing
#-------------------------------------------------------------------------------

#---------------------------put stuff in tables---------------------------------
q = """INSERT INTO users VALUES ("anya", "hashedpass", 0)"""
c.execute(q)
q = """INSERT INTO TABLE stories("the title","the whole entire story.","entire story.",0,0,0)"""
c.execute(q)
#-------------------------------------------------------------------------------
db.commit()
db.close()

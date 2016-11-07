from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from  utils import accountManager, dbManager

app = Flask(__name__)
f = open( "utils/key", 'r' )
app.secret_key = f.read();
f.close

#how to sort feed and history
sortFeedBy = 0
sortHistoryBy = 0

#root, two behaviors:
#    if logged in: redirects you to your feed
#    if not logged in: displays log in/register page
@app.route("/")
def loginOrRegister():
    if 'username' in session:
        return redirect("/feed")
    else:
        return render_template("loginOrReg.html")

#handles input of the login register page
@app.route("/authOrCreate", methods=["POST"])
def authOrCreate():
    formDict = request.form
    print formDict #for debugging
    if formDict["logOrReg"] == "login":
        username = formDict["username"]
        password = formDict["password"]
        loginStatus = "login failed"
        statusNum = accountManager.authenticate(username,password) #returns 0,1 or 2 for login status messate
        if statusNum == 0:
            loginStatus = "user does not exist"
        elif statusNum == 1:
            session["username"]=username
            loginStatus = username + " logged in"
            return redirect( "/feed" )
        elif statusNum == 2:
            loginStatus = "wrong password"

        return render_template("loginOrReg.html",status=loginStatus)

    elif formDict["logOrReg"] == "register":  #registering
        username = formDict["username"]
        password = formDict["password"]
        pwd = formDict["pwd"]  #confirm password
        registerStatus = "register failed"
        statusNum = accountManager.register(username,password,pwd) #returns true or false
        if statusNum == 0:
            registerStatus = "username taken"
        elif statusNum == 1:
            registerStatus = "passwords do not match"
        elif statusNum == 2:
            registerStatus = username +" account created"

        return render_template("loginOrReg.html",status=registerStatus) #status is the login/creation messate 
    else:
        return redirect(url_for("loginOrReg"))

#logout of user
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop('username')
        return render_template("loginOrReg.html",status="logged out") 
    else:
        return redirect(url_for('loginOrRegister'))

#dictates how to sort stories in the feed
@app.route("/sortfeed", methods=["POST"])
def sortfeed():
    formDict = request.form
    print "f", formDict
    #for e in formDict:
     #   print e
    sortBy = formDict[ "sortBy" ]
    print sortBy
    global sortFeedBy
    sortFeedBy = int(sortBy)
    return redirect("/feed")
    
#every story in the feed will have a form submit button
#upon form submit it will send post ID to edit()
@app.route("/feed")
def storiesFeed():
    if 'username' in session:
        print session
        storys = dbManager.undoneStories( session['username'], sortFeedBy)
        if storys: #not empty, meaning there are stories to show
            return render_template('feed.html', user = session["username"], stories = storys)
        else:
            return render_template('feed.html', user = session["username"], message = "No stories to show.")
    else:
        return redirect(url_for('loginOrRegister'))

#called when someone clicks the form submit button next to one of the stories in feed
#edit the story
@app.route("/edit", methods=["POST"])
def edit():
    formDict = request.form
    ID = formDict[ "storyId" ]
    stats = dbManager.getEditStats( ID )
    return render_template('edit.html', user = session["username"], info = stats)

#backend of editing story
@app.route("/recieveEdit", methods=['POST'])
def recieveEdit():
    formDict = request.form
    addition = formDict[ "content" ]
    storyID = int(formDict[ "storyId" ])
    uID = dbManager.getUserId( session[ "username" ] )
    dbManager.updateStory( storyID, addition, uID )
    
    return redirect("/history")

#change criteria of sorting history
@app.route("/sorthistory", methods=["POST"])
def sorthistory():
    formDict = request.form
    print "f", formDict
    sortBy = formDict[ "sortBy" ]
    print sortBy
    global sortHistoryBy
    sortHistoryBy = int(sortBy)
    return redirect("/history")

#display history -- feed of the stories you have contributed to
@app.route("/history")
def history():
    if 'username' in session:
        storys = dbManager.doneStories( session['username'], sortHistoryBy)#testing alphabetize
        print storys
        if storys: #not empty, meaning there are stories to show
            return render_template('history.html', user = session["username"], stories = storys)
        else:
            return render_template('history.html', user = session["username"], message = "No stories to show.")

    else:
        return redirect("/")

#create a new story
@app.route("/create")
def newStory():
    if 'username' in session:
        return render_template('create.html', user = session["username"])
    else:
        return redirect("/")
    
#backend of creating new story
@app.route("/recieveCreate", methods=['POST'])
def recieveCreate():
    formDict = request.form
    storyTitle = formDict["storyTitle"]
    storyContent = formDict["storyContent"]
    dbManager.createStory( storyTitle, storyContent, session["username"] )
    return redirect("/history")



if __name__ == "__main__":
    app.debug = True
    app.run()

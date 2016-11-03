from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from  utils import accountManager, dbManager

app = Flask(__name__)
f = open( "utils/key", 'r' )
app.secret_key = f.read();
f.close

#tells apache what to do when browser requests access from root of flask app
@app.route("/")
def loginOrRegister():
    return render_template("loginOrReg.html")

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
            registerStatus = username +" account Created"

        return render_template("loginOrReg.html",status=registerStatus) #status is the login/creation messate 
    else:
        return redirect(url_for("loginOrReg"))

@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop('username')
        return render_template("loginOrReg.html",status=" logged out") 
    else:
        return redirect(url_for('loginOrRegister'))


#every story in the feed will have a form submit button
#upon form submit it will send post ID to edit()
@app.route("/feed")
def storiesFeed():
    if 'username' in session:
        print session
        return render_template('feed.html', user = session["username"])
    else:
        return redirect(url_for('loginOrRegister'))
    
@app.route("/edit", methods=["POST"])
def edit():
    if 'username' in session:
        return render_template('edit.html', user = session["username"])
    else:
        return redirect("/")
    
@app.route("/history")
def history():
    if 'username' in session:
        storys = dbManager.doneStories( session['username'] )
        print storys
        return render_template('history.html', user = session["username"], stories = storys)
    else:
        return redirect("/")
   
@app.route("/create")
def newStory():
    if 'username' in session:
        return render_template('create.html', user = session["username"])
    else:
        return redirect("/")
        
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

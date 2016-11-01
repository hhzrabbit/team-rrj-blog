from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils.accountManager

app = Flask(__name__)
f = open( "utils/key", 'r' )
app.secret_key = f.read();
f.close

#tells apache what to do when browser requests access from root of flask app
@app.route("/")
def loginOrRegister():
    return ""

@app.route("/authOrCreate", methods=["POST"])
def authOrCreate():
    formDict = request.form
    if formDict["logOrReg"] == "login":
        username = formDict["username"]
        password = formDict["password"]
        loginStatus = "login failed"
        if accountManager.authenticate(username,password): #returns true or false
            session["username"]=username
            loginStatus = username + " logged in"
        return redirect(url_for("/",status=loginStatus))
    elif formDict["logOrReg"] == "register":
        username = formDict["username"]
        password = formDict["password"]
        pwd = formDict["pwd"]  #confirm password
        registerStatus = "register failed"
        if accountManager.register(username,password,pwd): #returns true or false
            registerStatus = "Account Created"
        return redirect(url_for("authOrCreate",status=registerStatus)) #status is the login/creation messate 
    else:
        return redirect(url_for("/"))

#every story in the feed will have a form submit button
#upon form submit it will send post ID to edit()
@app.route("/feed")
def storiesFeed():
    return render_template('feed.html')

@app.route("/edit", methods=["POST", "GET"])
def edit():
    #postID = request.form['id']
    return render_template('edit.html')

@app.route("/history")
def history():
    return render_template('history.html')


@app.route("/create")
def newStory():
    return render_template('create.html')


if __name__ == "__main__":
    app.debug = True
    app.run()

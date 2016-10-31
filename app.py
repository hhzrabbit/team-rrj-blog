from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(32) 

#tells apache what to do when browser requests access from root of flask app
@app.route("/")
def loginOrRegister():
    return ""

#every story in the feed will have a form submit button
#upon form submit it will send post ID to edit()
@app.route("/feed")
def storiesFeed():
    return ""

@app.route("/edit", methods=["POST"])
def edit():
    postID = request.form['id']
    
@app.route("/history")
def history():
    return ""

@app.route("/create")
def newStory():
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()

from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os

app = Flask(__name__)
f = open( "utils/key", 'r' )
app.secret_key = f.read();
f.close

#tells apache what to do when browser requests access from root of flask app
@app.route("/")
def loginOrRegister():
    return ""

#every story in the feed will have a form submit button
#upon form submit it will send post ID to edit()
@app.route("/feed")
def storiesFeed():

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

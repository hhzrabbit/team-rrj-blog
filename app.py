from flask import Flask, render_template
import utils.script

#this is a constructor call
#creating an instance of a class
app = Flask(__name__) 

#tells apache what to do when browser requests access from root of flask app
@app.route("/")
def loginOrRegister():
    return ""
    
@app.route("/feed")
def storiesFeed():
    return ""
    
@app.route("/history")
def history():
    return ""

@app.route("/create")
def newStory():
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()

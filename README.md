Collaboroddative Story Maker: ~~a collabor...~~ the title is self explanatory 
===============================================
- [About] (#about)
  - [Setting Up] (#setting-up)
  - [Creating an Account] (#creating-an-account)
  - [Logging In/Out] (#logging-inout)
  - [Start New Story] (#start-new-story)
  - [The Feed] (#the-feed)
  - [History] (#history)

About
----------
Welcome to the CollaboRoddative Story Maker! Grab a couple of friends and start playing this exciting, team-building game! This game is a mix of mad-libs, telephone, and that one game we all played but has no name where you sit in a circle with your friends and build a story one word at a time and the first person who stutters loses.. yeah, that one -- the CollaboRoddative Story Maker combines the best of three worlds!

This brilliant amazing dazzling trailblazing fun-for-the-whole-family game was built by Team Rodda Reimer John, consisting of Anya Keller, Bayle Smith-Salzberg, Jack Schluger, and Haley Zeng, of Mr. Brown Mykolyk's Pd 8 Softdev class.

### Setting Up

To set up the game for the first time:
```
$ python utils/initialize.py
```

To run the server:
```
$ python app.py
```

### Creating an Account

You must come up with a username, and a distinct 5-63 character password cconsisting of only alphanumeric characters.  Fill in desired username in the username field under register.  Fill in desired password in both password fields under register.  Click the register button.  

If the message says account created, you're registerd!
If it says username taken, you have to choose a new username and try again.  
If it says passwords do not match, try filling out the form with the same username and password, this message occurs when the user types two different passwords in the password fields under register.

### Logging In/Out

Fill in your chosen username in the username field under login.  Fill in your account password in the field under login.  Click the login button.

If the message says you've logged in, you're logged in!
If the message says the username does not exist, make sure you typed the username correctly and try logging in again.
If the message says password inccorect, make sure you typed the password correctly and try logging in again.

### Start New Story

Click on the "Create" button on the navbar to start a new story. You will be prompted to enter a title and the contents of your story. Once you submit your story, it will be stored in the database and other users will be able to contribute to it!

### The Feed

Click on the "Feed" button on the navbar to see a feed of stories other users have submitted. If you see one that interests you, click the Edit button and contribute to the story! Once you contribute to a story, the story will be moved to your history.

### History

Click on the "History" button on the navbar to see a feed of stories you have contributed to. The full stories will be shown. You may not contribute to these stories again.


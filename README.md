Feel free to contribute to this project or suggest more features to add.
# Updates
19032023: Will add an option to use a proxy with the bot in the next few days.<br/>
NOTE: V2.0 is the newest version of the bot, that is proven to work.<br/>
01032023: I'm working on a better version of this project. It will have quite so many more features; such as a web interface for the bot(aka frontend), the bot will run even if Reddit changes their site structure, it will also have it's own mysql database for better data management... I will change README.md once I'm done, it should take a few weeks.<br/>
[Ignore]24022022: Added GU.py and usernames.json to the project. GU gets usernames and writes them to usernames.json<br/>
[Ignore]18012022: I ran some bots that resulted in Reddit changing the structre of some of their web pages, BotV3.0.py is the up to date version.<br/>

# How to use
0 - Have Python and Pip installed. Clone this repository. Run ```pip install -r r.txt```<br/>
1 - Add an account to ```account.py```<br/>
2 - Change the variables that needs to be changed in ```variables.py```<br/>
3 - Run ```fillUsernames.csv.py``` to get usernames into ```usernames.csv```, or fill it yourself (:<br/>
4 - Run ```py.py```

# How does it work?
RedditDMBot is a bot made for the purpouse of automating the process of sending messages to Reddit users<br/>
What the bot does:<br/>
1 - Scrapes all the users that made comments with the Keywords specified<br/>
2 - Logs into your Reddit account<br/>
3 - Navigates to chat page<br/>
4 - Checks if the user already received a message<br/>
5 - Sends a message to the user<br/>
6 - Appends the user to a list of users that already received messages<br/>
7 - Deletes the user from the list of users<br/>

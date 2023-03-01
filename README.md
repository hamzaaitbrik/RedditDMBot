# RedditMassDM

# UPDATE 01032023: I'm working on a better version of this project. It will have quite so many more features; such as a web interface for the bot(aka frontend), the bot will run even if Reddit changes their site structure, it will also have it's own mysql database for better data management... I will change README.md once I'm done, it should take a few weeks.

# UPDATE 24022022: Added GU.py and usernames.json to the project. GU gets usernames and writes them to usernames.json

# UPDATE: I ran some bots that resulted in Reddit changing the structre of some of their web pages, BotV3.0.py is the up to date version.

# NOTE: The script needs to be modified, read the comments, add as many keywords as you can, each keyword returns 100 users from the API
RedditSeleniumBot is a bot made for the purpouse of automating the process of sending messages to Reddit users<br/>
What the bot does:<br/>
1 - Logs into your Reddit account<br/>
2 - Scrapes all the users that made comments with the Keywords specified<br/>
3 - Navigates to the user page<br/>
4 - Checks if the user already received a message<br/>
5 - Sends a message to the user<br/>
6 - Appends the user to a list of users that already received messages<br/>
7 - Deletes the user from the list of users<br/>
8 - Recalls get_usernames() and send_messages()<br/>

# Important: Always use the latest version; Reddit keeps on changing the structure of their site everytime they detect bot activities..
In V2.0, the bot navigates to a private chat room to prevent the 'Fetching Messages' problem. V2.0 works like a charm.

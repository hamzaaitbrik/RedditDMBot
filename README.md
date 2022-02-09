# RedditSeleniumBot
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

# Important: Use the V2.0 instead of V1.0
In V2.0, the bot navigates to a private chat room to prevent the 'Fetching Messages' problem. V2.0 works like a charm.

# Update: I ran some bots that resulted in Reddit changing the structre of some of their web pages, BotV3.0.py is the up to date version.

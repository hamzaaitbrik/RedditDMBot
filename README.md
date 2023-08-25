Feel free to contribute to this project or suggest more features to add. You can reach me on Discord: OzymandiasTheGreat#3112
# Notice
This project hasn't been tested in months, it might not work, and it is currently not being developed further more due to some life complications. I will start working on it in a few weeks.
# Updates
IMPORTANT: The script ```fillUsernames.csv.py``` is currently not working due to Reddit commercializing their API and charging to use it. You can fill ```/db/usernames.csv``` yourself while I develop a solution.<br/>
NOTE: 18/05/2023's version is the newest version that is proven to work. The only inconvenience is that the bot gets stopped after sending a dozen messages, to counter this I added an amount of time to wait between messages that you can change in config file, feel free to shoot me a DM on Discord with possible solutions and I'll implement them. <br/>

# In progress
1 - Add an option to use a proxy with the bot. Estimated to be up and running by the 15th of June 2023<br/>
2 - Add an option to loop through multiple bots, if one banned switch to another. Estimated to be up and running by the month of July 2023<br/>
3 - Add a UI(User Interface). I haven't started working on this, I think the bot will remain a CLI-only tool for now.

# How to use
0 - Have Python and Pip installed. Clone this repository. Run ```pip install -r r.txt```<br/>
1 - Add an account to ```account.py```<br/>
2 - Change what needs to be changed in ```config.py```<br/>
3 - Run ```fillUsernames.csv.py``` to get usernames into ```/db/usernames.csv```, or fill it yourself (:<br/>
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

Feel free to contribute to this project or suggest more features to add. You can reach me on Discord @**ozymandiasthegreat**.
# What's new?
Multi-accounting implemented in Python.

# Notice
Java version is under development, to allow more functionality for managing accounts and proxies..

# Updates
This software is tested on 2nd of February, 2024. It is working..<br>

# In progress
1 - Add an option to use a proxy with the bot.<br>
2 - Add a UI(User Interface). I haven't started working on this, I think the bot will remain a CLI-only tool for now.

# How to use
0 - Have Python and Pip installed. Clone this repository running the command ```git clone https://github.com/hamzaaitbrik/RedditDMBot.git``` or simply [Download it](https://github.com/hamzaaitbrik/RedditDMBot/archive/refs/heads/main.zip). Then run ```pip install -r requirements.txt``` to install dependencies<br>
1 - Add accounts to ```rdt/account.json```. Refer to [Documentation](https://github.com/hamzaaitbrik/RedditDMBot/blob/main/rdt/README.md) to see how to properly add accounts.<br>
2 - Change what needs to be changed in ```rsrc/config.json```. Refer to [Documentation](https://github.com/hamzaaitbrik/RedditDMBot/blob/main/rsrc/README.md) to see how to change values to meet your needs.<br>
3 - Fill ```db/usernames.csv``` with all the usernames you want to DM<br>
4 - Run ```start.py```

# How does it work?
RedditDMBot is a bot made for the purpouse of automating the process of sending messages to Reddit users<br>
What the bot does:<br>
1 - Logs into one of the Reddit account in ```accounts.json```<br>
2 - Navigates to chat page<br>
3 - Checks if the user already received a message<br>
4 - Sends a message to the user<br>
5 - Appends the user to a list of users that already received messages<br>
6 - Deletes the user from the list of users<br>
7 - Logs out of the account used to DM the user<br>
8 - Remove it from the list of available accounts and add it to a list of used accounts<br>
9 - Logs into another Reddit account that wasn't used<br>
10 - If there are no many available accounts, the bot reuses the used accounts until all users on your ```db/usernames.csv``` received DMs.


<br><br><br>
Enjoy!
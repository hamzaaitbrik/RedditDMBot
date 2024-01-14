Feel free to contribute to this project or suggest more features to add. You can reach me on Discord @ozymandiasthegreat.
# Notice
V4.0 is under development.

# Updates
This software is tested on 14th of January, 2024. It is working..<br/>

# In progress
1 - Add an option to use a proxy with the bot. Estimated to be up and running by the 15th of June 2023<br/>
2 - Add an option to loop through multiple bots, if one banned switch to another. Estimated to be up and running by the month of July 2023<br/>
3 - Add a UI(User Interface). I haven't started working on this, I think the bot will remain a CLI-only tool for now.

# How to use
0 - Have Python and Pip installed. Clone this repository. Run ```pip install -r requirements.txt```<br/>
1 - Add an account to ```rdt/account.py```<br/>
2 - Change what needs to be changed in ```src/config.py```<br/>
3 - Fill ```db/usernames.csv``` with all the usernames you want to DM<br/>
4 - Run ```start.py```

# How does it work?
RedditDMBot is a bot made for the purpouse of automating the process of sending messages to Reddit users<br/>
What the bot does:<br/>
1 - Logs into your Reddit account<br/>
2 - Navigates to chat page<br/>
3 - Checks if the user already received a message<br/>
4 - Sends a message to the user<br/>
5 - Appends the user to a list of users that already received messages<br/>
6 - Deletes the user from the list of users<br/>

**[Click here](https://discord.gg/Y5NeDy5XXT) to join the Discord server for this project, let's connect!**<br>
**[Click here](https://t.me/RedditDMBot) to join the Telegram channel for this project, in case Discord server goes down. Let's connect!**<br>

Feel free to contribute to this project or suggest more features to add. You can reach me on Discord @**ozymandiasthegreat**.
# What's new?
I changed the technology which the software depend on to a private framework I built on top of [Zendriver](https://github.com/stephanlensky/zendriver). The reason I changed the framework is because Playwright and Selenium are easily detected by Reddit, unlike Zendriver that uses CDP to connect to Chrome.<br>
I also added functionality so that you only need to provide the bot with plain usernames of users you want to DM, unlike the older version which required you to get a datapoint Reddit has on its backend.

# Importnat
There are three versions of the bot, [Selenium](https://github.com/hamzaaitbrik/RedditDMBot/tree/selenium), [Playwright](https://github.com/hamzaaitbrik/RedditDMBot), and [Zendriver](https://github.com/hamzaaitbrik/RedditDMBot/tree/zendriver). Zendriver version is tested as of the 22nd of April 2025. **Zendriver version performs better than the rest.**<br>

# Prerequisites
0 - Have ```Python``` and ```Pip``` installed. This project was developed with Python 3.11.8<br>
1 - Clone this repository running the command ```git clone https://github.com/hamzaaitbrik/RedditDMBot.git``` or simply [Download it](https://github.com/hamzaaitbrik/RedditDMBot/archive/refs/heads/zendriver.zip).<br>
2 - Install ```Pipenv``` using the command ```pip install pipenv```.<br>
3 - Run ```pipenv install``` inside the project to install its dependencies.<br>

# How to use
1 - Add accounts to ```rdt/account.json```. Refer to [rdt/README](https://github.com/hamzaaitbrik/RedditDMBot/blob/playwright/rdt/README.md) to see how to properly add accounts.<br>
2 - Change what needs to be changed in ```rsrc/config.json```. Refer to [rsrc/README](https://github.com/hamzaaitbrik/RedditDMBot/blob/playwright/rsrc/README.md) to see how to change values to meet your needs.<br>
3 - Add proxies to ```rsrc/proxies.json``` to use the bot with proxies.<br>
4 - Fill ```db/usernames.csv``` with all the **usernames** you want to DM.<br>
5 - Run ```RedditDMBot.py```.

# How does it work?
RedditDMBot is a bot made for the purpouse of automating the process of sending messages to Reddit users<br>
What the bot does:<br>
0 - The bot checks whether you have a proxy in ```rsrc/config.json```, all actions will be made through the proxy if found. Refer to [rsrc/README](https://github.com/hamzaaitbrik/RedditDMBot/blob/playwright/rsrc/README.md) to better understand how to properly add a proxy.<br>
1 - Logs into one of the Reddit account in ```accounts.json```.<br>
2 - Navigates to chat page.<br>
3 - Checks if the user already received a message.<br>
4 - Sends a message to the user.<br>
5 - Deletes the user from the list of users to DM and adds it to ```db/usernames_sent.csv```.<br>
6 - Logs out of the account used to DM the user.<br>
7 - Remove it from the list of available accounts and add it to a list of used accounts.<br>
8 - Logs into another Reddit account that wasn't used.<br>
9 - If there are no many available accounts, the bot reuses the used accounts until all users on your ```db/usernames.csv``` received DMs.

# In action!
![In action!](https://github.com/hamzaaitbrik/RedditDMBot/blob/playwright/media/InAction!.png "In action!")

<br><br>
Enjoy!

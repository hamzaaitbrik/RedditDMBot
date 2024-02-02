Ignore ```links.json``` and ```xpath.json```, those aren't meant to be modified.
# How to change the configuration of the bot?
The basic configuration that ships with the bot looks like this:
```
{
    "cooldown":5,
    "headless":false,
    "messages":[
        "",
        ""
    ]
}
```
```cooldown``` is the number of seconds the bot will wait between DMs. I advise to keep it at 5 seconds minimum if you're multi-accounting. If you have a single account, it's best to increase that number to somewhere near 60-120 seconds.<br>
```headless``` is the indicator of whether to run the bot in headless mode or not, in headless mode you will not be able to see what the bot does. If you're testing, I advise to keep headless on ```false```. If you want to run multiple bots, then switch the value of headless to ```true```. The bot runs better on headless mode because less resources are being consumed.<br>
```messages``` is the list of messages you want to send, you can have one message in there. Otherwise, the more messages you add, the bot will keep choosing a message in a random way to prevent being detected and shadowbanned.
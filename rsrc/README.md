Feel free to reach me on Discord @**ozymandiasthegreat** in case you need assistance.<br><br>
Ignore ```js/*```, ```links.json``` and ```xpath.json```, those aren't meant to be modified.
# How to change the configuration of the bot?
The basic configuration that ships with the bot looks like this:
```
{
    "proxy":{
        "proxy":"localhost",
        "proxyRotationLink":"",
        "proxyRotationCooldown":20
    },
    "cooldown":5,
    "headless":false,
    "messages":[
        "",
        ""
    ]
}
```
<br>

```proxy``` is the configuration of the proxy, it is default to ```localhost``` and empty ```proxyRotationLink```; meaning no proxy. To add a proxy, simply replace ```localhost``` with ```host:port:user:pass``` in that format. ```proxyRotationLink``` is the link the bot will use to rotate the IP of the proxy assuming you have a proxy that rotates its IP, leave empty if you don't have. ```proxyRotationCooldown``` is the amount of time your proxy takes to rotate, it is ignored if ```proxy``` is equal to ```localhost```.<br>
The bot **for now** only supports the use of one proxy with authentication; more functionality will be added. In this case, make sure you get an authenticated proxy that rotates its IP.<br>
This is how proxy part should look like:<br>
```
"proxy":{
        "proxy":"host:port:username:password",
        "proxyRotationLink":"http://link_that_will_rotate_the_ip_of_the_proxy"
    }
```
<br>

```cooldown``` is the number of seconds the bot will wait between DMs. I advise to keep it at 5 seconds minimum if you're multi-accounting. If you have a single account, it's best to increase that number to somewhere near 60-120 seconds.<br><br>
```headless``` is the indicator of whether to run the bot in headless mode or not, in headless mode you will not be able to see what the bot does. If you're testing, I advise to keep headless on ```false```. If you want to run multiple bots, then switch the value of headless to ```true```. The bot runs better on headless mode because less resources are being consumed.<br><br>
```messages``` is the list of messages you want to send, you can have one message in there. Otherwise, the more messages you add, the bot will keep choosing a message in a random way to prevent being detected and shadowbanned.
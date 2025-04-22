Feel free to reach me on Discord @**ozymandiasthegreat** in case you need assistance.<br><br>
Ignore ```links.json``` and ```locators.json```, those aren't meant to be modified.
# How to change the configuration of the bot?
The basic configuration that ships with the bot looks like this:
```
{
    "proxy":{
        "proxy_type":"localhost",
        "proxy_rotation_link":"",
        "proxy_rotation_cooldown":20
    },
    "cooldown":3.5,
    "headless":false,
    "browser_args":[
        "--start-maximized",
        "--disable-background-networking",
        "--disable-sync",
        "--blink-settings=imagesEnabled=false",
        "--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints"
    ],
    "messages":[
        "",
        ""
    ]
}
```
<br>

```proxy``` is the configuration of the proxy, it is default to ```localhost``` and empty ```proxyRotationLink```; meaning no proxy will be used. To add a proxy, simply replace ```localhost``` with either ```sticky``` or ```rotative```, ```sticky``` option will make the bot get the list of sticky proxies from ```rsrc/proxies.json```, ```rotative``` option will make the bot get the list of rotative proxies from ```rsrc/proxies.json```; note that the bot only supports the use of one rotative option for now. ```proxyRotationLink``` is the link the bot will use to rotate the IP of the proxy assuming you have a proxy that rotates its IP, leave empty if you don't have. ```proxyRotationCooldown``` is the amount of time your proxy takes to rotate, it is ignored if ```proxy``` is equal to ```localhost``` or if ```proxyRotationLink``` is empty.<br><br>
```cooldown``` is the number of seconds the bot will wait between DMs. I advise to keep it at 5 seconds minimum if you're multi-accounting. If you have a single account, it's best to increase that number to somewhere near 60-120 seconds.<br><br>
```headless``` is the indicator of whether to run the bot in headless mode or not, in headless mode you will not be able to see what the bot does. If you're testing, I advise to keep headless on ```false```. If you want to run multiple bots, then switch the value of headless to ```true```. The bot runs better on headless mode because less resources are being consumed.<br><br>
```messages``` is the list of messages you want to send, you can have one message in there. Otherwise, the more messages you add, the bot will keep choosing a message in a random way to prevent being detected and shadowbanned.<br><br><br>
The bot supports the use of multiple sticky proxies, and only one rotative proxy **for now**. You can use whatever amount of sticky proxies you have in hand, and the bot will know how to rotate over them, meaning if you have 5000 accounts and only 3000 proxies, the bot will use the 3000 proxies for the first 3000 accounts, then re-use the first 2000 proxies for the remaining accounts.<br>
This is the ```rsrc/proxies.json``` that ships with the bot:<br>
```
{
    "sticky":[

    ],
    "rotative":[
        
    ]
}
```
It's empty because the bot by default uses no proxies. If you want to add a list of sticky proxies, you can add them like this:<br>
```
{
    "sticky":[
        "host1:port1:user1:password1",
        "host2:port2:user2:password2",
        "host3:port3:user3:password3"
    ],
    "rotative":[
        
    ]
}
```
in that specific order. If you wish to add a rotative proxy, you can do it like this:<br>
```
{
    "sticky":[

    ],
    "rotative":[
        "host:port:user:password"
    ]
}
```
I personally recommend using a rotative proxy because it has the ability to rotate its IP multiple times.
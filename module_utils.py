from modules import *
import json
from csv import DictReader, DictWriter, reader, writer

class Modules:
    """
        Modules class, this class holds all the non-main functions the program needs for better functionality.
    """

    Format = {
        'GREEN':'\033[92m',
        'YELLOW':'\033[93m',
        'RED':'\033[91m',
        'END':'\033[0m'
    }

    @staticmethod
    def log(index: int, data: str) -> None:
        """
            Logging system. Not necessary, but good and useful.
        """
        
        # managing different inputs to output them in different colors
        if(index == -1): # neutral input, no color
            print(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}')
        elif(index == 0): # success input, green
            print(f'{Modules.Format["GREEN"]}[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}{Modules.Format["END"]}')
        elif(index == 1): # error input, yellow
            print(f'{Modules.Format["YELLOW"]}[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}{Modules.Format["END"]}')
        elif(index == 2): # fatal error input, red
            print(f'{Modules.Format["RED"]}[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}{Modules.Format["END"]}')

        with open('logs/log', 'a') as log:
            log.write(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}\n')

    @staticmethod
    def dbToList(database: str, list_usernames: list) -> None: # to get all usernames from usernames.csv into list_usernames
        """
            retrieving data from a CSV database
        """
        with open(database, 'r') as usernames:
            dbReader = reader(usernames, delimiter=',')
            for row in dbReader:
                list_usernames.append(
                    str(row[0])
                )

    @staticmethod
    def writeToCSV(database: str, data: list) -> None:
        """
            saving data to a CSV database
        """
        with open(database, 'a', newline='', encoding='utf-8') as db:
            _writer = writer(db)
            _writer.writerow(
                data
            )

    @staticmethod
    def manageProxyExtension(index: int, proxy_backend_path: str, proxy: str) -> None:
        """
            this function is responsible for adding and removing proxy from rsrc/extensions/proxy
            this is a really important function that would enable the software to rotate between proxies
        """
        try:

            if(index == 0): # removing proxy

                proxyList, proxy_backend = proxy.split(':'), str()
                host, port, username, password = proxyList[0], proxyList[1], proxyList[2], proxyList[3]
                with open(proxy_backend_path, 'r') as proxy_backend_js:
                    proxy_backend = proxy_backend_js.read()
                proxy_backend = proxy_backend.replace(host, '_host').replace(port, '_port').replace(username, '_username').replace(password, '_password')
                with open(proxy_backend_path, 'w') as proxy_backend_js:
                    proxy_backend_js.write(proxy_backend)
                Modules.log(0, f'[RedditDMBot] - Proxy {proxy} was removed successfully.')

            elif(index == 1): # adding proxy

                proxyList, proxy_backend = proxy.split(':'), str()
                host, port, username, password = proxyList[0], proxyList[1], proxyList[2], proxyList[3]
                with open(proxy_backend_path, 'r') as proxy_backend_js:
                    proxy_backend = proxy_backend_js.read()
                proxy_backend = proxy_backend.replace('_host', host).replace('_port', port).replace('_username', username).replace('_password', password)
                with open(proxy_backend_path, 'w') as proxy_backend_js:
                    proxy_backend_js.write(proxy_backend)
                Modules.log(0, f'[RedditDMBot] - Proxy {proxy} was removed successfully.')

        except:

            #import traceback
            # logging out the error
            #Modules.log(2, traceback.format_exc())
            Modules.log(2, '[RedditDMBot] - Fatal error while trying to setup Proxy extension.')


    # getting necessary data: configuration, Reddit account(s), locators of Reddit pages, necessary links, and more for the program to function

    @staticmethod
    def getAccounts() -> list:
        with open('rdt/accounts.json','r') as accounts:
            return load(accounts)

    @staticmethod
    def getProxies() -> list:
        with open('rsrc/proxies.json','r') as proxies:
            return load(proxies)

    @staticmethod
    def getPaths() -> dict: # managing relative paths in case this program needs to run on multiple computers with different paths to resources
        with open('rsrc/paths.json','r') as config:
            return load(config)

    @staticmethod
    def getConfig() -> dict:
        with open('rsrc/config.json','r') as config:
            return load(config)

    @staticmethod
    def getLocators() -> dict:
        with open('rsrc/locators.json','r') as locators:
            return load(locators)

    @staticmethod
    def getLinks() -> dict:
        with open('rsrc/links.json','r') as links:
            return load(links)

    # getting JavaScript code to execute inside CD
    @staticmethod
    def getJS(path) -> str:
        with open(path, 'r') as JS:
            return str(JS.read())

    # getting a list of the most common user agents to use
    @staticmethod
    def getUserAgents() -> list:
        with open('rsrc/user_agents.json','r') as user_agents:
            return load(user_agents)
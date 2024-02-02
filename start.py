from modules import *








global driver

# Initializing components
config, links, xpath = getConfig(), getLinks(), getXpath()
list_usernames, usernames_sent = list(), list()
#




def driverInit(): # Initializing driver instance
    options = uc.ChromeOptions()
    isHeadless(options, config['headless'])
    driver = uc.Chrome(options = options)
    driver.maximize_window()
    return driver


def isHeadless(options, headless): # Should the bot run in headless mode or not?
    if(not headless):
        log(f'[Main] The application will not run in headless mode. Starting...')
    else:
        log(f'[Main] The application will run in headless mode. Starting...')
        options.add_argument('--headless')


# def getAccount(accounts):
#     account = accounts[0]
#     accounts.remove(account)
#     return account


def loginRedditAccount(account, driver): # login to your Reddit bot
    try:
        driver.get(links['REDDIT_LOGIN_PAGE_URL'])
        log(f'[Main] Logging in to Reddit account {account["username"]}:{account["password"]}')
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, xpath['REDDIT_LOGIN_PAGE']['usernameInput']))).send_keys(account['username'])
        sleep(uniform(0.5, 1))
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, xpath['REDDIT_LOGIN_PAGE']['passwordInput']))).send_keys(account['password'])
        sleep(uniform(0.5, 1))
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, xpath['REDDIT_LOGIN_PAGE']['loginButton']))).click()
        sleep(uniform(1, 2))
        log(f'[Main] Successfuly logged in to Reddit account {account["username"]}:{account["password"]}')
        return
    except:
        log(f'[Main] ERROR! An exception occured while trying to login to Reddit account {account["username"]}:{account["password"]}. Retrying..')
        sleep(uniform(2, 3))
        return loginRedditAccount(account, driver)


def dbToList(): # to get all usernames from usernames.csv into list_usernames
    with open('./db/usernames.csv', 'r') as usernames:
        dbReader = reader(usernames, delimiter=',')
        for row in dbReader:
            list_usernames.append(
                str(row[0])
            )


def sendMessage(username,driver): # to send message
    #log(f'[Main] Sending messages to {len(list_usernames)} users')
    sent2 = open('./db/usernames_sent.csv', 'a', newline='', encoding='utf-8')
    _writer = writer(sent2) # added writer object before for loop for better efficiency
    try: # to handle exceptions
        #if username not in usernames_sent: # checking if the user was already DMed
        driver.get(f'{links["MESSAGE_URL"]}/{username}') # navigating directly to the chat room!
        # !! JavaScript handles sending messages.
        sleep(config['cooldown'])
        try: # to handle exceptions
            driver.execute_script(TYPE_CHAT_MESSAGE_JS.replace('pythonisthebestprogramminglanguageever!', choice(config['messages'])))
            sleep(uniform(0.5, 1))
            driver.execute_script(ENABLE_CHAT_MESSAGE_JS)
            sleep(uniform(0.5, 1))
            driver.execute_script(CLICK_CHAT_MESSAGE_JS)
            log(f'[Main] Message sent to {username}')
            usernames_sent.append(username)
            _writer.writerow( # saving this user to the list of users that were DMed
                [
                    username
                ]
            )
        except: # an exception might occur here, if it does, it means that there are already sent messages. The bot simply send the message again, if you don't want it to, remove all the code and write pass
            driver.execute_script(TYPE_ROOM_MESSAGE_JS.replace('pythonisthebestprogramminglanguageever!', choice(config['messages'])))
            sleep(uniform(0.5, 1))
            driver.execute_script(ENABLE_ROOM_MESSAGE_JS)
            sleep(uniform(0.5, 1))
            driver.execute_script(CLICK_ROOM_MESSAGE_JS)
            log(f'[Main] Message sent to {username}')
            usernames_sent.append(username)
            _writer.writerow( # saving this user to the list of users that were DMed
                [
                    username
                ]
            )
        #else:
        #    log(f'[Main] Message already sent to {username}.')
    except:
        log(f'[Main] ERROR! An exception occured. Retrying...')
        sleep(uniform(2, 3))
        sendMessage(username, driver)






def main():
    dbToList()
    accounts, used_accounts = getAccounts(), list()
    while(len(list_usernames) != 0): # while there are usernames to send DM to
        username = choice(list_usernames) # getting a random username from the list of usernames to DM
        if(len(accounts) == 0): # to check if all accounts are used
            accounts, used_accounts = used_accounts, list() # repopulates accounts with used_accounts and reinitialize used_accounts to an empty list
        account = accounts.pop(0) # getting the first account of the list accounts, then removing it
        driver = driverInit() # initializing the web driver
        loginRedditAccount(account, driver) # logs into the random account chosen
        sendMessage(username, driver) # sends a message to a random username
        list_usernames.remove(username) # removing that username from the list of usernames to DM
        writeToCSV(username) # adding the user that was DMed to the database of usernames that received DMs
        used_accounts.append(account) # appending the account used to DM to the list of used accounts









if __name__ == '__main__':
    main()

from modules import *








global _
global driver
_ = {
    'user':account['user'],
    'pass':account['pass']
}


options = uc.ChromeOptions()
#options.add_argument('--headless') # to run the bot in headless mode | meaning no GUI(Graphical User Interface). Remove first # to enable it




def isHeadless(iH):
    #global isHeadless
    #log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - Would you like this application to run in headless mode? enter 1 for yes and 0 for no.')
    #iH = int(input('\n--> '))
    if(iH == 1):
        log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] The application will run in headless mode.')
        #options.headless = True # same thing as below code
        options.add_argument('--headless')
    elif(iH == 0):
        log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] The application will not run in headless mode.')
    else:
        #iH = int(input(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - Headless requires a value of either 1 or 0, enter 1 if you want to run in headless mode and 0 if you want to run in normal mode.\n--> '))
        log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] It is necessary to provide a value of either 1 or 0 for the application to continue. Enter 1 to run in normal mode and 0 to run in headless mode.')
        try:
            iH = int(input('\n--> '))
        except:
            iH = -1
        isHeadless(iH)


def loginRedditAccount(account,driver): # login to your Reddit bot
    try:
        driver.get(REDDIT_LOGIN_PAGE_URL)
        log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Logging in to Reddit account {account["username"]}:{account["password"]}')
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_LOGIN_PAGE['usernameInput']))).send_keys(account['username'])
        sleep(uniform(0.5,1))
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_LOGIN_PAGE['passwordInput']))).send_keys(account['password'])
        sleep(uniform(0.5,1))
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_LOGIN_PAGE['loginButton']))).click()
        sleep(uniform(1,2))
        log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Successfuly logged in to Reddit account {account["username"]}:{account["password"]}')
        return 0
    except:
        log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] ERROR! An exception occured. Retrying..')
        sleep(uniform(2,3))
        return loginRedditAccount(account)


def db2list(): # to get all usernames from usernames.csv into list_usernames
    with open('usernames.csv', 'r') as usernames:
        dbReader = csv.reader(usernames, delimiter=',')
        for row in dbReader:
            list_usernames.append(
                str(row[0])
            )


def sendMessage(driver): # to send message
    log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Sending messages to {len(list_usernames)}')
    try: # to handle exceptions
        for username in list_usernames:
            if username not in usernames_sent:
                #log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Sending message to {username}')
                driver.get(MESSAGE_URL)
                WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_CHAT_PAGE['usernameInput']))).send_keys(username)
                sleep(uniform(0.5,1.5))
                WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_CHAT_PAGE['firstResult']))).click()
                sleep(uniform(0.5,1.5))
                WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_CHAT_PAGE['startChatButton']))).click()
                sleep(uniform(0.5,1.5))
                WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_CHAT_PAGE['messageInput']))).send_keys(message)
                sleep(uniform(0.5,1.5))
                WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_CHAT_PAGE['sendButton']))).click()
                log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Message sent to {username}')
                usernames_sent.append(username)
            else:
                log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Message already sent to {username}.')
    except:
        log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] ERROR! An exception occured. Retrying...')
        sleep(uniform(2,3))
        sendMessage(driver)





def main():
    db2list()
    log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Would you like this application to run in headless mode? enter 1 for yes and 0 for no.')
    try:
        iH = int(input('\n--> '))
        isHeadless(iH)
    except:
        isHeadless(-1)
    log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Starting...')
    sleep(uniform(0.5,1))
    driver = uc.Chrome( # declaring WebDriver
        options=options
        )
    loginRedditAccount(_,driver)
    sendMessage(driver)









if __name__ == '__main__':
    main()

from modules import *








global _
global driver
_ = {
    'username':account['user'],
    'password':account['pass']
}


options = uc.ChromeOptions()




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
    with open('./db/usernames.csv','r') as usernames:
        dbReader = csv.reader(usernames,delimiter=',')
        for row in dbReader:
            list_usernames.append(
                str(row[0])
            )
    # with open('./db/usernames_sent.csv','r') as us:
    #     dbReader = csv.reader(us,delimiter=',')
    #     for row in dbReader:
    #         usernames_sent.append(
    #             str(row[0])
    #         )


def sendMessage(driver): # to send message
    log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Sending messages to {len(list_usernames)} users')
    sent2 = open('./db/usernames_sent.csv','a',newline='',encoding='utf-8')
    writer = csv.writer(sent2)
    try: # to handle exceptions
        for username in list_usernames:
            if username not in usernames_sent:
                #log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Sending message to {username}')
                driver.get(f'{MESSAGE_URL}/{username}')
                sleep(20) # waiting for DOM to load and to prevent spam # feel free to change the amount of waiting seconds to suit your needs.
                # !! JavaScript handles sending messages.
                try:
                    driver.execute_script(TYPE_CHAT_MESSAGE_JS.replace('pythonisthebestprogramminglanguageever!', message))
                    sleep(uniform(0.5,1))
                    driver.execute_script(ENABLE_CHAT_MESSAGE_JS)
                    sleep(uniform(0.5,1))
                    driver.execute_script(CLICK_CHAT_MESSAGE_JS)
                    log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Message sent to {username}')
                    usernames_sent.append(username)
                    writer.writerow(
                        [username]
                    )
                except: # an exception might occur here, if it does, it means that there are already sent messages. The bot simply send the message again, if you don't want it to, remove all the code and write pass
                    driver.execute_script(TYPE_ROOM_MESSAGE_JS.replace('pythonisthebestprogramminglanguageever!', message))
                    sleep(uniform(0.5,1))
                    driver.execute_script(ENABLE_ROOM_MESSAGE_JS)
                    sleep(uniform(0.5,1))
                    driver.execute_script(CLICK_ROOM_MESSAGE_JS)
                    log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Message sent to {username}')
                    usernames_sent.append(username)
                    writer.writerow(
                        [username]
                    )
            else:
                log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] Message already sent to {username}.')
            if(len(usernames_sent) % 20 == 0):
                log(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - [Main] 20 messages has been sent since the last pause, pausing for a minute to catch my breath...I don\'t want to be banned :p')
                sleep(60)
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

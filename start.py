from modules import *








global _
global driver
_ = {
    'username':account['user'],
    'password':account['pass']
}


options = uc.ChromeOptions()




def isHeadless(headless):
    if(not headless):
        log(f'[Main] The application will not run in headless mode. Starting...')
    else:
        log(f'[Main] The application will run in headless mode. Starting...')
        options.add_argument('--headless')


def loginRedditAccount(account,driver): # login to your Reddit bot
    try:
        driver.get(REDDIT_LOGIN_PAGE_URL)
        log(f'[Main] Logging in to Reddit account {account["username"]}:{account["password"]}')
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_LOGIN_PAGE['usernameInput']))).send_keys(account['username'])
        sleep(uniform(0.5,1))
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_LOGIN_PAGE['passwordInput']))).send_keys(account['password'])
        sleep(uniform(0.5,1))
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,REDDIT_LOGIN_PAGE['loginButton']))).click()
        sleep(uniform(1,2))
        log(f'[Main] Successfuly logged in to Reddit account {account["username"]}:{account["password"]}')
        return 0
    except:
        log(f'[Main] ERROR! An exception occured. Retrying..')
        sleep(uniform(2,3))
        return loginRedditAccount(account)


def db2list(): # to get all usernames from usernames.csv into list_usernames
    with open('./db/usernames.csv','r') as usernames:
        dbReader = csv.reader(usernames,delimiter=',')
        for row in dbReader:
            list_usernames.append(
                str(row[0])
            )


def sendMessage(driver): # to send message
    log(f'[Main] Sending messages to {len(list_usernames)} users')
    sent2 = open('./db/usernames_sent.csv','a',newline='',encoding='utf-8')
    writer = csv.writer(sent2)
    try: # to handle exceptions
        for username in list_usernames:
            if username not in usernames_sent:
                driver.get(f'{MESSAGE_URL}/{username}')
                sleep(cooldown)
                # !! JavaScript handles sending messages.
                try:
                    driver.execute_script(TYPE_CHAT_MESSAGE_JS.replace('pythonisthebestprogramminglanguageever!', choice(messages)))
                    sleep(uniform(0.5,1))
                    driver.execute_script(ENABLE_CHAT_MESSAGE_JS)
                    sleep(uniform(0.5,1))
                    driver.execute_script(CLICK_CHAT_MESSAGE_JS)
                    log(f'[Main] Message sent to {username}')
                    usernames_sent.append(username)
                    writer.writerow(
                        [username]
                    )
                except: # an exception might occur here, if it does, it means that there are already sent messages. The bot simply send the message again, if you don't want it to, remove all the code and write pass
                    driver.execute_script(TYPE_ROOM_MESSAGE_JS.replace('pythonisthebestprogramminglanguageever!', choice(messages)))
                    sleep(uniform(0.5,1))
                    driver.execute_script(ENABLE_ROOM_MESSAGE_JS)
                    sleep(uniform(0.5,1))
                    driver.execute_script(CLICK_ROOM_MESSAGE_JS)
                    log(f'[Main] Message sent to {username}')
                    usernames_sent.append(username)
                    writer.writerow(
                        [username]
                    )
            else:
                log(f'[Main] Message already sent to {username}.')
    except:
        log(f'[Main] ERROR! An exception occured. Retrying...')
        sleep(uniform(2,3))
        sendMessage(driver)





def main():
    db2list()
    isHeadless(headless)
    sleep(uniform(0.5,1))
    driver = uc.Chrome( # declaring WebDriver
        options=options
        )
    loginRedditAccount(_,driver)
    sendMessage(driver)









if __name__ == '__main__':
    main()

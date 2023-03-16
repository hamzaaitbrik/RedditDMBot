import time
import requests
import json
import random
import pyautogui

from seleniumwire import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions



account_infos = {
    'username':'', # Reddit account username
    'password':'' # Reddit account password
}

# Driver init
reddit_login = r'https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fuser%2F' + account_infos['username']
reddit_message_raw_link = r'https://www.reddit.com/chat/channel/create'
driver = webdriver.Chrome('/home/hamza/chromedriver') # here goes the path where chrome driver is found
driver.proxy = {
    'http': 'http://proxy33:bf87203f77852664375ae582@154.52.36.33:3128' # comment this section if you don't want to use a proxy
}
driver.delete_all_cookies()

#driver.get('https://whoer.net') # to check that the proxy is working
#time.sleep(20)
driver.get(reddit_login)

# Variable init
#keyboard = Controller()
message = "Generate Free Reddit Karma at www.redditkarmagenerator.tk" # the message which will be sent
username_field = driver.find_element_by_id('loginUsername')
password_field = driver.find_element_by_id('loginPassword')
usernames = [] # leave empty
usernames_sent = [] # leave empty
keywords = [] # in this list goes the keywords which the API will look for in recent made comments
scrape_urls = [] # leave empty
data = [] # leave empty
api_url = r'https://api.pushshift.io/reddit/search/comment/?q='
for keyword in keywords:
    scrape_urls.append(str(api_url + keyword + '&size=100'))



# Functions
def main():
    login()
    get_usernames(scrape_urls)
    time.sleep(5)
    send_message(message, usernames, reddit_message_raw_link)


def login():
    username_field.send_keys(account_infos['username'])
    time.sleep(random.uniform(0.9054, 1.2498))
    password_field.send_keys(account_infos['password'])
    time.sleep(random.uniform(0.8452, 1.6254))
    login_button = driver.find_element_by_class_name('AnimatedForm__submitButton')
    login_button.click()
    time.sleep(random.uniform(0.0524, 1.2487))

def get_usernames(scrape_urls):
    for scrape_url in scrape_urls:
        response = requests.get(scrape_url)
        data.append(json.loads(response.content.decode()))
    for dict in data:
        for i in range((len(keywords) * 100) - (len(keywords) - 1)):
            #print(i)
            #print(dict['data'][i]['author'])
            if(dict['data'][i]['author'] not in usernames and dict['data'][i]['author'] != 'AutoModerator'):
                usernames.append(dict['data'][i]['author'])
                print(f'length is: {len(usernames)}')
    print(f'Sending messages to {len(usernames)} users...')

def send_message(message, usernames, reddit_message_raw_link):
    for username in usernames:
        if username not in usernames_sent:
            time.sleep(random.uniform(25,50))
            driver.get(reddit_message_raw_link)
            time.sleep(random.uniform(25,50))
            driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div/form/div/div/div[2]/div[1]/span/input').send_keys(username)
            time.sleep(random.uniform(5,10))
            driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div/form/div/div/div[2]/div[2]/div/label/span/span[1]/div/div/div').click()
            time.sleep(random.uniform(5,10))
            driver.find_element_by_xpath('/html/body/div[1]/div/main/form/div/div[2]/div/button[2]').click()
            time.sleep(random.uniform(5,10))
            driver.find_element_by_xpath('').send_keys(message)
            time.sleep(random.uniform(1,5))
            #pyautogui.press('enter')
            driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/form/div/button').click()
            usernames_sent.append(username)
            usernames.remove(username)
    get_usernames(scrape_urls)
    send_message(message, usernames)



if(__name__ == '__main__'):
    main()

#from pynput import keyboard
from typing import final
#import selenium
#import praw
import time
#import urllib.request
import requests
import json
import random
#import pyautogui

from seleniumwire import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from pynput.keyboard import Key, Controller

# Proxy init
#proxy = Proxy()
#proxy.http_proxy = "ip:port"
#proxy.socks_proxy = "ip:port"
# options = {
#    'proxy':{
#        'http': 'http://user:pass@ip:port',
#        'https': 'https://user:pass@ip:port',
#        'no_proxy': 'localhost,127.0.0.1'
#    }
#}

account_infos = {
    'username':'', # Reddit account username
    'password':'' # Reddit account password
}

# Driver init
reddit_login = r'https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fuser%2F' + account_infos['username']
driver = webdriver.Chrome('') # here goes the path where chrome driver is found
driver.proxy = {
    'http': 'http://user:pass@ip:port' # comment this section if you don't want to use a proxy
}
driver.delete_all_cookies()

#driver.get('https://whoer.net') # to check that the proxy is working
#time.sleep(20)
driver.get(reddit_login)

# Variable init
#keyboard = Controller()
message = 'Hello' # the message which will be sent
username_field = driver.find_element_by_id('loginUsername')
password_field = driver.find_element_by_id('loginPassword')
usernames = [] # leave empty
usernames_sent = [] # leave empty
keywords = [] # in this list goes the keywords which the API will look for in recent made comments
scrape_urls = [] # leave empty
data = [] # leave empty
api_url = r'https://api.pushshift.io/reddit/search/comment/?q='
for keyword in keywords:
    scrape_urls.append(str(api_url + keyword + '&size=100')) # 100 is the max data the api returns

# Functions
def main():
    login()
    get_usernames(scrape_urls)
    time.sleep(5)
    send_message(message, usernames)


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
        for i in range(100):
            #print(dict['data'][i]['author'])
            if(dict['data'][i]['author'] not in usernames and dict['data'][i]['author'] != 'AutoModerator'):
                usernames.append(dict['data'][i]['author'])

def send_message(message, usernames):
    time.sleep(random.randint(25, 50))
    for username in usernames:
        if username not in usernames_sent: # to prevent sending multiple messages to the same user
            user_url = 'https://reddit.com/u/' + username
            driver.get(user_url)
            time.sleep(random.uniform(25, 50))
            try:
                driver.find_element_by_xpath("//span[contains(text(), 'Chat')]").find_element_by_xpath('..').click() # looks for the 'Chat' button
            except:
                usernames.remove(username) # removes the user with no 'Chat' button
                send_message(message, usernames) # recalls the function send_message()
            #try:
            #    driver.find_element_by_xpath("//button[contains(text(), 'New Chat')]").find_element_by_xpath('..').click()
            #except:
            #    driver.find_element_by_xpath("//span[contains(text(), 'Chat')]").find_element_by_xpath('..').click()
            #    pass
            #driver.find_element_by_xpath("//button[contains(text(), 'New Chat')]").find_element_by_xpath('..').click()
            time.sleep(random.uniform(11,24))
            #textarea = driver.find_element_by_xpath("/html/body/div[4]/div/div/main/div[1]/div[2]/div/form/div/div")
            #textarea.send_keys('Hello world!')
            #pyautogui.click(x = random.randint(640, 890), y = random.randint(670, 690))
            #time.sleep(random.uniform(70, 150))
            driver.find_element_by_xpath('//*[@id="MessageInputTooltip--Container"]/div/div/textarea').send_keys(message)
            time.sleep(random.uniform(0.1, 2))
            #pyautogui.click(x = random.randint(965, 980), y = random.randint(676, 692))
            driver.find_element_by_xpath('//*[@id="MessageInputTooltip--Container"]/div/button').click()
            usernames_sent.append(username)
            usernames.remove(username)
    get_usernames(scrape_urls)
    send_message(message, usernames)



if(__name__ == '__main__'):
    main()
# from src.xpath import *
# from src.constants import *
# from src.config import *
# from rdt.account import account
from csv import reader, writer
import requests
from json import load
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from time import sleep
from random import uniform,randint,choice




def log(data):
        print(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}')
        with open('log', 'a') as log:
            log.write(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}\n')

def checkExistByXPATH(driver,xpath):
    try:
        #sleep(uniform(3.5,5))
        #WebDriverWait(driver,5).until(EC.presence_of_element_located((By>
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:# or TimeoutException:
        return False
    return True

def getAccounts():
    with open('rdt/accounts.json','r') as accounts:
        return load(accounts)

def getConfig():
    with open('rsrc/config.json','r') as config:
        return load(config)

def getXpath():
    with open('rsrc/xpath.json','r') as xpath:
        return load(xpath)

def getLinks():
    with open('rsrc/links.json','r') as links:
        return load(links)

with open('./rsrc/js/chat_message.type.js','r') as type_chat_message:
    TYPE_CHAT_MESSAGE_JS = type_chat_message.read()
with open('./rsrc/js/chat_message.enable.js','r') as enable_chat_message:
    ENABLE_CHAT_MESSAGE_JS = enable_chat_message.read()
with open('./rsrc/js/chat_message.click.js','r') as click_chat_message:
    CLICK_CHAT_MESSAGE_JS = click_chat_message.read()
with open('./rsrc/js/room_message.type.js','r') as type_room_message:
    TYPE_ROOM_MESSAGE_JS = type_room_message.read()
with open('./rsrc/js/room_message.enable.js','r') as enable_room_message:
    ENABLE_ROOM_MESSAGE_JS = enable_room_message.read()
with open('./rsrc/js/room_message.click.js','r') as click_room_message:
    CLICK_ROOM_MESSAGE_JS = click_room_message.read()

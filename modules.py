from requests import get
from csv import reader, writer
from json import load
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from datetime import datetime
from time import sleep
from random import uniform,randint,choice




def log(data):
        print(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}')
        with open('log', 'a') as log:
            log.write(f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}] - {data}\n')

def dbToList(list_usernames): # to get all usernames from usernames.csv into list_usernames
    with open('./db/usernames.csv', 'r') as usernames:
        dbReader = reader(usernames, delimiter=',')
        for row in dbReader:
            list_usernames.append(
                str(row[0])
            )

def writeToCSV(database,data):
    with open(database, 'a', newline='', encoding='utf-8') as db:
        _writer = writer(db)
        _writer.writerow(
            [
                data[0],
                data[1]
            ]
        )

def getAccounts():
    with open('rdt/accounts.json','r') as accounts:
        return load(accounts)

def getConfig():
    with open('rsrc/config.json','r') as config:
        return load(config)

def getLocators():
    with open('rsrc/locators.json','r') as xpath:
        return load(xpath)

def getLinks():
    with open('rsrc/links.json','r') as links:
        return load(links)
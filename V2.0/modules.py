from XPATH import *
from CONSTANTS import *
from variables import *
from account import account
import csv
import requests
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
from random import uniform,randint




def log(data):
        print(data)
        with open('log.txt', 'a') as log:
            log.write(f'{data}\n')

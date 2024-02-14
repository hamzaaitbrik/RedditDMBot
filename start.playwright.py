from requests import get
from csv import reader, writer
import requests
from json import load
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from datetime import datetime
from time import sleep
from random import uniform,randint,choice


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
# Initializing components
config, links, xpath = getConfig(), getLinks(), getXpath()
list_usernames, usernames_sent = list(), list()
#




async def main():
    async with async_playwright() as playwright:
        device = playwright.devices['Desktop Chrome']
        browser = await playwright.chromium.launch()
        context = await browser.new_context(**device)
        page = await context.new_page()
        await stealth_async(page)
        try:
            await page.goto('https://reddit.com/login')
            await page.wait_for_load_state('networkidle')
            await page.locator('#loginUsername').fill('EastAd6908')
            await page.locator("#loginPassword").fill('HtUsEuZL6vrQPul')
            await page.locator('body > div > main > div.OnboardingStep.Onboarding__step.mode-auth > div > div.Step__content > form > fieldset:nth-child(8) > button').click()
            await page.wait_for_load_state('load')
            sleep(2)
            await page.goto('https://chat.reddit.com/user/t2_6q3yyhiy6')
            #await page.wait_for_load_state('networkidle')
            await page.wait_for_selector('body > faceplate-app')
            # await page.wait_until('body')
            sleep(5)
            await page.locator('body > faceplate-app > rs-app div.container > rs-direct-chat section > rs-message-composer form > div > textarea').fill('Hello world')
            # await page.evaluate(
            #     '() => document.querySelector("body > faceplate-app > rs-app").shadowRoot.querySelector("div.container > rs-direct-chat").shadowRoot.querySelector("section > rs-message-composer").shadowRoot.querySelector("form > div > textarea").value = "Hello!"'
            # )
            await page.locator('body > faceplate-app > rs-app div.container > rs-direct-chat section > rs-message-composer form > button.button-send.button-medium.px-\\[length\\:var\\(--rem8\\)\\].button-plain.icon.button.inline-flex.items-center.justify-center').click()
            #await page.locator()
            sleep(3)
            await page.screenshot(path="playwright.png")
        except:
            pass
        finally:
            await browser.close()


asyncio.run(main())
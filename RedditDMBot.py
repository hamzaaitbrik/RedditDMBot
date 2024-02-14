from modules import *



# Initializing components
config, links, locators = getConfig(), getLinks(), getLocators()
list_usernames, usernames_sent = list(), list()
#




async def RedditDMBot(account,username):
    async with async_playwright() as playwright:
        device = playwright.devices['Desktop Chrome']
        browser = await playwright.chromium.launch()
        context = await browser.new_context(**device)
        page = await context.new_page()
        await stealth_async(page)
        try:
            await page.goto(links['REDDIT_LOGIN_PAGE_URL'])
            await page.wait_for_load_state('networkidle')
            await page.locator(locators['usernameLocator']).fill(account['username'])
            await page.locator(locators['passwordLocator']).fill(account['password'])
            await page.locator(locators['loginButtonLocator']).click()
            await page.wait_for_load_state('load')
            sleep(uniform(1,2))
            await page.goto(f'{links["MESSAGE_URL"]}/{username}')
            sleep(uniform(1,2))
            await page.locator(locators['messageInputLocator']).fill(choice(config['messages']))
            await page.locator(locators['sendButtonLocator']).click()
            log(f'[Main] Message sent to {username} using {account["username"]}:{account["password"]}. Writing it to the database...')
            sleep(config['cooldown'])
        except:
            log(f'[Main] ERROR! An exception occured while trying to DM {username} using {account["username"]}:{account["password"]}.')
            await browser.close()
        finally:
            if(config['proxy']['proxyRotationLink'] != ''):
                log('[Main] Rotating proxy IP...')
                get(config['proxy']['proxyRotationLink'])
                sleep(uniform(15,20))
            await browser.close()


def main():
    dbToList(list_usernames)
    accounts, used_accounts = getAccounts(), list()




asyncio.run(RedditDMBot()) # entry point
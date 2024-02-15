from modules import *



# Initializing components
config, links, paths, locators = getConfig(), getLinks(), getPaths(), getLocators()
list_usernames, usernames_sent = list(), list()
#




async def RedditDMBot(used_accounts,account,username):
    async with async_playwright() as playwright:
        device = playwright.devices['Desktop Chrome']
        if(config['proxy']['proxy'] == 'localhost'):
            browser = await playwright.chromium.launch(
                headless = config['headless']
            )
        else:
            browser = await playwright.chromium.launch(
                headless = config['headless'],
                proxy = {
                    "server":f"{config['proxy']['proxy'].split(':')[0]}:{config['proxy']['proxy'].split(':')[1]}",
                    "username":config['proxy']['proxy'].split(':')[2],
                    "password":config['proxy']['proxy'].split(':')[3]
                }
            )
        context = await browser.new_context(**device)
        page = await context.new_page()
        await stealth_async(page)
        try:
            await page.goto(links['REDDIT_LOGIN_PAGE_URL'])
            await page.wait_for_load_state('networkidle')
            await page.locator(locators['usernameLocator']).fill(account['username'])
            await page.locator(locators['passwordLocator']).fill(account['password'])
            await page.locator(locators['loginButtonLocator']).click()
            sleep(uniform(1.5,2))
            log(f'[Main] Successfuly logged in to Reddit account {account["username"]}:{account["password"]}')
            await page.goto(f'{links["MESSAGE_URL"]}/{username}')
            sleep(config['cooldown'])
            await page.locator(locators['messageInputLocator']).fill(choice(config['messages']))
            await page.locator(locators['sendButtonLocator']).click()
            sleep(uniform(1,2))
            try:
                page.locator(locators['unableToDMLocator'])
                log(f'[Main] {account["username"]} was unable to send DM. Writing it to the database...')
                writeToCSV(
                    paths['toss_accounts'],
                    [
                        account['username'],
                        account['password']
                    ]
                )
                await page.screenshot( path=f"screenshots/failed/{account['username']}_to_{username}#{await page.locator(locators['receiverLocator']).get_attribute('title')}.png" )
            except:
                log(f'[Main] Message sent to {username}#{await page.locator(locators["receiverLocator"]).get_attribute("title")} using {account["username"]}. Writing it to the database...')
                writeToCSV(
                    paths['usernames_sent'],
                    [
                        username,
                        account['username']
                    ]
                )
                await page.screenshot( path=f"screenshots/succeeded/{account['username']}_to_{username}#{await page.locator(locators['receiverLocator']).get_attribute('title')}.png" )
                list_usernames.remove(username) # removing that username from the list of usernames to DM
                used_accounts.append(account) # adding account to the list of used accounts
        except:
            log(f'[Main] ERROR! An exception occured while trying to DM {username}#{page.locator(locators["receiverLocator"]).get_attribute("title")} using {account["username"]}:{account["password"]}.')
            writeToCSV(
                paths['usernames_failed'],
                [
                    username,
                    account['username']
                ]
            )
            if(config['proxy']['proxyRotationLink'] != ''):
                log('[Main] Rotating proxy IP...')
                get(config['proxy']['proxyRotationLink'])
                sleep(config['proxy']['proxyRotationCooldown'])
            await browser.close()
        finally:
            if(config['proxy']['proxyRotationLink'] != ''):
                log('[Main] Rotating proxy IP...')
                get(config['proxy']['proxyRotationLink'])
                sleep(config['proxy']['proxyRotationCooldown'])
            await browser.close()


def main():
    dbToList(paths['usernames'],list_usernames)
    accounts, used_accounts = getAccounts(), list()
    while(len(list_usernames) != 0): # while there are usernames to send DM to
        username = choice(list_usernames) # getting a random username from the list of usernames to DM
        if(len(accounts) == 0): # to check if all accounts are used
            accounts, used_accounts = used_accounts, list() # repopulates accounts with used_accounts and reinitialize used_accounts to an empty list
        account = accounts.pop(0) # getting the first account of the list accounts, then removing it
        asyncio.run(RedditDMBot(used_accounts,account,username)) # entry point




if __name__ == '__main__':
    main()
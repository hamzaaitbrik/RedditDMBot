from modules import *



# Initializing components
config, links, xpath = getConfig(), getLinks(), getXpath()
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
            await page.locator('#loginUsername').fill(account['username'])
            await page.locator("#loginPassword").fill(account['password'])
            await page.locator('body > div > main > div.OnboardingStep.Onboarding__step.mode-auth > div > div.Step__content > form > fieldset:nth-child(8) > button').click()
            await page.wait_for_load_state('load')
            sleep(uniform(1,2))
            await page.goto(f'{links["MESSAGE_URL"]}/{username}')
            sleep(5)
            await page.locator('body > faceplate-app > rs-app div.container > rs-direct-chat section > rs-message-composer form > div > textarea').fill('Hello world')
            await page.locator('body > faceplate-app > rs-app div.container > rs-direct-chat section > rs-message-composer form > button.button-send.button-medium.px-\\[length\\:var\\(--rem8\\)\\].button-plain.icon.button.inline-flex.items-center.justify-center').click()
            #await page.locator()
            sleep(3)
            await page.screenshot(path="playwright.png")
        except:
            pass
        finally:
            await browser.close()


asyncio.run(main())
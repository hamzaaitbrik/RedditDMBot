from modules import *
from module_utils import Modules
from harvester import poll_subreddit_new
from message_composer import compose_dm_message_openai_lib
# Initializing components
list_usernames, usernames_sent = list(), list()


async def RedditDMBot(
        config: dict,
        links: dict,
        paths: dict,
        locators: dict,
        proxy: str,
        list_usernames: list,
        used_accounts: list,
        toss_accounts: list,
        account: dict,
        target: str,
        usernames_sent: list,
        personalized_message: str,
        post_url: str
) -> None:
    """
        main function responsible for sending a DM
    """
    browser, instance = None, None # Initialize here
    try:
        # initializing a config instance for the browser
        browser_config = zendriver.Config(
            browser_args = config['browser_args']
        )

        # headless or headfull?
        browser_config.headless = config['headless']

        # Add --no-sandbox argument
        if '--no-sandbox' not in browser_config.browser_args:
            browser_config.browser_args.append('--no-sandbox')


        # adding arguments to the configuration to initiate the browser with
        #browser_config.browser_args = config['browser_args']

        # changing proxy configuration to add to the browser
        if(proxy != 'localhost'): # in case there are proxies for the software to use

            Modules.manageProxyExtension(
                index = 1,
                proxy_backend_path = paths['proxy']['proxy_backend_path'],
                proxy = proxy
            )
            try:
                ip = loads(
                        get(
                            links['GET_CONNECTION_IP'],
                            proxies={
                                'http':f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                "https":f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
                            }
                        ).text
                    )['query']
            except: # in case of an error, the IP is 0
                ip = 0
            
            browser_config.add_extension( # adding proxy extension
                extension_path = paths['proxy']['proxy_extension_path']
            )

        else: # in case no proxy was provided

            try:
                ip = loads(
                    get(
                        links['GET_CONNECTION_IP']
                    ).text
                )['query']
            except: # in case of an error, the IP is 0
                ip = 0

        # initializing a browser of nodriver
        browser = await zendriver.start(
            config = browser_config
        )

        # creating an instance by navigating to Reddit's login page
        instance = await browser.get(links['REDDIT_LOGIN_PAGE_URL'])

        sleep(10)

        try: # logging in to Reddit

            # finding the username input and filling it
            username_input = await instance.find(
                tagname = 'input',
                attrs = {
                    "name":"username"
                },
                timeout = 15
            )
            await username_input.send_keys(account['username'])

            # finding the password input and filling it
            password_input = await instance.find(
                tagname = 'input',
                attrs = {
                    "name":"password"
                },
                timeout = 15
            )
            await password_input.send_keys(account['password'])

            sleep(uniform(0.5,1))

            # finding and clicking the log in button
            login_button = await instance.find(
                tagname = 'button',
                attrs = {
                    'class':'login',
                    'type':'button'
                }
            )
            await login_button.click()

        except TimeoutError: # in case of wrong locators # rare
            import traceback
            print(traceback.format_exc())
            Modules.log(2, f'[RedditDMBot] - An error occured while trying to login to Reddit account {account["username"]}:{account["password"]} via {ip}. Failed to locate one or more elements on Reddit\'s login page.')
            sleep(500)
            return

        except: # in case of other error
            import traceback
            print(traceback.format_exc())
            Modules.log(2, f'[RedditDMBot] - An error occured while trying to login to Reddit account {account["username"]}:{account["password"]} via {ip}.')
            sleep(500)
            return
         
        try:

            await instance.select(locators['logged_in_indicator_locator'], timeout = 10)
            Modules.log(0, f'[RedditDMBot] - Successfully logged in to Reddit account {account["username"]}:{account["password"]} via {ip}.')

        except:
            
            Modules.log(2, f'[RedditDMBot] - Unable to log in into account {account["username"]}:{account["password"]} via {ip}. Exiting.')
            sleep(500)
            return

        sleep(config['cooldown'])

        # sending DM

        # getting the id of our target first
        await instance.get(f'{links["REDDIT_USER_PAGE_URL"]}/{target}')
        reddit_user_data_element = await instance.find(
            tagname = locators['reddit_user_data_locator']
        )
        target_id = loads(reddit_user_data_element.attributes[1])['profile']['id']

        sleep(config['cooldown'])

        # getting the chat page
        await instance.get(f'{links["REDDIT_MESSAGE_PAGE_URL"]}/{target_id}')

        sleep(config['cooldown'])
        
        # writing the message
        message_input = await instance.find(
            tagname = 'textarea',
            attrs = {
                'name':'message',
                'placeholder':'Message'
            }
        )
        await message_input.send_keys(personalized_message) # chosing a random message out of the list of messages

        sleep(uniform(0.5,1.5))

        page_buttons = await instance.find_all(tagname = 'button')
        for button in page_buttons:
            try:
                if button.attrs['aria-label'] == 'Send message':
                    send_message_button = button
            except:
                pass
        
        await send_message_button.click()

        try: # in case the message was not sent

            # searching for the elements responsible for identifying whether the DM was sent or not
            await instance.select(locators['unable_to_DM_locator'], timeout = 3)
            #await instance.find('Wow, you\'ve sent', best_match = True, timeout = 3)

            Modules.log(2, f'[RedditDMBot] - {account["username"]}:{account["password"]} via {ip} was unable to send DM. Writing it to the database...')
            
            # adding the username of the account that was not able to send a DM to a list of accounts to toss
            toss_accounts.append(account['username'])

            # writing the result to the database of accounts to toss
            Modules.writeToCSV(
                paths['toss_accounts'],
                [
                    account['username'],
                    account['password'],
                    ip
                ]
            )

        except: # in case the DM was sent successfully

            Modules.log(0, f'[RedditDMBot] - Message sent successfully to {target} using Reddit account {account["username"]}:{account["password"]} via {ip}. Writing it to the database...')

            # appending the account we used to 
            used_accounts.append(account)

            # removing the user we DMed from the list of usernames
            list_usernames.remove(username)
            usernames_sent.append(username)

            # adding the user we DMed alongside the account we used to DM to db/usernames_sent.csv
            Modules.writeToCSV(
                paths['usernames_sent'],
                [
                    username,
                    account['username']
                ]
            )
            Modules.writeToCSV(
                paths['sent_log'],
                [
                    username,
                    post_url,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            )
        sleep(config['cooldown'])

    except:
        import traceback
        print(traceback.print_exc())
        Modules.log(2, f'[RedditDMBot] - An error occured while trying to DM {target} with Reddit account {account["username"]}:{account["password"]} via {ip}.')

    finally: # finally rotating proxy IP if a rotation link exists

        if(config['proxy']['proxy_type'] == 'rotative'):
            if(config['proxy']['proxy_rotation_link'] != ''):
                Modules.log(-1, '[RedditDMBot] Rotating proxy IP...')
                get(config['proxy']['proxy_rotation_link'])
                sleep(config['proxy']['proxy_rotation_cooldown'])
            else:
                Modules.log(2, '[RedditDMBot] - A proxy rotation link must be provided to rotate the proxy!')
                exit()

        # closing the instance and the browser
        # Check if instance exists before closing
        if instance:
            await instance.close()
        # Check if browser exists before stopping (if uncommented later)
        # if browser:
        #     await browser.stop()

        sleep(config['cooldown'])




if __name__ == '__main__': # software entry point

    config, paths, links, locators = Modules.getConfig(), Modules.getPaths(), Modules.getLinks(), Modules.getLocators()
    proxies_pool = Modules.getProxies()

    # harvest posts from subreddits to add to database 
    # subreddit_posts = poll_subreddit_new(config['target_subreddits'][0])

    Modules.dbToList(paths['usernames'], list_usernames)
    Modules.dbToList(paths['usernames_sent'], usernames_sent)

    accounts, used_accounts, toss_accounts = Modules.getAccounts(), list(), list()

    # LOOP STARTS HERE
    while(True):
        # harvest posts from subreddits and add to database
        posts_per_hour = 3
        len_subreddits = len(config['target_subreddits'])
        Modules.log(0, f"Harvesting {posts_per_hour} total posts per hour from {len_subreddits} subreddits...")

        all_posts = []
        for subreddit in config['target_subreddits']:
            subreddit_posts = poll_subreddit_new(subreddit, posts_per_hour // len_subreddits)
            for post in subreddit_posts:
                all_posts.append(post)

        dm_tasks = []
        # for post in all_posts:
        #     dm_tasks.append({
        #         "username": post['author'],
        #         "message": compose_dm_message_openai_lib(post_data=post),
        #         "post_url": post['url']
        #     })

        # for testing
        dm_tasks = [
            {
                "username": "XpsProGamer",
                "message": "test message",
                "post_url": "https://www.reddit.com/r/testsubreddit/comments/1234567890/testpost/"
            }
        ]

        Modules.log(0, f"Harvested {len(dm_tasks)} DM tasks from {len(all_posts)} posts.")

        message_count = 0

        while(len(dm_tasks) != 0): # while there are DM tasks to send
            task = dm_tasks.pop(0) # getting a random DM task from the list of DM tasks
            username = task['username']
            message = task['message']
            post_url = task['post_url']
            if username in usernames_sent:
                Modules.log(1, f'{username} has already been sent a DM, removing from list...')
                continue

            # choosing an account to send the DM with
            if(len(accounts) == 0): # to check if all accounts are used
                accounts, used_accounts = used_accounts, list() # repopulates accounts with used_accounts and reinitialize used_accounts to an empty list
            try:
                account = accounts.pop(0) # getting the first account of the list accounts, then removing it
            except IndexError: # in case no more accounts are in the accounts list
                Modules.log(1, '[RedditDMBot] There are no more useful accounts to use.')
                break

            # choosing a proxy to use
            if(config['proxy']['proxy_type'] == 'localhost'): proxy = 'localhost'
            elif(config['proxy']['proxy_type'] == 'sticky'):
                try:
                    proxy = proxies_pool['sticky'].pop(0)
                except IndexError:
                    Modules.log(1, '[RedditDMBot] There are no more useful proxies to use.')
                    break
            elif(config['proxy']['proxy_type'] == 'rotative'):
                proxy = proxies_pool['rotative'][0]

            asyncio.run(
                RedditDMBot(
                    config = config,
                    links = links,
                    paths = paths,
                    locators = locators,
                    proxy = proxy,
                    list_usernames = list_usernames,
                    used_accounts = used_accounts,
                    toss_accounts = toss_accounts,
                    account = account,
                    target = username,
                    personalized_message = message,
                    post_url = post_url,
                    usernames_sent = usernames_sent
                )
            ) # entry point
            message_count += 1
        Modules.log(0, f'Loop complete. Total DMs sent: {message_count}. Sleeping for {config["cooldown"]} seconds...')
        sleep(config['cooldown'])

    Modules.log(-1, '[RedditDMBot] - Done.')
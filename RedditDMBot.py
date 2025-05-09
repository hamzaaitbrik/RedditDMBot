from modules import *
from module_utils import Modules
from harvester import poll_subreddit_new
from message_composer import compose_dm_message_openai_lib
import time # Add time import
import random # Add random import
from collections import deque # Use deque for efficient timestamp tracking

# Initializing components
usernames_sent = list()

def escape_newlines(message):
    return message.replace('\n', '\r\n')

async def RedditDMBot(
        config: dict,
        links: dict,
        paths: dict,
        locators: dict,
        proxy: str,
        # list_usernames: list,
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
            # add account back to accounts list
            used_accounts.append(account)
            return

        except: # in case of other error
            import traceback
            print(traceback.format_exc())
            Modules.log(2, f'[RedditDMBot] - An error occured while trying to login to Reddit account {account["username"]}:{account["password"]} via {ip}.')
            sleep(500)
            # add account back to accounts list
            used_accounts.append(account)
            return
         
        try:

            await instance.select(locators['logged_in_indicator_locator'], timeout = 10)
            Modules.log(0, f'[RedditDMBot] - Successfully logged in to Reddit account {account["username"]}:{account["password"]} via {ip}.')

        except:
            
            Modules.log(2, f'[RedditDMBot] - Unable to log in into account {account["username"]}:{account["password"]} via {ip}. Exiting.')
            sleep(500)
            # add account back to accounts list
            used_accounts.append(account)
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
        Modules.log(0, "accessing the chat page")
        await instance.get(f'{links["REDDIT_MESSAGE_PAGE_URL"]}/{target_id}')

        sleep(config['cooldown'])
        
        # writing the message
        Modules.log(0, "writing the message")
        message_input = await instance.find(
            tagname = 'textarea',
            attrs = {
                'name':'message',
                'placeholder':'Message'
            }
        )
        Modules.log(0, f"[RedditDMBot] - Sending message: {personalized_message}")
        await message_input.send_keys(escape_newlines(personalized_message)) # chosing a random message out of the list of messages

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
            usernames_sent.append(target)

            # adding the user we DMed alongside the account we used to DM to db/usernames_sent.csv
            Modules.writeToCSV(
                paths['usernames_sent'],
                [
                    target,
                    account['username']
                ]
            )
            Modules.writeToCSV(
                paths['sent_log_file'],
                [
                    target,
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

    # --- Get Pacing Configuration ---
    # Use .get() with defaults in case keys are missing
    harvest_interval_sec = config.get('HARVEST_INTERVAL_SEC', 30)
    min_dm_gap_sec = config.get('MIN_DM_GAP_SEC', 60)
    jitter_sec = config.get('JITTER_SEC', 15)
    max_dm_per_hour = config.get('MAX_DM_PER_HOUR', 40)

    # Validate jitter to prevent negative sleep times
    if jitter_sec > min_dm_gap_sec:
        Modules.log(1, f"Warning: JITTER_SEC ({jitter_sec}) is greater than MIN_DM_GAP_SEC ({min_dm_gap_sec}). Clamping jitter.")
        jitter_sec = min_dm_gap_sec // 2 # Example clamping

    Modules.log(0, f"Pacing Config: HarvestInterval={harvest_interval_sec}s, MinGap={min_dm_gap_sec}s, Jitter={jitter_sec}s, MaxDM/hr={max_dm_per_hour}")
    # --- End Pacing Configuration ---


    # --- Load Initial Data (outside the main loop) ---
    # Modules.dbToList(paths['usernames'], list_usernames) # Assuming this might still be needed for some legacy check? Or remove if unused.
    # Load the sent log using the correct Modules function
    Modules.dbToList(paths['usernames_sent'], usernames_sent)

    accounts_all = Modules.getAccounts()
    if not accounts_all:
        Modules.log(2, "CRITICAL: No accounts found. Exiting.")
        exit()
    accounts = list(accounts_all) # Create a mutable copy for the loop
    used_accounts, toss_accounts = list(), list()

    # Timestamp tracking for hourly limit (using deque for efficiency)
    dm_timestamps = deque()
    # --- End Initial Data Loading ---

    # LOOP STARTS HERE
    while(True):
        Modules.log(0, "--- Starting Harvest Cycle ---")
        Modules.log(0, f"Harvesting new posts from subreddits: {config.get('target_subreddits', [])}...")

        all_posts = []
        target_subreddits = config.get('target_subreddits', [])
        fetch_limit_scaling_factor = config.get('FETCH_LIMIT_SCALING_FACTOR', 1.5) # Default to 1.5 if not set

        if not target_subreddits:
            Modules.log(1, "No target subreddits defined in config. Skipping harvest.")
            fetch_limit_per_subreddit = 0 # Or some default like 10 if you want to fetch anyway
        else:
            # Calculate fetch limit per subreddit, ensuring it's at least 1
            fetch_limit_per_subreddit = max(1, int((max_dm_per_hour * fetch_limit_scaling_factor) / len(target_subreddits)))
            Modules.log(-1, f"Calculated fetch limit per subreddit: {fetch_limit_per_subreddit} (based on {max_dm_per_hour}/hr, {len(target_subreddits)} subs, factor {fetch_limit_scaling_factor})")

        for subreddit in target_subreddits:
             # Fetch a reasonable number, filtering happens later
            subreddit_posts = poll_subreddit_new(subreddit, limit= fetch_limit_per_subreddit) # Fetch more, filter later
            if subreddit_posts:
                all_posts.extend(subreddit_posts)
            time.sleep(random.uniform(1, 3)) # Small delay between subreddit polls

        if not all_posts:
            Modules.log(1, "No posts found in this harvest cycle.")
            # Go to sleep before next harvest attempt
            Modules.log(0, f"Sleeping for {harvest_interval_sec} seconds before next harvest cycle...")
            time.sleep(harvest_interval_sec)
            continue # Skip to the next iteration of the main `while True` loop


        dm_tasks = []
        Modules.log(0, "Composing messages for harvested posts...")
        composition_attempts = 0
        for post in all_posts:
            if post['author'] in usernames_sent:
                Modules.log(1, f'User {post["author"]} already sent DM previously. Skipping post.')
                continue
            composition_attempts += 1
            Modules.log(-1, f"Attempting composition {composition_attempts}/{len(all_posts)} for post by u/{post.get('author','N/A')}")
            # Pass the necessary config parts to the composer
            # Ensure your config.json has these keys or they are handled by defaults
            openai_config_for_composer = {
                "openaiApiKey": config.get("openaiApiKey"),
                "openaiModel": config.get("openaiModel", "gpt-4o-mini"),
                "messageTemplate": config.get("messageTemplate"),
                "personaRules": config.get("personaRules"),
                "brandBlurb": config.get("brandBlurb"),
                "appLink": config.get("appLink")
            }
            # Filter out None values if message_composer handles defaults safely
            openai_config_for_composer = {k: v for k, v in openai_config_for_composer.items() if v is not None}

            message = compose_dm_message_openai_lib(post_data=post, user_config=openai_config_for_composer)

            if message:
                dm_tasks.append({
                    "username": post['author'],
                    "message": message,
                    "post_url": post['url']
                })
                Modules.log(0, f"Successfully composed message for u/{post['author']}")
            else:
                 Modules.log(1, f"Failed to compose message for u/{post['author']}")
            time.sleep(random.uniform(0.5, 1.5)) # Small delay between OpenAI calls


        Modules.log(0, f"Generated {len(dm_tasks)} DM tasks from {len(all_posts)} harvested posts.")

        # --- DM Sending Loop ---
        message_count_this_cycle = 0
        tasks_processed_this_cycle = 0
        start_time = time.time()

        while dm_tasks and message_count_this_cycle < max_dm_per_hour and time.time() - start_time < 3600: # Process all generated tasks for this cycle
            tasks_processed_this_cycle += 1
            task = dm_tasks.pop(0) # FIFO processing
            username = task['username']
            message = task['message']
            post_url = task['post_url']

            # --- Filtering based on Sent Log ---
            if username in usernames_sent:
                Modules.log(1, f'User {username} already sent DM regarding post {post_url}. Skipping.')
                continue
            # --- End Filtering ---

            # --- Hourly Rate Limit Check ---
            current_time = time.time()
            # Remove timestamps older than an hour (3600 seconds)
            while dm_timestamps and dm_timestamps[0] < current_time - 3600:
                dm_timestamps.popleft()
            # Check if limit is reached
            if len(dm_timestamps) >= max_dm_per_hour:
                time_to_wait = (dm_timestamps[0] + 3600) - current_time
                if time_to_wait > 0:
                    Modules.log(1, f"Hourly DM limit ({max_dm_per_hour}/hr) reached. Sleeping for {time_to_wait:.1f} seconds...")
                    time.sleep(time_to_wait)
                # Re-evaluate after sleeping (remove old timestamps again)
                current_time = time.time()
                while dm_timestamps and dm_timestamps[0] < current_time - 3600:
                    dm_timestamps.popleft()
            # --- End Hourly Rate Limit Check ---


            # --- Account Selection ---
            if not accounts: # Check if the primary list is empty
                if not used_accounts: # Check if the used list is also empty
                    Modules.log(1, 'No accounts available (fresh or used). Breaking DM send loop for this cycle.')
                    # Put remaining tasks back? For now, they are lost for this cycle.
                    # dm_tasks.insert(0, task) # Put current task back
                    break # Break inner while loop
                else:
                    Modules.log(-1, 'Re-populating accounts from used list.')
                    accounts, used_accounts = used_accounts, list()

            try:
                account = accounts.pop(0)
            except IndexError:
                Modules.log(1, 'Account list unexpectedly empty. Breaking DM send loop.')
                # dm_tasks.insert(0, task) # Put current task back
                break # Break inner while loop
            # --- End Account Selection ---


            # --- Proxy Selection (Simplified as per UI changes) ---
            # Assuming no proxies are configured / needed based on UI removing proxy settings
            proxy = 'localhost'
            # --- End Proxy Selection ---

            Modules.log(0, f"Attempting DM {tasks_processed_this_cycle} to u/{username} using account {account.get('username', 'N/A')}...")

            # Record timestamp *before* sending for rate limiting
            dm_timestamps.append(time.time())

            try:
                # --- Run Async Bot Task ---
                # NOTE: This assumes RedditDMBot handles its own internal errors
                # and updates toss_accounts or used_accounts internally.
                # We are *not* getting a direct success/failure return value here.
                asyncio.run(
                    RedditDMBot(
                        config = config,
                        links = links,
                        paths = paths,
                        locators = locators,
                        proxy = proxy, # localhost
                        # list_usernames = list_usernames, # Pass for internal logic if still needed by RedditDMBot
                        used_accounts = used_accounts, # Pass mutable list
                        toss_accounts = toss_accounts, # Pass mutable list
                        account = account, # The chosen account
                        target = username, # Target user
                        personalized_message = message, # Composed message
                        post_url = post_url, # Post URL for logging
                        usernames_sent = usernames_sent # Pass for internal logic if still needed
                    )
                )
                Modules.log(0, f"Finished DM attempt for u/{username}.")
                # We assume success if no major error occurred *here*.
                # The actual logging to sent_log happens *inside* RedditDMBot currently.
                # If that needs changing, RedditDMBot must be modified.
                message_count_this_cycle += 1

            except Exception as e:
                 Modules.log(2, f"Unexpected error running asyncio task for {username}: {e}")
                 import traceback
                 traceback.print_exc()
                 # Decide what to do - maybe add account to toss_accounts here?
                 # toss_accounts.append(account['username'])
            # --- End Async Bot Task ---


            # --- Pacing Delay ---
            base_delay = max(0, min_dm_gap_sec) # Ensure base delay isn't negative
            actual_jitter = random.uniform(-jitter_sec, jitter_sec)
            sleep_duration = max(0.1, base_delay + actual_jitter) # Ensure minimum sleep to prevent rapid loops on 0 config
            Modules.log(-1, f"Sleeping for {sleep_duration:.2f} seconds before next DM...")
            time.sleep(sleep_duration)
            # --- End Pacing Delay ---
        dm_tasks = []
        Modules.log(0, "Clearing DM tasks for next cycle.")
        # --- End of Inner DM Sending Loop ---
        Modules.log(0, f'DM sending loop finished for this cycle. DMs attempted/sent in cycle: {message_count_this_cycle}.')

        # --- Sleep before next Harvest Cycle ---
        Modules.log(0, f"Sleeping for harvest interval: {harvest_interval_sec} seconds...")
        time.sleep(harvest_interval_sec)
        # --- End Sleep ---

    # This part is likely unreachable because of `while True`
    Modules.log(-1, '[RedditDMBot] - Main loop exited (unexpected).')
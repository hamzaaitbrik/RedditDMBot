from modules import *
from module_utils import Modules
from harvester import poll_subreddit_new
from message_composer import compose_dm_message_openai_lib
import time # Add time import
import random # Add random import
from collections import deque # Use deque for efficient timestamp tracking


async def test_ws():
    config = Modules.getConfig()
    browser, instance = None, None # Initialize here

    # initializing a config instance for the browser
    browser_config = zendriver.Config(
        browser_args = config['browser_args']
    )

    # headless or headfull?
    browser_config.headless = config['headless']

    # Add --no-sandbox argument
    if '--no-sandbox' not in browser_config.browser_args:
        browser_config.browser_args.append('--no-sandbox')

    browser = await zendriver.start(
            config = browser_config
        )

    instance = await browser.get("https://www.w3.org/WAI/UA/TS/html401/cp0101/0101-TEXTAREA.html")
    sleep(3)
    text_area = await instance.find(
        tagname = 'textarea',
        attrs = {
            "id":"textarea1",
        },
        timeout = 15
    )
    test_message_with_newlines = "Hello, world!\r\nThis is a test message with newlines."
    await text_area.send_keys(test_message_with_newlines)

    sleep(10)

    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_ws())
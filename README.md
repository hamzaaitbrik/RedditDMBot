Augments https://github.com/hamzaaitbrik/RedditDMBot.git

# Reddit DM Bot (Zendriver Version)

This bot automates sending personalized direct messages (DMs) to Reddit users based on their recent posts in specified subreddits. It leverages OpenAI for message composition and Zendriver for robust browser automation, making it less prone to detection than Selenium or Playwright.

# Prerequisites

1.  **Python:** Ensure you have Python installed (developed with 3.11+). You can download it from [python.org](https://www.python.org/). Pip (Python's package installer) should be included.
2.  **Pipenv:** A tool for managing project dependencies and virtual environments.
    - **macOS (using Homebrew):** `brew install pipenv`
    - **Other Systems (using pip):** `pip install pipenv`
3.  **Git:** Required to clone the repository.

# Installation & Setup

1.  **Clone Repository:** Open your terminal and run:
    ```bash
    git clone ...
    cd RedditDMBot
    ```
2.  **Install Dependencies:** Use Pipenv to create a virtual environment and install the required packages:
    ```bash
    pipenv install
    ```
    This reads the `Pipfile` and installs libraries like `requests`, `openai`, `streamlit`, `zendriver`, etc.
3.  **Activate Environment:** Enter the virtual environment created by Pipenv:
    ```bash
    pipenv shell
    ```
    You should now see the environment name (e.g., `(RedditDMBot)`) at the beginning of your terminal prompt. **All subsequent commands should be run within this shell.**
4.  **OpenAI API Key:** Set your OpenAI API key as an environment variable. The message composer needs this to function.
    - **Linux/macOS:** `export OPENAI_API_KEY='sk-your_real_key'`
    - **Windows (cmd):** `set OPENAI_API_KEY=sk-your_real_key`
    - **Windows (PowerShell):** `$env:OPENAI_API_KEY='sk-your_real_key'`
      (Replace `sk-your_real_key` with your actual key). You might want to add this to your shell's profile (`.zshrc`, `.bashrc`, etc.) for persistence.

# Configuration

Instead of manually editing JSON files, use the built-in Streamlit configuration UI:

1.  **Run the UI:** While inside the Pipenv shell (`pipenv shell`), run:
    ```bash
    streamlit run config_ui.py
    ```
2.  **Edit Settings:** This will open a configuration page in your web browser. Adjust the following:
    - **General Settings:** Target subreddits, cooldowns.
    - **Reddit Accounts:** Add/edit/delete the Reddit accounts the bot will use for logging in and sending DMs.
    - **OpenAI Message Composer:** Configure your OpenAI API Key (if not set via environment variable), the AI model (e.g., `gpt-4o-mini`), message template, persona rules, brand blurb, and app link. The AI will use these to craft personalized messages.
    - **Advanced Settings & Pacing:** Control DM sending rates (minimum gap, jitter, max per hour).
    - **File Paths:** Verify the paths for the Sent Log file.
3.  **Save:** Click the "Save All Configurations" button at the bottom. This will update `rsrc/config.json`, `rsrc/paths.json`, and `rdt/accounts.json`.

# How to Use

The bot operates in two main (conceptual) stages: Harvesting/Composing and Sending. Currently, these are combined within the main script's loop.

1.  **Ensure you are in the Pipenv shell:** `pipenv shell`
2.  **Run the Bot:**
    ```bash
    python RedditDMBot.py
    ```

# How it Works (Current Workflow)

1.  **Initialization:** The script loads configurations (`config.json`, `paths.json`), Reddit accounts (`accounts.json`), and the sent log (`sent_log.csv` specified in `paths.json`).
2.  **Main Loop (`while True`):**
    - **Harvesting:** It polls the target subreddits (defined in `config.json`) for recent posts using `harvester.py`'s `poll_subreddit_new` function.
    - **Composition:** For each harvested post, it calls OpenAI (via `message_composer.py`) using your configured template, rules, and API key to generate a personalized message.
    - **Task Queue:** Creates an in-memory list (`dm_tasks`) of tasks, each containing the target `username`, the `composed_message`, and the original `post_url`.
    - **DM Sending Sub-Loop:** Processes the `dm_tasks` list one by one:
      - **Filtering:** Checks the `sent_log.csv` data. If a DM has already been sent to that `username` for that specific `post_url`, it skips the task.
      - **Rate Limiting:** Checks timestamps of recent DM attempts to ensure the `MAX_DM_PER_HOUR` limit isn't exceeded. Pauses if necessary.
      - **Account Selection:** Picks an available Reddit account from the pool, rotating through used accounts if needed.
      - **DM Attempt:** Uses `zendriver` to:
        - Log into the selected Reddit account.
        - Navigate to the target user's profile/chat page.
        - Send the `composed_message`.
      - **Logging Success:** If the DM appears to be sent successfully (based on checks within the `RedditDMBot` function), it appends the `username`, `post_url`, and current `timestamp` to the `sent_log.csv` file.
      - **Pacing:** Waits for a calculated duration (`MIN_DM_GAP_SEC` +/- `JITTER_SEC`) before processing the next task.
    - **Cycle Delay:** After processing all tasks generated in the current harvest cycle, it sleeps for the `HARVEST_INTERVAL_SEC` before starting the next harvest.

This cycle repeats indefinitely until the script is stopped (e.g., with Ctrl+C).

Enjoy!

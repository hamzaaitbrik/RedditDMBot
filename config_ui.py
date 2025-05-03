import streamlit as st
import json
import os

CONFIG_PATH = os.path.join('rsrc', 'config.json')
PATHS_PATH = os.path.join('rsrc', 'paths.json')
ACCOUNTS_PATH = os.path.join('rdt', 'accounts.json') # Define path for accounts.json

def load_json(filepath):
    """Loads configuration from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: Configuration file not found at {filepath}")
        return None
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from {filepath}")
        return None

def save_json(filepath, data):
    """Saves configuration to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        st.success(f"Configuration saved successfully to {filepath}!")
        return True
    except IOError as e:
        st.error(f"Error saving configuration to {filepath}: {e}")
        return False
    except Exception as e:
        st.error(f"An unexpected error occurred while saving {filepath}: {e}")
        return False


st.set_page_config(layout="wide")
st.title("Reddit DM Bot Configuration")

# Load both config.json and paths.json
config = load_json(CONFIG_PATH)
paths_config = load_json(PATHS_PATH)
accounts_data = load_json(ACCOUNTS_PATH) # Load accounts data

# Initialize if loading failed
if config is None:
    config = {}
if paths_config is None:
    paths_config = {}
if accounts_data is None:
    # If accounts.json doesn't exist or is invalid, start with an empty list
    accounts_data = []
    st.warning(f"Could not load accounts from {ACCOUNTS_PATH}. You can add new accounts below.")


col1, col2 = st.columns(2)

with col1:
    st.header("General Settings")
    config['cooldown'] = st.number_input("Base Cooldown (seconds)", value=float(config.get('cooldown', 5)), min_value=0.1, step=0.5, format="%.1f", help="General delay used in various parts of the bot.")
    config['target_subreddits'] = st.text_area("Target Subreddits (one per line)", value="\n".join(config.get('target_subreddits', [])), height=100)
    config['target_subreddits'] = [sub.strip() for sub in config['target_subreddits'].split('\n') if sub.strip()]
    st.header("OpenAI Message Composer Settings")
    st.caption("The bot builds the prompt using the rules, template, brand blurb, and post details, replacing {username}. It uses the model specified below.")
    config['openaiApiKey'] = st.text_input("OpenAI API Key", value=config.get('openaiApiKey', ''), type="password", help="Your secret OpenAI API key (sk-...)")
    config['openaiModel'] = st.text_input("OpenAI Model", value=config.get('openaiModel', 'gpt-4o-mini'), help="e.g., gpt-4o-mini, gpt-4o, gpt-3.5-turbo")
    config['messageTemplate'] = st.text_area("Message Template", value=config.get('messageTemplate', "Hi {username}, saw your post about [briefly mention topic - AI should fill this]. Thought you might find this interesting: {brandBlurb}. Check it out: {appLink}"), height=150, help="Template for the AI to fill. Must include '[briefly mention topic - AI should fill this]'. Can use {username}, {brandBlurb}, {appLink}.")
    config['personaRules'] = st.text_area("Persona Rules for AI", value=config.get('personaRules', '- Be concise and direct.\n- Sound genuinely helpful, not overly salesy.\n- Avoid emojis.'), height=100)
    config['brandBlurb'] = st.text_input("Brand Blurb", value=config.get('brandBlurb', 'our cool new app'))
    config['appLink'] = st.text_input("App Link", value=config.get('appLink', 'https://example.com/app'))

    # --- Reddit Accounts Management --- #
    st.header("Reddit Accounts")
    st.caption(f"Manage accounts stored in {ACCOUNTS_PATH}")

    edited_accounts = st.data_editor(
        accounts_data, # Pass the loaded list of dicts
        num_rows="dynamic", # Allow adding/deleting rows
        key="accounts_editor",
        column_config={
            "username": st.column_config.TextColumn("Reddit Username", required=True),
            "password": st.column_config.TextColumn("Reddit Password", required=True),
            # Add other columns if your accounts.json has more fields
        },
        hide_index=True,
        use_container_width=True
    )
    # Store the edited data back (will be saved on button press)
    accounts_data = edited_accounts
    # --- End Reddit Accounts Management --- #

with col2:
    st.header("Advanced Settings & Pacing")
    st.caption("Pacing: Approx. 1 DM every MIN_DM_GAP_SEC +/- JITTER_SEC seconds.")
    config['HARVEST_INTERVAL_SEC'] = st.number_input("Harvest Interval (sec)", value=config.get('HARVEST_INTERVAL_SEC', 30), min_value=5, help="How often the harvester checks for new posts (if run continuously). Currently harvester runs once.")
    config['MIN_DM_GAP_SEC'] = st.number_input("Min DM Gap (sec)", value=config.get('MIN_DM_GAP_SEC', 60), min_value=10, help="Minimum time between sending DMs.")
    config['JITTER_SEC'] = st.number_input("DM Jitter (sec)", value=config.get('JITTER_SEC', 15), min_value=0, max_value=config.get('MIN_DM_GAP_SEC', 60) // 2, help="Random seconds added/subtracted to MIN_DM_GAP_SEC.")
    config['MAX_DM_PER_HOUR'] = st.number_input("Max DMs per Hour (approx)", value=config.get('MAX_DM_PER_HOUR', 40), min_value=1, help="An approximate safety limit.")

    st.header("File Paths")
    paths_config['sent_log_file'] = st.text_input("Sent Log File Path", value=paths_config.get('sent_log_file', 'logs/sent_log.csv'), help="Path relative to project root where sent DMs are logged.")
    paths_config['usernames_sent'] = paths_config.get('usernames_sent') # Ensure consistency if old code uses this key

st.divider()

if st.button("Save All Configurations", use_container_width=True):
    # Check if config objects were loaded successfully
    config_valid = config is not None
    paths_valid = paths_config is not None

    if config_valid:
        save_json(CONFIG_PATH, config)
    else:
        st.error("Main configuration (config.json) was not loaded, cannot save.")

    if paths_valid:
        save_json(PATHS_PATH, paths_config)
    else:
        st.error("Paths configuration (paths.json) was not loaded, cannot save.")

    # Save accounts data
    if accounts_data is not None: # Check if data exists (even if empty list)
        # Basic validation: Ensure required keys are present if list is not empty
        valid_accounts = True
        if isinstance(accounts_data, list):
            for i, acc in enumerate(accounts_data):
                if not isinstance(acc, dict) or 'username' not in acc or 'password' not in acc or not acc['username'] or not acc['password']:
                    st.error(f"Account entry #{i+1} is invalid or missing username/password. Please correct before saving.")
                    valid_accounts = False
                    break
        else:
             st.error("Accounts data structure is invalid (must be a list of dictionaries). Cannot save.")
             valid_accounts = False

        if valid_accounts:
            save_json(ACCOUNTS_PATH, accounts_data)
    else:
         # This case should ideally not happen due to initialization
         st.error("Accounts data is missing. Cannot save.") 
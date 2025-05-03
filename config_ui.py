import streamlit as st
import json
import os

CONFIG_PATH = os.path.join('rsrc', 'config.json')

def load_config():
    """Loads the configuration from config.json"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: Configuration file not found at {CONFIG_PATH}")
        return None
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from {CONFIG_PATH}")
        return None

def save_config(config_data):
    """Saves the configuration to config.json"""
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config_data, f, indent=4)
        st.success("Configuration saved successfully!")
    except IOError as e:
        st.error(f"Error saving configuration: {e}")


st.set_page_config(layout="wide")
st.title("Reddit DM Bot Configuration")

config = load_config()

if config:
    st.header("General Settings")
    config['headless'] = st.checkbox("Run Headless", value=config.get('headless', True))
    config['cooldown'] = st.number_input("Cooldown (seconds)", value=float(config.get('cooldown', 5)), min_value=0.1, step=0.5, format="%.1f")

    st.header("Browser Arguments")
    # Display list as a newline-separated string
    browser_args_str = "\n".join(config.get('browser_args', []))
    new_browser_args_str = st.text_area("Browser Arguments (one per line)", value=browser_args_str, height=150)
    # Convert back to list, stripping empty lines
    config['browser_args'] = [arg.strip() for arg in new_browser_args_str.split('\n') if arg.strip()]

    st.header("Messages")
    # Display list as a newline-separated string
    messages_str = "\n".join(config.get('messages', []))
    new_messages_str = st.text_area("Messages (one per line, chosen randomly)", value=messages_str, height=200)
    # Convert back to list, stripping empty lines
    config['messages'] = [msg.strip() for msg in new_messages_str.split('\n') if msg.strip()]

    st.header("Proxy Settings")
    proxy_config = config.get('proxy', {})
    proxy_config['proxy_type'] = st.selectbox(
        "Proxy Type",
        options=['localhost', 'sticky', 'rotative'],
        index=['localhost', 'sticky', 'rotative'].index(proxy_config.get('proxy_type', 'localhost'))
    )
    proxy_config['proxy_rotation_link'] = st.text_input("Proxy Rotation Link (for 'rotative')", value=proxy_config.get('proxy_rotation_link', ''))
    proxy_config['proxy_rotation_cooldown'] = st.number_input("Proxy Rotation Cooldown (seconds)", value=proxy_config.get('proxy_rotation_cooldown', 10), min_value=0)

    config['proxy'] = proxy_config # Update the main config dict

    st.divider()

    if st.button("Save Configuration", use_container_width=True):
        save_config(config)

else:
    st.warning("Could not load configuration.") 
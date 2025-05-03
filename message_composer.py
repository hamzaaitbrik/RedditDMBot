import openai # Use the official OpenAI library
import json
import os
from typing import Dict, Any, Optional
from module_utils import Modules

# Example user configuration (in a real scenario, load this from your config)
DEFAULT_USER_CONFIG = {
    "openaiApiKey": os.getenv("OPENAI_API_KEY", "sk-..."),
    "openaiModel": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
    "messageTemplate": "Hi {username}, saw your post about [briefly mention topic - AI should fill this]. Thought you might find this interesting: {brandBlurb}. Check it out: {appLink}",
    "personaRules": """
    - Be concise and direct.
    - Sound genuinely helpful, not overly salesy.
    - Avoid emojis.""",
    "brandBlurb": "our cool new app",
    "appLink": "https://example.com/app"
}
# --- End Configuration ---

# Initialize the OpenAI client globally or within the function
# Global initialization is fine if the API key doesn't change often.
# The client will automatically pick up the OPENAI_API_KEY environment variable.
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except openai.OpenAIError as e:
     Modules.log(1, f"[Composer] ERROR: Failed to initialize OpenAI client: {e} Exiting...")
     exit()

def compose_dm_message_openai_lib( # Renamed slightly for clarity
    post_data: Dict[str, Any],
    user_config: Dict[str, Any] = DEFAULT_USER_CONFIG
) -> Optional[str]:
    post_author = post_data.get('author', 'user')
    post_title = post_data.get('title', '')


    message_template = user_config.get("messageTemplate", "")
    persona_rules = user_config.get("personaRules", "")
    brand_blurb = user_config.get("brandBlurb", "")
    app_link = user_config.get("appLink", "")

    Modules.log(0, f"[Composer] Composing message for u/{post_author} regarding post: {post_title}")

    # Pre-fill parts of the template (same as before)
    final_template = message_template
    if "{username}" in final_template:
         final_template = final_template.replace("{username}", post_author)
    if "{appLink}" in final_template:
         final_template = final_template.replace("{appLink}", app_link)
    if "{brandBlurb}" in final_template:
         final_template = final_template.replace("{brandBlurb}", brand_blurb)

    system_prompt = f"""
You are a friendly assistant helping users discover relevant information based on their Reddit posts.
Your personality and tone should follow these rules:
{persona_rules}
Your goal is to adapt the provided message template. You MUST fill in the placeholder "[briefly mention topic - AI should fill this]" based on the user's post title provided. Keep the topic mention very short (a few words).
Ensure the final output strictly adheres to the structure of the template provided in the user message. Do not add any extra greetings, closings, or text beyond the template structure.
Output only the final, complete message text.
    """.strip()

    user_prompt = f"""
User Post Title: "{post_title}"
---
Message Template to use (fill in the topic placeholder):
{final_template}
    """.strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        model = user_config.get("openaiModel", "gpt-3.5-turbo")
        Modules.log(0, f"[Composer] Sending request to OpenAI API (Model: {model}) via library...")
        # Use the client.chat.completions.create method
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            n=1
            # timeout=30 # You can set timeouts here too
        )

        # Access the response content
        if response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message.content
            if message_content:
                composed_message = message_content.strip()
                Modules.log(0, f"[Composer] Successfully composed message for u/{post_author}")
                return composed_message
            else:
                 Modules.log(1, "[Composer] ERROR: 'content' missing in OpenAI response choice.")
                 print(f"[Composer] Full Response Object: {response}")
                 return None
        else:
            Modules.log(1, f"[Composer] ERROR: 'choices' array missing or empty in OpenAI response.")
            Modules.log(1, f"[Composer] Full Response Object: {response}")
            return None
        
    except Exception as e:
        Modules.log(1, f"[Composer] ERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None


# --- Main block for testing ---
def main_test():
    print("--- Running Message Composer Test (using OpenAI Library) ---")


    mock_post = {
        'author': 'TestUser123',
        'title': 'Looking for advice on scaling my Python web application',
        'subreddit': 'Python',
        'url': 'https://example.com/post1',
        'created_utc': 1678886400,
        'selftext': 'My Flask app is getting slow...'
    }

    Modules.log(0, f"Using Mock Post:{json.dumps(mock_post, indent=2)}")
    Modules.log(0, f"Using Default Config (Template: '{DEFAULT_USER_CONFIG['messageTemplate']}')")

    # Call the library-based function
    composed_message = compose_dm_message_openai_lib(mock_post)

    if composed_message:
        Modules.log(0, "--- Successfully Composed Message ---")
        Modules.log(0, composed_message)
        Modules.log(0, "--- End of Message ---")
    else:
        Modules.log(1, "--- Failed to Compose Message ---")

    Modules.log(0, "--- Test Finished ---")


if __name__ == "__main__":
    main_test()
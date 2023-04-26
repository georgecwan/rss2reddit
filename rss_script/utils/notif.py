import os
from discordwebhook import Discord
from dotenv import load_dotenv

# Load the webhook url from the .env file
load_dotenv()
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

# Create the discord object
discord = Discord(url=webhook_url)


def send_discord_message(message: str) -> None:
    """
    Sends a message to the discord webhook url

    Args:
        message: The message to be sent to the discord webhook url

    Returns:
        None
    """
    # Check if the webhook url is specified
    if webhook_url:
        try:
            discord.post(content=message)
            print("Sent discord notification")
        except Exception as e:
            print(f"Error sending discord notification: {str(e)}")
    else:
        print("No webhook url found, skipping discord message")

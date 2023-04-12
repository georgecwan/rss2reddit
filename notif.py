import os
from discordwebhook import Discord
from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
discord = Discord(url=webhook_url)


def send_discord_message(message):
    if webhook_url:
        try:
            discord.post(content=message)
            print("Sent discord notification")
        except Exception as e:
            print(f"Error sending discord notification: {str(e)}")
    else:
        print("No webhook url found, skipping discord message")

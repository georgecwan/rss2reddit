import discord


TOKEN_ID = 'DISCORD_TOKEN_ID'
CHANNEL_ID = 123456789

def send_discord_notification(message):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
        channel = client.get_channel(CHANNEL_ID)
        if channel is not None:
            await channel.send(message)
            print('Discord message sent')
        else:
            print(f"Error occurred while finding Discord channel")
        await client.close()

    try:
        client.run(TOKEN_ID)
    except Exception as e:
        print(f"Error occurred in Discord Client: {str(e)}")

import discord
from discord.ext import commands
from secret import DISCORD_CLIENT_ID
import timecog
from discord_message_handler import handle_message

async def on_ready():
    print('discordbot... Logged on as {0}!'.format(client.user))
    await client.change_presence(status=discord.Status.invisible)

async def on_message(message):
    if message.author.name != client.user.name:
        print('discordbot... Message from {0.author}: {0.content}'.format(message))
        await handle_message(message)

client = commands.Bot(command_prefix=commands.when_mentioned_or('~'))
client.add_listener(on_ready)
client.add_listener(on_message)
client.load_extension('timecog')

client.run(DISCORD_CLIENT_ID)

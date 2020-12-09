import discord
from discord.ext import commands
from constants import DISCORD_CLIENT_ID
import timecog
from discord_message_handler import handle_message

role_name_to_emoji = {'advent of code':'😂'}

def setup_gaer_dictionary(): #guild and emoji to role
    for guild in client.guilds:
        for role in guild.roles:
            role_name = role.name.lower()
            if role_name in role_name_to_emoji.keys():
                emoji = role_name_to_emoji[role_name]
                if emoji:
                    gaer[(guild.id, emoji)] = role.id
    # print(gaer)

async def on_ready():
    print('discordbot... Logged on as {0}!'.format(client.user))
    client.cogs['Heartbeat'].setup_advent_blasts()
    client.intents.guild_reactions = False
    client.intents.members = True
    setup_gaer_dictionary()
    await client.change_presence(status=discord.Status.do_not_disturb)

async def on_message(message):
    if message.author.id != client.user.id:
        print('discordbot... Message from {0.author}: {0.content}'.format(message))
        await handle_message(message)

intents = discord.Intents.default()
# intents.members = True
# intents.guild_reactions = True

client = commands.Bot(command_prefix=commands.when_mentioned_or('~'), intents=intents)
client.add_listener(on_ready)
client.add_listener(on_message)
client.load_extension('timecog')

#Guild And Emoji to Role
gaer = {}

@client.event
async def on_raw_reaction_add(payload):
    # print(payload)
    channel = client.get_channel(payload.channel_id)
    guild = client.get_guild(payload.guild_id)
    if (channel and channel.name.lower() == "get-roles"):
        emoji = payload.emoji.name
        role_id = gaer[(payload.guild_id), emoji]
        if role_id:
            role = guild.get_role(role_id)
            await payload.member.add_roles(role)

# @client.event
# async def on_raw_reaction_remove(payload):
#     print(payload)
#     channel = client.get_channel(payload.channel_id)
#     guild = client.get_guild(payload.guild_id)
#     if (channel and channel.name.lower() == "get-roles"):
#         emoji = payload.emoji.name
#         role_id = gaer[(payload.guild_id), emoji]
#         if role_id:
#             role = guild.get_role(role_id)
#             member = guild.get_member(payload.user_id)
#             print(member)
#             await payload.member.remove_roles(role)

client.run(DISCORD_CLIENT_ID)

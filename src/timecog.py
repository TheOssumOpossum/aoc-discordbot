from discord.ext import commands, tasks
from datetime import datetime
from discord_api import send_message
from constants import TIMEZONE

class Heartbeat(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.heartbeat.start()
      self.advent_blasts = {} #role -> channel

   def cog_unload(self):
      self.heartbeat.stop()

   @tasks.loop(minutes=1)
   async def heartbeat(self):
      now = datetime.now(TIMEZONE)
      minute = now.minute
      hour = now.hour
      if now.hour == 23 and now.minute == 30 and ((now.day < 25 and now.month == 12) or (now.day == 30 and now.month == 11)):
         for role, channel in self.advent_blasts.items():
            await send_message("<@&{0}> starts in 30 minutes!".format(role), channel)

   @heartbeat.before_loop
   async def before_update_loop(self):
      await self.bot.wait_until_ready()

   def setup_advent_blasts(self):
      for guild in self.bot.guilds:
            for channel in guild.channels:
               if channel.name.lower() == "advent-of-code-2020":
                  send_to_channel = channel
                  break
            for role in guild.roles:
               if role.name.lower() == 'advent of code':
                  send_to_role = role.id
                  break
            if send_to_channel and send_to_role:
               self.advent_blasts[send_to_role] = send_to_channel
      # print(self.advent_blasts)


def setup(bot):
    bot.add_cog(Heartbeat(bot))

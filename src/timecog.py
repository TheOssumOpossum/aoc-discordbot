from discord.ext import commands, tasks
from datetime import datetime
from discord_api import send_message
from constants import TIMEZONE

class Heartbeat(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.heartbeat.start()
      self.msg_channel = '' #only works for one guild
      self.mention_role = '' #only works for one guild

   def cog_unload(self):
      self.heartbeat.stop()

   @tasks.loop(minutes=1)
   async def heartbeat(self):
      now = datetime.now(TIMEZONE)
      minute = now.minute
      hour = now.hour
      if now.hour == 23 and now.minute == 30:
         if self.msg_channel == '':
            self.msg_channel = get_channel(self.bot.get_all_channels(), "advent-of-code-2020")
            for g in self.bot.guilds:
               for r in g.roles:
                  if r.name.lower() == 'advent of code':
                     self.mention_role = r.id
         await send_message("<@&{0}> starts in 30 minutes!".format(self.mention_role), self.msg_channel)

   @heartbeat.before_loop
   async def before_update_loop(self):
      await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Heartbeat(bot))

def get_channel(channels, channel_name):
    for channel in channels:
        if channel.name == channel_name:
            return channel
    return None

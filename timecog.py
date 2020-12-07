from discord.ext import commands, tasks
from datetime import datetime
from bot import send_message, TIMEZONE

class Heartbeat(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.heartbeat.start()
      self.msg_channel = ''
      self.mention_role = ''

   def cog_unload(self):
      self.heartbeat.stop()

   @tasks.loop(minutes=1)
   async def heartbeat(self):
      alerted = False
      now = datetime.now(TIMEZONE)
      minute = now.minute
      hour = now.hour
      if now.hour == 23 and now.minute == 30:
         if self.msg_channel == '':
            self.msg_channel = get_channel(self.bot.get_all_channels(), "advent-of-code-2020")
            for g in self.bot.guilds:
               if g.name.lower() == '@adventofcode':
                  self.mention_role = g.id
         await send_message("<@&{0}> second is 3".format(self.mention_role), self.msg_channel)

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

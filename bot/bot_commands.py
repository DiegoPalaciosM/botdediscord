from discord.ext import commands

from utils import singleton

@singleton
class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        print(ctx.content.lower())
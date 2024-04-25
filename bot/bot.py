import asyncio
import threading
import os

from dotenv import load_dotenv

from discord import Intents
from discord.ext import commands

from utils import logger, singleton

from bot_commands import BotCommands
from player import PlayerCommands

dotenv_path = '/bot/.env'
load_dotenv(dotenv_path)

#load_dotenv()


@singleton
class LeyDeOhmBot(commands.Bot):
    def __init__(self):
        intents = Intents.all()
        commands.Bot.__init__(self, command_prefix='>',
                              self_bot=True, intents=intents, help_command=None)
        self.thread = None
        self.key = os.environ['DISCORD_KEY']

    def init(self):
        self.run(self.key)

    async def on_ready(self):
        await self.add_cog(BotCommands(self))
        await self.add_cog(PlayerCommands(self))
        logger.info('Bot Iniciado')

LeyDeOhmBot().init()
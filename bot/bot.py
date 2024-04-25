import asyncio
import threading
import django
import os

from discord import Intents
from discord.ext import commands

from discordBot.commands import logger, singleton

from bot.commands import BotCommands
from bot.player import PlayerCommands


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "discordBot.settings")
django.setup()

@singleton
class LeyDeOhmBot(commands.Bot):
    def __init__(self):
        intents = Intents.all()
        commands.Bot.__init__(self, command_prefix='>',
                              self_bot=True, intents=intents, help_command=None)
        self.thread = None
        self.key = os.environ['DISCORD_KEY']

    def init(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.thread = threading.Thread(
            target=self.run, args=(self.key,), daemon=True)
        self.thread.start()
        self.thread.setName("LeyDeOhmBot")

    async def on_ready(self):
        await self.add_cog(BotCommands(self))
        await self.add_cog(PlayerCommands(self))
        logger.info('Bot Iniciado')
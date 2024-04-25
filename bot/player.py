import asyncio
import time
from discord import FFmpegOpusAudio, Embed
from discord.ext import commands

from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

from lang import *

from bot_commands import singleton

lang = es

@singleton
class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.queue = []
        self.playing = None
        self.ydl_format = {'format': 'bestaudio',
                           'noplaylist': 'True', 'quiet': True, }
        self.fmmpg_format = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.command()
    async def join(self, ctx):
        try:
            voice_channel = ctx.message.author.voice.channel
            self.voice_client = ctx.message.author.guild.voice_client
        except Exception as e:
            voice_channel = False
        if voice_channel:
            if self.voice_client:
                if voice_channel != self.voice_client.channel:
                    await self.voice_client.disconnect()
                    self.voice_client = await voice_channel.connect(self_deaf=True)
                    await ctx.message.reply(f'''{lang['connect_channel_voice']} <#{voice_channel.id}>''')
            else:
                self.voice_client = await voice_channel.connect(self_deaf=True)
                await ctx.message.reply(f'''{lang['connect_channel_voice']} <#{voice_channel.id}>''')
            return True
        else:
            await ctx.message.reply(
                lang['need_voice_channel'])
            return False

    @commands.command()
    async def leave(self, ctx):
        try:
            voice_client = ctx.message.author.guild.voice_client
            await voice_client.disconnect()
            self.queue.clear()
        except:
            await ctx.message.reply(lang['not_connected_voice_channel'])

    @commands.command()
    async def play(self, ctx, *args):
        if await self.join(ctx):
            if self.voice_client.is_paused():
                self.voice_client.resume()
            else:
                if args:
                    video = self.getVideo(ctx, ' '.join(args))
                    self.queue.append(video)
                    await ctx.send(lang['link_added_to_queue'], embed=Embed.from_dict(self.vidEmbed(video)))
                if not self.voice_client.is_playing():
                    self.play_audio()

    @commands.command()
    async def skip(self, ctx):
        if self.voice_client:
            self.voice_client.stop()
            if not len(self.queue):
                await self.voice_client.disconnect()

    @commands.command()
    async def queue(self, ctx):
        await ctx.message.reply(embed=Embed.from_dict(self.queueEmbed()))

    @commands.command()
    async def clear(self, ctx, *args):
        if len(args):
            try:
                await ctx.reply(lang['delete_from_queue'], embed=Embed.from_dict(self.vidEmbed(self.queue[int(args[0]) - 1])))
                del self.queue[int(args[0]) - 1]
            except:
                await ctx.reply(lang['index_doesnt_exist_in_queue'])
        else:
            self.queue.clear()
            await ctx.reply(lang['delete_queue'])

    def getVideo(self, ctx, link):
        with YoutubeDL(self.ydl_format) as ydl:
            video_info = ydl.extract_info(VideosSearch(link, limit=1).result()[
                                          'result'][0]['link'], download=False)
            video_info['ctx'] = ctx
        return video_info

    def play_audio(self, another=None):
        if len(self.queue):
            self.playing = self.queue[0]
            audio = FFmpegOpusAudio(
                source=self.playing['url'], **self.fmmpg_format)
            while not self.voice_client.is_connected():
                time.sleep(0.1)
            self.queue.pop(0)
            self.voice_client.play(
                audio, after=self.play_audio)
            asyncio.run_coroutine_threadsafe(
                coro=self.playing['ctx'].send(lang['next_from_queue'], embed=Embed.from_dict(self.vidEmbed(self.playing))), loop=self.voice_client.loop)
        else:
            asyncio.run_coroutine_threadsafe(coro=self.playing['ctx'].send(
                lang["nothing_in_queue"]), loop=self.voice_client.loop).result()
            asyncio.run_coroutine_threadsafe(
                coro=self.voice_client.disconnect(), loop=self.voice_client.loop).result()

    def vidEmbed(self, video_info):
        return {
            'title': video_info['title'],
            'color': 0x215aa0,
            'url': video_info['webpage_url'],
            'thumbnail': {
                'url': video_info['thumbnail']
            },
            'author': {
                'name': 'Ley de Ohm',
                'icon_url': "https://cdn.discordapp.com/avatars/982727308433555556/5003107155eea0a278bb43bba460144c.png?size=128"
            },
            'fields': [
                {'name': lang['duration'],
                 'value': video_info['duration_string'], 'inline': True},
                {'name': lang['added_by'],
                 'value': video_info['ctx'].author.name, 'inline': True}
            ]
        }

    def queueEmbed(self):
        lista = [{'name': f'''{index + 1}: {info['title']}''', 'value': f'''{lang['added_by']}: {info['ctx'].author.name}'''}
                 for index, info in enumerate([vid for vid in self.queue])]
        return {
            'title': lang['queue'],
            'color': 0x215aa0,
            'author': {
                'name': 'Ley de Ohm',
                'icon_url': "https://cdn.discordapp.com/avatars/982727308433555556/5003107155eea0a278bb43bba460144c.png?size=128"
            },
            'fields': [{'name': lang['empty_queue'], 'value': lang['helper_create_queue']}] if not lista else lista
        }

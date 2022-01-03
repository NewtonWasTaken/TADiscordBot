import discord
from discord.ext import commands
import asyncio
import youtube_dl
import os
import pymongo

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
storage = mongo_client['TABOT']['storage']

ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

song_queue = {}

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Připojí bota k tobě na voice.', usage='!connect')
    async def connect(self, ctx):
        channel = ctx.author.voice
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if channel == None:
            await ctx.send('Musíš být připojen do kanálu na připojení bota')
        else:
            if voice == None:
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
                await ctx.send('Bot připojen na voice!')
                return (True)
            else:
                return (True)
                await ctx.send('Bot už je připojen jinde')

    @commands.command(help='Odpojí bota z voice.', usage='!leave')
    async def leave(self, ctx):
        channel = ctx.author.voice
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if channel == None:
            await ctx.send('Musíš být připojen do kanálu na odpojení bota')
        elif voice.channel.id == ctx.author.voice.channel.id:
            song_queue[str(ctx.guild.id)] = []
            await voice.disconnect()
            await ctx.send('Bot byl odpojen z voicu!')
        else:
            await ctx.send('Musíš být připojen do stejného kanálu na odpojení bota')

    @commands.command(help='Připojí bota k tobě na voice a přehraje skladbu. Linky pouze z youtube. Nepoužívat playlisty.', usage='!play [link]')
    async def play(self, ctx, *, url):
        if await self.connect(ctx):
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if self.search(url, ctx.author, ctx.guild):
                if not voice.is_playing():
                        voice.play(discord.FFmpegPCMAudio(song_queue[str(ctx.guild.id)][0]['source'], **FFMPEG_OPTIONS),
                                   after=lambda e: self.play_next(ctx))
                        voice.is_playing()
                        embed = discord.Embed(title="Hudba", color=0x1927e6)
                        embed.set_thumbnail(
                            url=self.client.user.avatar_url)
                        embed.add_field(name="Právě hraje",
                                        value=f"[{song_queue[str(ctx.guild.id)][0]['title']}]({song_queue[str(ctx.guild.id)][0]['link']})",
                                        inline=False)
                        embed.add_field(name=f"Song navrhl: ", value=f"{song_queue[str(ctx.guild.id)][0]['user'].mention}",
                                        inline=False)
                        await ctx.send(embed=embed)
                else:
                        embed = discord.Embed(title="Hudba", color=0x1927e6)
                        embed.set_thumbnail(
                            url=self.client.user.avatar_url)
                        embed.add_field(name="Přidáno do řady", value=f"[{song_queue[str(ctx.guild.id)][-1]['title']}]({song_queue[str(ctx.guild.id)][-1]['link']})", inline=False)
                        embed.add_field(name=f"Song navrhl: ", value=f"{song_queue[str(ctx.guild.id)][-1]['user'].mention}", inline=False)
                        await ctx.send(embed=embed)
            else:
                await ctx.send('Tento song je blacklistnutý, nepouštěj ho chuju! :warning:')

    @commands.command(help='Přeskočí song co právě hraje', usage='!skip')
    async def skip(self, ctx):
        channel = ctx.author.voice
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if channel == None:
            await ctx.send('Musíš být připojen do kanálu na skipnutí songu')
        elif voice.channel.id == ctx.author.voice.channel.id:
            if voice.is_playing():
                self.skip_song(ctx)
            else:
                await ctx.send('Nic nehraje...')
        else:
            await ctx.send('Musíš být připojen do stejného kanálu na skipnutí')

    @commands.command(help='Pozastaví aktualní song.', usage='!pause')
    async def pause(self, ctx):
        channel = ctx.author.voice
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if channel == None:
            await ctx.send('Musíš být připojen do kanálu na pausnutí songu')
        elif voice.channel.id == ctx.author.voice.channel.id:
            if voice.is_playing():
                voice.pause()
                await ctx.send('Pozasatveno :pause_button:')
            else:
                await ctx.send('Nic nehraje...')
        else:
            await ctx.send('Musíš být připojen do stejného kanálu na pause')

    @commands.command(help='Opět spustí pozastavený song.', usage='!resume')
    async def resume(self, ctx):
        channel = ctx.author.voice
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if channel == None:
            await ctx.send('Musíš být připojen do kanálu na pausnutí songu')
        elif voice.channel.id == ctx.author.voice.channel.id:

            voice.resume()
            await ctx.send('Pokračujeme... :play_pause:')

        else:
            await ctx.send('Musíš být připojen do stejného kanálu na pause')

    def skip_song(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if len(song_queue[str(ctx.guild.id)]) > 0:
            voice.stop()
            asyncio.run_coroutine_threadsafe(ctx.send('Skipnuto :white_check_mark:'), self.client.loop)

    def play_next(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if len(song_queue[str(ctx.guild.id)]) > 1:
            del song_queue[str(ctx.guild.id)][0]
            voice.play(discord.FFmpegPCMAudio(song_queue[str(ctx.guild.id)][0]['source'], **FFMPEG_OPTIONS),
                       after=lambda e: self.play_next(ctx))
            voice.is_playing()
            embed = discord.Embed(title="Hudba", color=0x1927e6)
            embed.set_thumbnail(
                url=self.client.user.avatar_url)
            embed.add_field(name="Právě hraje",
                            value=f"[{song_queue[str(ctx.guild.id)][0]['title']}]({song_queue[str(ctx.guild.id)][0]['link']})",
                            inline=False)
            embed.add_field(name=f"Song navrhl: ", value=f"{song_queue[str(ctx.guild.id)][0]['user'].mention}",
                            inline=False)
            asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
        else:
            try:
                del song_queue[str(ctx.guild.id)][0]
                asyncio.run_coroutine_threadsafe(ctx.send('Konec řady. :white_check_mark:'), self.loop)
            except:
                asyncio.run_coroutine_threadsafe(ctx.send('Konec řady. :white_check_mark:'), self.client.loop)

    def search(self, arg, user, server):
        blacklist = storage.find_one({'id': '1'})
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(arg, download=False)
        try:
            song = {'type': info['_type'], 'entries': info['entries'], 'user': user}
        except:
            song =  {'type': 'single', 'source': info['formats'][0]['url'], 'title': info['title'],
            'link': f'https://www.youtube.com/watch?v={info["id"]}', 'user': user, 'id': info['id']}
        if song['type'] == 'playlist':
            for single in song['entries']:
                try:
                    song_queue[str(server.id)].append({'type': 'single', 'source': single['formats'][0]['url'], 'title': single['title'],
            'link': f'https://www.youtube.com/watch?v={single["id"]}', 'user': user, 'id': single['id']})
                except:
                    song_queue[str(server.id)] = []
                    song_queue[str(server.id)].append({'type': 'single', 'source': single['formats'][0]['url'], 'title': single['title'],
            'link': f'https://www.youtube.com/watch?v={single["id"]}', 'user': user, 'id': single['id']})
            return True
        else:
            if song['id'] in blacklist['links']:
                return False
            else:
                try:
                    song_queue[str(server.id)].append(song)
                except:
                    song_queue[str(server.id)] = []
                    song_queue[str(server.id)].append(song)
                return True



def setup(client):
    client.add_cog(Music(client))
import discord
from discord.ext import commands
from google_trans_new import google_translator
from discord.utils import get
import requests
import os
import random
from callouts import Callouts
translator = google_translator()
class Funkce(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(help='Nikdy nevíš', usage='!shrug')
    async def shrug(self, ctx):
        await ctx.send('¯\_(ツ)_/¯')

    @commands.command(help='Nezobrazí ping bota', usage='!ping')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(help='to je opravdu yum', usage='!yum')
    async def yum(self, ctx):
        await ctx.send('yim yum')

    @commands.command(help='Zobrazí ping bota', usage='!pong')
    async def pong(self, ctx):
        await ctx.send(f'Nemyslel jsi ping? {round(self.client.latency * 1000)}ms')

    @commands.command(help='Zavolá bajs na kompet', usage='!kompet')
    async def kompet(self, ctx):
        await ctx.send(
            '<@621353544490024961> , <@551426822299189259>, <@621701863821148166>, <@558659043833675806> pojďte hrát!')

    @commands.command(help=f'Ukáže {Callouts().name} Coin zblízka', usage='!emote')
    async def emote(self, ctx):
        await ctx.send(f'{Callouts().emote}')

    @commands.command(help='Kdo vyrobil bota?',usage='!credit')
    async def credit(self, ctx):
        embed = discord.Embed(
            title="Credits",
            description=
            "Tohoto bota vytvořil: <@551426822299189259> . ",
            color=0x14db3c)
        embed.set_thumbnail(
            url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help='Přeloží zadaný text z EN do CZ', usage='!translate [text]')
    async def translate(self, ctx):
        await ctx.send('Překladač je dočasně nedostupný...')

    @commands.command(help='Zobrazí help na všechny commandy', usage='!help (command-nepovinný)')
    async def help(self, ctx, command=None):
            command_names_list = [x.name for x in self.client.commands]
            if command in command_names_list:
                help = self.client.get_command(command).help
                usage = self.client.get_command(command).usage
                embed = discord.Embed(title=f"Help !{command}", description=f"Tady je help pro command {command}:", color=0xff0000)
                embed.set_author(name=f"{Callouts().name} Discord Bot")
                embed.set_thumbnail(
                    url=self.client.user.avatar_url)
                embed.add_field(name="Použití:", value=f"`{usage}`", inline=False)
                embed.add_field(name="Co dělá?", value=f"`{help}`", inline=True)
                embed.set_footer(text="Pro help s jakýmkoli commandem napiš !help [command]")
                await ctx.send(embed=embed)
            elif command == None:
                embed = discord.Embed(
                    title="Help",
                    description=
                    "Pokud potřebuješ s čimkoli pomoct, tady jsou všechny příkazy:",
                    color=0xff0000)
                embed.set_author(name=f"{Callouts().name} Discord Bot")
                embed.set_thumbnail(
                    url=
                    self.client.user.avatar_url
                )
                embed.add_field(name="Funkce :gear: ", value="`ping` `pong` `status` `mute` `unmute` `clear` `kick` `ban` `blacklist`", inline=False)
                embed.add_field(name=f"Vlastní commandy {Callouts().emote} ",
                                value="`yum` `emote` `kompet` `credit` `shrug` `translate`", inline=False)
                embed.add_field(name="Random věci :slot_machine: ",
                                value="`ucitel` `howgay` `simp` `rng` `meme` `student` `news`",
                                inline=False)
                embed.add_field(name="Flaška <:flaska:807228132326899732> ",
                                value="`flaska`", inline=False)
                embed.add_field(name="Kahoot <:kahoot:813837093494325278> ", value="`kahoot` ", inline=False)
                embed.add_field(name="Rank systém :chart_with_upwards_trend: ", value="`rank` `leaderboard`", inline=False)
                embed.add_field(name="Minecraft server :tent: ", value="`server` ", inline=False)
                embed.add_field(name=f"Ekonomika {Callouts().emote} ",
                                value="`daily` `money` `inventory` `hunt` `send` `shop` `kviz` `sell` `prices` ",
                                inline=False)
                embed.add_field(name="Hudba :notes: ", value="`join` `leave` `play` `skip` `pause` `resume`",
                                inline=False)
                embed.add_field(name="Osu! <:osu:917383973984940072> ", value="`osu` `pp`",
                                inline=False)
                embed.set_footer(text="Pro help s jakýmkoli commandem napiš !help [command]")
                await ctx.send(embed=embed)
            elif command not in command_names_list:
                await ctx.send('Tenhle command neexistuje')

    @commands.command(help='Ukáže náhodnou čerstvou zprávu ze světa.', usage='!news')
    async def news(self, ctx):
        f = requests.get('https://newsapi.org/v2/top-headlines?country=cz&apiKey={}'.format(os.getenv('NEWS_TOKEN')))
        news = f.json()
        await ctx.send(news['articles'][random.choice(range(0, len(news['articles'])))]['title'])
def setup(client):
    client.add_cog(Funkce(client))
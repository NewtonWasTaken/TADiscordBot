import discord
from discord.ext import commands
from google_trans_new import google_translator
from discord import app_commands
from discord.utils import get
import requests
import os
import random
from callouts import Callouts
translator = google_translator()
class Funkce(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello from private command!")


    @app_commands.command(name="shrug",description='Nikdy nevíš')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def shrug(self, interaction):
        await interaction.response.send_message('¯\_(ツ)_/¯')

    @app_commands.command(description='Nezobrazí ping bota')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def ping(self, interaction):
        await interaction.response.send_message('Pong!')

    @app_commands.command(description='to je opravdu yum')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def yum(self, interaction):
        await interaction.response.send_message('yim yum')

    @app_commands.command(description='Zobrazí ping bota')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def pong(self, interaction):
        await interaction.response.send_message(f'Nemyslel jsi ping? {round(self.client.latency * 1000)}ms')

    @app_commands.command(description='Zavolá bajs na kompet')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def kompet(self, interaction):
        await interaction.response.send_message(
            '<@621353544490024961> , <@551426822299189259>, <@621701863821148166>, <@558659043833675806> pojďte hrát!')

    @app_commands.command(description=f'Ukáže {Callouts().name} Coin zblízka')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def emote(self, interaction):
        await interaction.response.send_message(f'{Callouts().emote}')

    @app_commands.command(description='Kdo vyrobil bota?')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def credit(self, interaction):
        embed = discord.Embed(
            title="Credits",
            description=
            "Tohoto bota vytvořil: <@551426822299189259> . ",
            color=0x14db3c)
        embed.set_thumbnail(
            url=self.client.user.avatar_url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description='Ukáže náhodnou čerstvou zprávu ze světa.')
    @app_commands.guilds(discord.Object(id=806808047509831700))
    async def news(self, interaction):
        f = requests.get('https://newsapi.org/v2/top-headlines?country=cz&apiKey={}'.format(os.getenv('NEWS_TOKEN')))
        news = f.json()
        await interaction.response.send_message(news['articles'][random.choice(range(0, len(news['articles'])))]['title'])

async def setup(client):
    await client.add_cog(Funkce(client))
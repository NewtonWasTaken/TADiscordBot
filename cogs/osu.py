import discord
import os
from discord.ext import commands
import random
import pymongo
import requests
import json

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
osu_database = mongo_client['TABOT']['osu']

class Osu(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def pp(self, ctx):
        osu_stat = osu_database.find_one({'id': str(ctx.author.id)})
        if osu_stat == None:
            embed = discord.Embed(title="Osu Propojení s Discordem",
                                  description="Návod na propojení Osu! účtu s Discordem", color=0xe6649e)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/806808047509831703/917191182633824306/768px-Osu21Logo_28201529.png")
            embed.add_field(name="1. ", value='Jdi na https://osu.ppy.sh/', inline=False)
            embed.add_field(name="2. ", value='Přihlaš se na svůj osu účet', inline=False)
            embed.add_field(name="3. ", value='Běž do nastavení', inline=False)
            embed.add_field(name="4. ", value='Zde zadej svůj nick na Discordu: ', inline=False)
            embed.set_image(
                url="https://media.discordapp.net/attachments/806808047509831703/917189198212104262/Discord-Tutorial.png")
            embed.set_footer(text="Nakonec dej příkaz !osu auth *tvůj nick v osu*")
            await ctx.send(embed=embed)
        else:
            await get_token()
            f = requests.get(f'https://osu.ppy.sh/api/v2/users/{osu_stat["id_osu"]}/osu', headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
            data = f.json()
            print(data)
            await ctx.send(f'Tvoje pp je {data["statistics"]["pp"]}')



def setup(client):
    client.add_cog(Osu(client))





async def get_token():
    data = {"client_id": 11378, "client_secret": "KdRTjzG0tlEOmVrNNX2LIDgmNyu6bZs6O4lNMKHr",
            "grant_type": "client_credentials", "scope": "public"}
    f = requests.post('https://osu.ppy.sh/oauth/token', data=data)
    token_data = f.json()
    if token_data['access_token'] != os.getenv('OSU_TOKEN'):
        os.environ['OSU_TOKEN'] = token_data['access_token']

async def insert_osu(user):
    newuser = {'id': str(user.id), 'server': str(server.id), 'money': 0, 'time': 0, 'time2': 0, 'time3': 0,
                'capacity': 25}
    inventory.insert_one(newuser)
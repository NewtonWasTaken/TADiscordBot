import discord
import os
import random
from discord.ext import commands
import requests
import os.path

class NSFW(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='NSFW obrázek, pouze v roomce NSFW', usage='!nsfw')
    async def nsfw(self, ctx):
        f = requests.get('https://meme-api.herokuapp.com/gimme/nsfw')
        meme = f.json()
        if ctx.channel.is_nsfw():
            await ctx.send(meme['url'])
        if not ctx.channel.is_nsfw():
            await ctx.send('Tento příkaz může být použit pouze v nsfw kanálu.')

    @commands.command(help='Hláška, nic nebezpečného', usage='!butt')
    async def butt(self, ctx):
        nsfw = open(os.path.dirname(__file__) + '/../nsfw.txt','r', encoding='utf-8')
        nsfw2 = nsfw.read().splitlines()
        print(nsfw2)
        await ctx.send(f'{random.choice(nsfw2)}')
        nsfw.close()
    @commands.command(help='Další hlášky nic nebezpečného', usage='!boob')
    async def boob(self, ctx):
        nsfw = open('nsfw.txt', 'r', encoding='utf-8')
        nsfw2 = nsfw.read().splitlines()
        await ctx.send(f'{random.choice(nsfw2)}')
        nsfw.close()



def setup(client):
    client.add_cog(NSFW(client))
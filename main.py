import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from kahoot import client
import requests



requests.packages.urllib3.disable_warnings()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!")
client.remove_command('help')

@client.event
async def on_ready():
    print('Connected to {0.user}'.format(client))
    await client.change_presence(activity= discord.Game(name='Cvičí posilko s Vaňkem | !help'))





client.load_extension('cogs.kahoot')
client.load_extension('cogs.minecraft_server')
client.load_extension('cogs.economy')
client.load_extension('cogs.ranking_system')
client.load_extension('cogs.flaska')
client.load_extension('cogs.nsfw')
client.load_extension('cogs.random')
client.load_extension('cogs.music')
client.load_extension('cogs.mainCog')
client.load_extension('cogs.utilities')




client.run(os.getenv('TOKEN'))





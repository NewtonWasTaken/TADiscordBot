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
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        command = ctx.command.qualified_name
        help = client.get_command(command).help
        usage = client.get_command(command).usage
        embed = discord.Embed(title=f"Chyba", description=f"Tady je help pro command {command}:",
                              color=0xff0000)
        embed.set_author(name="TA Discord Bot")
        embed.set_thumbnail(
            url=client.user.avatar_url)
        embed.add_field(name="Použití:", value=f"`{usage}`", inline=False)
        embed.add_field(name="Co dělá?", value=f"`{help}`", inline=True)
        embed.set_footer(text="Pro help s jakýmkoli commandem napiš !help [command]")
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Nemáš oprávnění pro tenhle command.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command nenalezen')
        pass
    if isinstance(error, commands.BadArgument):
        command = ctx.command.qualified_name
        help = client.get_command(command).help
        usage = client.get_command(command).usage
        embed = discord.Embed(title=f"Chyba", description=f"Tady je help pro command {command}:",
                              color=0xff0000)
        embed.set_author(name="TA Discord Bot")
        embed.set_thumbnail(
            url=client.user.avatar_url)
        embed.add_field(name="Použití:", value=f"`{usage}`", inline=False)
        embed.add_field(name="Co dělá?", value=f"`{help}`", inline=True)
        embed.set_footer(text="Pro help s jakýmkoli commandem napiš !help [command]")
        await ctx.send(embed=embed)
    else:

        print(error)





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





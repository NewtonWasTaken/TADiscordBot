import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, Bot
from kahoot import client
import requests
from discord_components import DiscordComponents, Button, Select, SelectOption
from callouts import Callouts
requests.packages.urllib3.disable_warnings()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!")
client.remove_command('help')

@client.event
async def on_ready():
    print('Connected to {0.user}'.format(client))
    await client.change_presence(activity= discord.Game(name='Cvičí posilko s Vaňkem | !help'))
    DiscordComponents(client)
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        command = ctx.command.qualified_name
        help = client.get_command(command).help
        usage = client.get_command(command).usage
        embed = discord.Embed(title=f"Chyba", description=f"Tady je help pro command {command}:",
                              color=0xff0000)
        embed.set_author(name=f"{Callouts().name} Discord Bot")
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
        embed.set_author(name=f"{Callouts().name} Discord Bot")
        embed.set_thumbnail(
            url=client.user.avatar_url)
        embed.add_field(name="Použití:", value=f"`{usage}`", inline=False)
        embed.add_field(name="Co dělá?", value=f"`{help}`", inline=True)
        embed.set_footer(text="Pro help s jakýmkoli commandem napiš !help [command]")
        await ctx.send(embed=embed)
    else:

        print(error)

@client.command()
async def button(ctx):
    await ctx.send('Ahoj', components = [Button(label = 'Pog', custom_id = 'button1', style= 4)])
    message = await client.wait_for("button_click", check=lambda i: i.custom_id == "button1")
    await message.send(content= "Button clicked!")


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





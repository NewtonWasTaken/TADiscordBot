import discord
from discord.ext import commands
import requests


class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='server', invoke_without_command=True)
    async def server(self, ctx):
        await ctx.send('IP našeho serveru je: TercieA.minehut.gg, Je na verzi 1.16.5')

    @server.command(name='status')
    async def status_subcommand(self, ctx):
        response = requests.get('https://api.minehut.com/server/TercieA?byName=true')
        server = response.json()
        count = server['server']['playerCount']
        maxplayers = server['server']['maxPlayers']
        if server['server']['online'] == False:
            embed = discord.Embed(title="Server je offline!", color=0xff0000)
            embed.set_author(name="Minecraft Server Tercie A")
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Připoj se na server a do chatu napiš:",
                            value="/join TercieA, pak se odpoj a počkej až se server zapne", inline=False)
            embed.set_footer(text="IP adresa serveru: TercieA.minehut.gg")
            await ctx.send(embed=embed)
        elif server['server']['online'] == True:
            embed = discord.Embed(title="Server je online!", color=0x1fd312)
            embed.set_author(name="Minecraft Server Tercie A")
            embed.set_thumbnail(
                url='https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png')
            embed.add_field(name="Počet lidí na serveru:",
                            value=f'{count} z {maxplayers} \n' + count * ' :blue_square: ' + (
                                        10 - count) * ' :white_large_square: ', inline=False)
            embed.set_footer(text="IP adresa serveru: TercieA.minehut.gg")
            await ctx.send(embed=embed)

    '''
    @server.command(name = 'start', invoke_without_command=True)
    async def start_server_subcommand(self, ctx):
      s = requests.post('https://api.minehut.com/users/login', data = login)

      r = requests.post('https://api.minehut.com/server/6037e2a8800860017c1f0ee0/start_service')
      await ctx.send('Server byl zapnut!')
      print(r.text)
      print(s.text)
    '''
def setup(client):
    client.add_cog(Minecraft(client))
import discord
from discord.ext import commands
import requests
from callouts import Callouts

class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='server', invoke_without_command=True, help='Zobrazí IP a verzi našeho serveru', usage='!server <status> \nstatus: nepovinný, ukáže jestli je server online')
    async def server(self, ctx):
        await ctx.send('IP našeho serveru je: BigyKvarta.minehut.gg, Je na verzi 1.18')

    @server.command(name='status')
    async def status_subcommand(self, ctx):
        response = requests.get('https://api.minehut.com/server/6037e2a8800860017c1f0ee0')
        server = response.json()
        count = server['server']['playerCount']
        maxplayers = 10
        print(server)
        if server['server']['online'] == False:
            embed = discord.Embed(title="Server je offline!", color=0xff0000)
            embed.set_author(name="Minecraft Server Kvarta A")
            embed.set_thumbnail(
                url=self.client.user.avatar_url)
            embed.add_field(name="Připoj se na server a do chatu napiš:",
                            value="/join BigyKvarta, pak se odpoj a počkej až se server zapne", inline=False)
            embed.set_footer(text="IP adresa serveru: BigyKvarta.minehut.gg")
            await ctx.send(embed=embed)
        elif server['server']['online'] == True:
            embed = discord.Embed(title="Server je online!", color=0x1fd312)
            embed.set_author(name="Minecraft Server BigyKvarta")
            embed.set_thumbnail(
                url=self.client.user.avatar_url)
            embed.add_field(name="Počet lidí na serveru:",
                            value=f'{count} z {maxplayers} \n' + count * ' :blue_square: ' + (
                                        10 - count) * ' :white_large_square: ', inline=False)
            embed.set_footer(text="IP adresa serveru: BigyKvarta.minehut.gg")
            await ctx.send(embed=embed)

    '''
    @server.command(name = 'start', invoke_without_command=True)
    async def start_server_subcommand(self, ctx):
        s = requests.get('https://api.minehut.com/users/login', data = data)
        r = requests.post('https://api.minehut.com/server/6037e2a8800860017c1f0ee0/start')
        print(r)
        await ctx.send('server se zapíná i guess')
        '''
def setup(client):
    client.add_cog(Minecraft(client))

    '''s = requests.post('https://api.minehut.com/users/login', data = login)

      r = requests.post('https://api.minehut.com/server/6037e2a8800860017c1f0ee0/start_service')
      await ctx.send('Server byl zapnut!')
      print(r.text)
      print(s.text)'''
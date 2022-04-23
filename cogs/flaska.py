import random
from discord.ext import commands


flaska1 = []
flaska2 = []
flaska3 = []
flaska4 = []

class Flaska(commands.Cog):
    def __init__(self, client):
        self.slient = client

    @commands.group(name='flaska', invoke_without_command=True, help='Připojí tě do hry flašky s ostatními členy Discordu.', usage='!flaska <list|start|end> \nlist: nepovinný, zobrazí list hráčů připojených ve flašce\nstart: nepovinný, vylosuje flašku z připojených lidí\nend: nepovinný, vymaže list připojených lidí a ukonči flašku')
    async def flaska(self, ctx):
        flaska1.append(f'<@{ctx.message.author.id}>')
        flaska2.append(f'{ctx.message.author.name}')
        await ctx.send(f'<@{ctx.message.author.id}>' + ' se připojil do flašky!')

    @flaska.command(name='list')
    async def list_subcommand(self, ctx):

        enoughPlayers1 = len(flaska1)
        if enoughPlayers1 <= 0:
            await ctx.send('Zatím se nikdo nepřipojil...')
        else:
            flaska4 = list(dict.fromkeys(flaska2))
            await ctx.send(', '.join(flaska4))

    @flaska.command(name='start')
    async def start_subcommand(self, ctx):
        flaska3 = list(dict.fromkeys(flaska1))
        enoughPlayers = len(flaska3)
        if enoughPlayers > 1:
            result = random.sample(flaska3, 2)
            await ctx.send(' <:flaska:807228132326899732> '.join(result) +
                           ' Pravda nebo úkol?')
        else:
            await ctx.send('Není dostatek hráčů pro zahájení flašky.')

    @flaska.command(name='end')
    async def end_subcommand(self, ctx):
        flaska1.clear()
        flaska2.clear()
        flaska3.clear()
        flaska4.clear()
        await ctx.send('Flaška byla ukončena!')

def setup(client):
    client.add_cog(Flaska(client))
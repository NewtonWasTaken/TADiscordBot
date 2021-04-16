from discord.ext import commands
from kahoot import client

bot = client()

class Kahoot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='kahoot', invoke_without_command=True, help='Připojí 1 bota se zadaným jménem na daný kahoot')
    async def kahoot(self, ctx, kahoot_number, kahoot_name):
        bot.join(kahoot_number, kahoot_name)
        await ctx.send(f'Připojil si se do kahootu: {kahoot_number}, se jménem {kahoot_name}')

    @kahoot.command(name='ddos', help='Připojí 100 botů s daným jménem na daný kahoot')
    async def ddos_subcommand(self, ctx, kahoot_number, kahoot_name):
        i = 0
        await ctx.send(f'Úspěšně připojeno 100 botů na {kahoot_number}')
        while i < 100:
            name = f'{kahoot_name}{i}'
            bot.join(kahoot_number, name)
            i = i + 1

def setup(client):
    client.add_cog(Kahoot(client))
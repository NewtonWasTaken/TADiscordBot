import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='blacklist')
    @has_permissions(administrator=True)
    async def _blacklist(self, ctx, id):
        f = open('blacklist.txt', 'a', encoding='utf-8')
        s = open('blacklist.txt', 'r', encoding='utf-8')
        blacklist = s.read().lower().splitlines()
        if id in blacklist:
            embed = discord.Embed(title="TA Discord bot", color=0xfc0303)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Oh no...", value="ID už je blacklistnuté", inline=False)
            await ctx.send(embed=embed)
        elif id not in blacklist:
            f.write(f'\n{id}')
            embed = discord.Embed(title="TA Discord bot", color=0x12e60f)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Nice!", value=f"ID: {id} bylo blacklistnuto!", inline=False)
            await ctx.send(embed=embed)
        f.close()
        s.close()

    @_blacklist.error
    async def blacklist_error(self, ctx, error):
        await ctx.send('Nemáš permise na tenhle command!')

def setup(client):
    client.add_cog(Utilities(client))
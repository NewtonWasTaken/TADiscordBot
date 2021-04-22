import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import time

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='blacklist', help='Blacklistne song pro play command. Potřebuješ oprávnění Spravovat role.', usage='!blacklist [id_songu_youtube]')
    @has_permissions(manage_roles=True)
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
    @commands.command(help='Kickne uživatele ze serveru, Potřebuješ oprávnění Vyhodit člena.', usage='!kick [uživatel] (důvod-nepovinný)')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='žádný reason'):
        await ctx.send(f'Kicknut {member.mention}. Reason: {reason}')
        await member.kick(reason=reason)

    @commands.command(help='Mutne daného člověka. Potřebuješ oprávnění Zabanovat člena.', usage='!mute [uživatel] (reason-nepovinný)')
    @has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason='žádný reason'):
        role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f'Uživatel {member.mention} byl mutnut. Reason: {reason}')
        else:
            await ctx.send(f'Uživatel {member.mention} už je mutnut')

    @commands.command(help='Unmutne daného člověka. Potřebuješ oprávnění Zabanovat člena.',
                      usage='!unmute [uživatel]')
    @has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
        if role not in member.roles:
            await ctx.send(f'Uživatel {member.mention} není mutnut')
        else:
            await member.remove_roles(role)
            await ctx.send(f'Uživatel {member.mention} byl odmutnut.')
    @commands.command(help='Zabanuje daného člověka. Potřebuješ Oprávnění Zabanovat člena.', usage='!ban [uživatel] [reason]')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason='žádný reason'):
        await member.ban(reason=reason)
        await ctx.send(f'Uživatel {member.mention} byl zabanován, Reason: {reason}')

    @commands.command(help='Smaže určitý počet zpráv', usage='!clear [počet zpráv]')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, count):
        await ctx.channel.purge(limit=int(count))
        await ctx.send(f'Smazáno {count} zpráv :white_check_mark:')

def setup(client):
    client.add_cog(Utilities(client))
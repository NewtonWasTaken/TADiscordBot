import os

import discord
import pymongo
from discord.ext import commands
from discord.ext.commands import has_permissions

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
storage = mongo_client['TABOT']['storage']

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='blacklist', help='Blacklistne song pro play command. Potřebuješ oprávnění Spravovat role.', usage='!blacklist [id_songu_youtube]')
    @has_permissions(manage_roles=True)
    async def _blacklist(self, ctx, id):
        blacklist = storage.find_one({'id': '1'})
        if id in blacklist['links']:
            embed = discord.Embed(title="TA Discord bot", color=0xfc0303)
            embed.set_thumbnail(
                url=self.client.user.avatar_url)
            embed.add_field(name="Oh no...", value="ID už je blacklistnuté", inline=False)
            await ctx.send(embed=embed)
        elif id not in blacklist['links']:
            blacklist['links'].append(id)
            storage.update_one({'id': '1'}, {'$set': {'links': blacklist['links']}})
            embed = discord.Embed(title="TA Discord bot", color=0x12e60f)
            embed.set_thumbnail(
                url=self.client.user.avatar_url)
            embed.add_field(name="Nice!", value=f"ID: {id} bylo blacklistnuto!", inline=False)
            await ctx.send(embed=embed)
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
            await member.edit(mute=True)
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
            await member.edit(mute=False)
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
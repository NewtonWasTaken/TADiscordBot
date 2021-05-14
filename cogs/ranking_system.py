import discord
import os
from discord.ext import commands
import pymongo
import asyncio

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
users = mongo_client['TABOT']['users']

class Ranking(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        self.update_data(message.author, message.guild)
        self.add_xp(message.author, 20, message.guild)
        self.level_up(message.author, message.guild)


    @commands.command(help='Ukáže tvůj rank.', usage='!rank (uživatel-nepovinný)')
    async def rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        server = ctx.message.guild
        stats = users.find_one({'id': str(member.id), 'server': str(server.id)})
        if stats == None:
            embed = discord.Embed(title="Rank", description="Jméno člena: {}".format(member.mention), color=0x084be7)
            embed.add_field(name="XP:", value='0/16 XP', inline=True)
            embed.add_field(name="Level:", value='1', inline=True)
            embed.add_field(name="1                                                           2",
                            value=10 * ' :white_large_square: ', inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)

        else:
            lvl_end = stats['level'] + 1
            lvl = stats['level']
            exp = stats['xp']

            finish = lvl_end ** (1 / (1 / 4))
            finish2 = lvl ** (1 / (1 / 4))
            finish3 = finish - finish2
            exp2 = exp - finish2
            boxes = finish3 / 10
            boxes1 = exp2 / boxes

            list = []
            id = []
            l = 1
            for i in users.find({'server': str(ctx.guild.id)}):
                list.append(i)
            list.sort(reverse=True, key=sort_func)
            for i in list:
                id.append(i['id'])



            embed = discord.Embed(title="Rank", description="Jméno člena: {}".format(member.mention), color=0x084be7)
            embed.add_field(name="XP:", value=f'{exp} / {int(finish)} XP', inline=True)
            embed.add_field(name="Level:", value=lvl, inline=True)
            embed.add_field(name="Rank:", value=f'# {int(id.index(str(member.id)) + 1)}', inline=True)
            embed.add_field(name=f"{lvl}                                                                {lvl_end}",
                            value=int(boxes1) * ' :blue_square: ' + (10 - int(boxes1)) * ' :white_large_square: ',
                            inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(help='Ukáže tabulku podle xp na serveru.', usage='!leaderboard')
    async def leaderboard(self, ctx):
        list = []
        id = []
        xp = []
        l=1
        rank = []
        for i in users.find({'server': str(ctx.guild.id)}):
            list.append(i)
        list.sort(reverse=True, key=sort_func)
        for i in list:
            id.append(i['id'])
            xp.append(i['xp'])
            rank.append(l)
            l+=1
        embed = discord.Embed(title='Leaderboard',description='Tady vidíš kolikáty jsi v počtu odeslaných zpráv, za každou zprávu je 20xp:', color=0x1926e1)
        embed.add_field(name='Tabulka' ,value="\n".join("{}. - <@{}> - {} XP".format(x, y, z) for x, y, z in zip(rank,id, xp) ), inline=False)
        embed.set_thumbnail(url=
                            self.client.user.avatar_url)
        await ctx.send(embed=embed)





    def update_data(self, user, server):
        stats = users.find_one({'id': str(user.id), 'server': str(server.id)})
        if stats == None:
            newuser = {'id': str(user.id), 'server': str(server.id), 'xp': 0, 'level': 1}
            users.insert_one(newuser)

    def add_xp(self, user, xp, server):
        stats = users.find_one({'id': str(user.id), 'server': str(server.id)})
        add = stats['xp'] + xp
        users.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {'xp': add}})

    def level_up(self, user, server):
        stats = users.find_one({'id': str(user.id), 'server': str(server.id)})

        if server.id == 693009303526703134:
            channel = self.client.get_channel(826042384558063617)
            lvl_end = stats['level'] + 1
            exp = stats['xp']
            finish = lvl_end ** (1 / (1 / 4))
        if server.id == 806808047509831700:
            channel = self.client.get_channel(807246401607827536)
            lvl_end = stats['level'] + 1
            exp = stats['xp']
            finish = lvl_end ** (1 / (1 / 4))

        if exp >= finish:
            update_level = lvl_end
            users.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {'level': update_level}})
            asyncio.run_coroutine_threadsafe(channel.send('{} má level {}'.format(user.mention, lvl_end)), self.client.loop)

def setup(client):
    client.add_cog(Ranking(client))
def sort_func(e):
        return e['xp']



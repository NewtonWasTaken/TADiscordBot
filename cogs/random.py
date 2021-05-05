import discord
import random
from discord.ext import commands
import requests
import os
import pymongo

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
storage = mongo_client['TABOT']['storage']
pp = ['8D', '8=D', '8==D', '8===D', '8====D', '8=====D', '8======D', '8=======D', '8========D']
life = ['Žiju!', 'Nežiju!']
distribution = [.9, .1]

class Random(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        f = requests.get('https://meme-api.herokuapp.com/gimme/meme')
        meme = f.json()
        if meme['nsfw'] == False:
            await ctx.send(meme['url'])
        else:
            meme()

    @commands.group(name='student', invoke_without_command=True, help='Zobrazí náhodnou hlášku studenta z naší třídy', usage='!student <add> [hláška] \nadd: nepovinný, přidá další hlášku')
    async def student(self, ctx):
        student_storage = storage.find_one({'id': '2'})
        student = random.choice(student_storage['student'])
        await ctx.send(student)

    @student.command(name='add')
    async def student_insert(self, ctx, *, hlaska):
        roast_storage = storage.find_one({'id': '2'})
        roasts = roast_storage['student']
        if hlaska.lower() in roasts:
            embed = discord.Embed(title="TA Discord bot", color=0xfc0303)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Oh no...", value="Hláška se už nachází v seznamu...", inline=False)
            await ctx.send(embed=embed)
        elif hlaska.lower() not in roasts:
            roasts.append(hlaska)
            storage.update_one({'id': '2'}, {'$set': {'student': roasts}})
            embed = discord.Embed(title="TA Discord bot", color=0x12e60f)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Nice!", value=f"Hláška: '{hlaska}' byla přidána do seznamu!", inline=False)
            await ctx.send(embed=embed)

    @commands.command(help='Testovací zpráva jestli bot žije', usage='!status')
    async def status(self, ctx):
        rng = random.choices(life, distribution)
        await ctx.send(''.join(rng))

    @commands.command(help='Napíše na kolik % jsi gay', usage='!howgay (uživatel-nepovinný)')
    async def howgay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        await ctx.send(
            f'{member.mention} jsi na {random.randrange(1, 100, 3)}% gay. <:rainbow_flag:811896666848100363>')

    @commands.command(help='Napíše koho simpíš a na kolik %.', usage='!simp (uživatel-nepovinný)')
    async def simp(self, ctx, member: discord.Member = None):
        input = open(os.path.dirname(__file__) + '/../classsimp.txt', 'r', encoding='utf-8')
        ourclasssimp = [str(number) for number in input.readline().split(',')]

        if member is None:
            member = ctx.message.author
        await ctx.send(
            f'{member.mention} simpíš{random.choice(ourclasssimp)} na {random.randrange(1, 100, 3)}%. <:SIMP:782941806244921354>')
        input.close()

    @commands.command(name='pp', help='Ukáže jak máš dlouhý pp.', usage='!pp (uživatel-nepovinný)')
    async def delka(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        await ctx.send(f'{member.mention} máš {random.choice(pp)}')

    @commands.command(help='Ukáže náhodného člověka z naší třídy.', usage='!rng')
    async def rng(self, ctx):
        input2 = open(os.path.dirname(__file__) + '/../class.txt', 'r', encoding='utf-8')
        ourclass = [str(number2) for number2 in input2.readline().split(',')]
        await ctx.send(f'Náhodný člověk z naší třídy:{random.choice(ourclass)}')
        input2.close()

    @commands.group(name='ucitel', invoke_without_command=True, help='Ukáže náhodnou hlášku učitele.', usage='!ucitel <add> (hláška) \nadd: nepovinný, přidá další hlášku')
    async def ucitel(self, ctx):
        ucitel_storage = storage.find_one({'id': '3'})
        ucitel = ucitel_storage['ucitel']
        await ctx.send(random.choice(ucitel))

    @ucitel.command(name='add')
    async def ucitel_insert(self, ctx, *, hlaska):
        roasts_storage = storage.find_one({'id': '3'})
        roasts = roasts_storage['ucitel']
        if hlaska.lower() in roasts:
            embed = discord.Embed(title="TA Discord bot", color=0xfc0303)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Oh no...", value="Hláška se už nachází v seznamu...", inline=False)
            await ctx.send(embed=embed)
        elif hlaska.lower() not in roasts:
            roasts.append(hlaska)
            storage.update_one({'id': '3'}, {'$set': {'ucitel': roasts}})
            embed = discord.Embed(title="TA Discord bot", color=0x12e60f)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Nice!", value=f"Hláška: '{hlaska}' byla přidána do seznamu!", inline=False)
            await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Random(client))
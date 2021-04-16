import discord
import random
from discord.ext import commands
import requests
import os


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

    @commands.group(name='student', invoke_without_command=True)
    async def student(self, ctx):
        roasty = open(os.path.dirname(__file__) + '/../roasts.txt', 'r', encoding='utf-8')
        roasty2 = roasty.read().splitlines()
        student = random.choice(roasty2)
        await ctx.send(student)
        roasty.close()

    @student.command(name='add')
    async def student_insert(self, ctx, *, hlaska):
        f = open(os.path.dirname(__file__) + '/../roasts.txt', 'a', encoding='utf-8')
        s = open(os.path.dirname(__file__) + '/../roasts.txt', 'r', encoding='utf-8')
        roasts = s.read().lower().splitlines()
        if hlaska.lower() in roasts:
            embed = discord.Embed(title="TA Discord bot", color=0xfc0303)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Oh no...", value="Hláška se už nachází v seznamu...", inline=False)
            await ctx.send(embed=embed)
        elif hlaska.lower() not in roasts:
            f.write(f'\n{hlaska}')
            embed = discord.Embed(title="TA Discord bot", color=0x12e60f)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Nice!", value=f"Hláška: '{hlaska}' byla přidána do seznamu!", inline=False)
            await ctx.send(embed=embed)
        f.close()
        s.close()

    @commands.command()
    async def status(self, ctx):
        rng = random.choices(life, distribution)
        await ctx.send(''.join(rng))

    @commands.command()
    async def howgay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        await ctx.send(
            f'{member.mention} jsi na {random.randrange(1, 100, 3)}% gay. <:rainbow_flag:811896666848100363>')

    @commands.command()
    async def simp(self, ctx, member: discord.Member = None):
        input = open(os.path.dirname(__file__) + '/../classsimp.txt', 'r', encoding='utf-8')
        ourclasssimp = [str(number) for number in input.readline().split(',')]

        if member is None:
            member = ctx.message.author
        await ctx.send(
            f'{member.mention} simpíš{random.choice(ourclasssimp)} na {random.randrange(1, 100, 3)}%. <:SIMP:782941806244921354>')
        input.close()

    @commands.command(name='pp')
    async def delka(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        await ctx.send(f'{member.mention} máš {random.choice(pp)}')

    @commands.command()
    async def rng(self, ctx):
        input2 = open(os.path.dirname(__file__) + '/../class.txt', 'r', encoding='utf-8')
        ourclass = [str(number2) for number2 in input2.readline().split(',')]
        await ctx.send(f'Náhodný člověk z naší třídy:{random.choice(ourclass)}')
        input2.close()

    @commands.group(name='ucitel', invoke_without_command=True)
    async def ucitel(self, ctx):
        ucitel = open(os.path.dirname(__file__) + '/../ucitel.txt', 'r', encoding='utf-8')
        ucitel2 = ucitel.read().splitlines()
        await ctx.send(f'{random.choice(ucitel2)}')
        ucitel.close()

    @ucitel.command(name='add')
    async def ucitel_insert(self, ctx, *, hlaska):
        f = open(os.path.dirname(__file__) + '/../ucitel.txt', 'a', encoding='utf-8')
        s = open(os.path.dirname(__file__) + '/../ucitel.txt', 'r', encoding='utf-8')
        roasts = s.read().lower().splitlines()
        if hlaska.lower() in roasts:
            embed = discord.Embed(title="TA Discord bot", color=0xfc0303)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Oh no...", value="Hláška se už nachází v seznamu...", inline=False)
            await ctx.send(embed=embed)
        elif hlaska.lower() not in roasts:
            f.write(f'\n{hlaska}')
            embed = discord.Embed(title="TA Discord bot", color=0x12e60f)
            embed.set_thumbnail(
                url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Nice!", value=f"Hláška: '{hlaska}' byla přidána do seznamu!", inline=False)
            await ctx.send(embed=embed)
        f.close()
        s.close()
def setup(client):
    client.add_cog(Random(client))
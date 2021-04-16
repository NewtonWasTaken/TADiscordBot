import discord
from discord.ext import commands
from google_trans_new import google_translator
from discord.utils import get
translator = google_translator()


class Funkce(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Nikdy nevíš')
    async def shrug(self, ctx):
        await ctx.send('¯\_(ツ)_/¯')

    @commands.command(help='Zobrazí ping bota')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(help='to je opravdu yum')
    async def yum(self, ctx):
        await ctx.send('yim yum')

    @commands.command()
    async def pong(self, ctx):
        await ctx.send(f'Nemyslel jsi ping? {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def kompet(self, ctx):
        await ctx.send(
            '<@621353544490024961> , <@551426822299189259>, <@621701863821148166>, <@558659043833675806> pojďte hrát!')

    @commands.command()
    async def emote(self, ctx):
        await ctx.send('<:TACoin:806882594519515146>')

    @commands.command()
    async def credit(self, ctx):
        embed = discord.Embed(
            title="Credits",
            description=
            "Tohoto bota vytvořil: <@551426822299189259> . ",
            color=0x14db3c)
        embed.set_thumbnail(
            url="https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def translate(self, ctx, *, text):
        trans_text = text
        result = translator.translate(trans_text, lang_tgt='cs')
        await ctx.send(result)

    @commands.command()
    async def help(self, ctx):
            embed = discord.Embed(
                title="Help",
                description=
                "Pokud potřebuješ s čimkoli pomoct, tady jsou všechny příkazy:",
                color=0xff0000)
            embed.set_author(name="TA Discord Bot")
            embed.set_thumbnail(
                url=
                "https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png"
            )
            embed.add_field(name="Funkce :gear: ", value="`ping` `pong` `status`", inline=False)
            embed.add_field(name="Vlastní commandy <:TACoin:806882594519515146> ",
                            value="`yum` `emote` `kompet` `credit` `shrug` `translate`", inline=False)
            embed.add_field(name="Random věci :slot_machine: ",
                            value="`ucitel` `howgay` `simp` `rng` `pp` `meme` `student` \n`ucitel add` `student add`",
                            inline=False)
            embed.add_field(name="NSFW :underage: ", value="`boob` `butt` `nsfw`", inline=False)
            embed.add_field(name="Flaška <:flaska:807228132326899732> ",
                            value="`flaska` `flaska start` `flaska list` `flaska end` ", inline=False)
            embed.add_field(name="Kahoot <:kahoot:813837093494325278> ", value="`kahoot` `kahoot ddos` ", inline=False)
            embed.add_field(name="Rank systém :chart_with_upwards_trend: ", value="`rank` ", inline=False)
            embed.add_field(name="Minecraft server :tent: ", value="`server` `server status` ", inline=False)
            embed.add_field(name="Ekonomika <:TACoin:806882594519515146> ",
                            value="`daily` `money` `inventory` `hunt` `send` `shop` `kviz` `kviz cz` `sell` `buy` `prices` ",
                            inline=False)
            embed.add_field(name="Hudba :notes: ", value="`join` `leave` `play **url**` `skip` `pause` `resume`",
                            inline=False)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Funkce(client))
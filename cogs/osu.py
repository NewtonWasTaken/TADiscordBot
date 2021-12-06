import discord
import os
from discord.ext import commands
import random
import pymongo
import requests
import json
from datetime import datetime
from discord_components import DiscordComponents, Button, Select, SelectOption

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
osu_database = mongo_client['TABOT']['osu']

class Osu(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(help="Napíše tvoje PP ve hře Osu!", usage="!pp")
    async def pp(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        osu_stat = osu_database.find_one({'id': str(member.id)})
        if osu_stat == None:
            await ctx.send(':x: Tento člověk nemá propojen Osu! účet s Discordem. Pokud jsi to ty dej `!osu auth **tvůj nick v Osu!**`')
        elif member == ctx.author:
            await get_token()
            f = requests.get(f'https://osu.ppy.sh/api/v2/users/{osu_stat["osu_id"]}/osu',
                             headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
            data = f.json()
            await ctx.send(f'Tvoje pp je {data["statistics"]["pp"]} :eggplant:')
        else:
            await get_token()
            f = requests.get(f'https://osu.ppy.sh/api/v2/users/{osu_stat["osu_id"]}/osu',
                             headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
            data = f.json()
            await ctx.send(f'PP uživatele {member.mention}: {data["statistics"]["pp"]} :eggplant:')
    @commands.group(name='osu', invoke_without_command=True, help="Ukáže tvůj osu profil", usage= "!osu <auth|unauth|inspect> [jmeno] \nauth: nepovinný, propojí tvůj Discord s účtem Osu!\nunauth: nepovinný, odpojí tvůj Discord od účtu Osu!\ninspect: nepovinný, zobrazí zadaný profil ve hře Osu!")
    async def osu(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        osu_stat = osu_database.find_one({'id': str(member.id)})
        if osu_stat == None:
            await ctx.send(':x: Tento člověk nemá propojen Osu! účet s Discordem. Pokud jsi to ty dej `!osu auth **tvůj nick v Osu!**`')
        else:
            await get_token()
            x = requests.get(f"https://osu.ppy.sh/api/v2/users/{osu_stat['osu_id']}/beatmapsets/most_played", headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
            graveyard = x.json()
            f = requests.get(f'https://osu.ppy.sh/api/v2/users/{osu_stat["osu_id"]}/osu',
                             headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
            data = f.json()
            embed = discord.Embed(title=data['username'],
                                  description=f'{data["country"]["name"]} :flag_{data["country_code"].lower()}:', color=0xe6649e)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url=data["avatar_url"])
            if data["is_online"] == True:
                datum = datetime.fromisoformat(data['join_date'])
                embed.add_field(name="Online: <:online:917365516342030356>",
                                value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}',
                                inline=False)
            else:
                datum = datetime.fromisoformat(data['join_date'])
                embed.add_field(name="Offline: <:offline:917365551435767819>",
                                value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}',
                                inline=False)
            if graveyard[0]["beatmap"]["status"] == "graveyard":
                embed.add_field(name="Nejhranější mapa",
                                value=f'<:rip:917382794970279956> {graveyard[0]["beatmapset"]["artist"]} - {graveyard[0]["beatmapset"]["title"]}',
                                inline=False)
            else:
                embed.add_field(name="Nejhranější mapa",
                                value=f'<:osu:917383973984940072> {graveyard[0]["beatmapset"]["artist"]} - {graveyard[0]["beatmapset"]["title"]}',
                                inline=False)
            embed.add_field(name="Odehraných map:",
                            value=f'<:osu:917383973984940072> {data["beatmap_playcounts_count"]}',
                            inline=False)
            embed.add_field(name="PP:",
                            value=f':eggplant: {data["statistics"]["pp"]}',
                            inline=False)
            embed.add_field(name="Přesnost:",
                            value=f'<:procento:917386466412351498> {data["statistics"]["hit_accuracy"]}',
                            inline=False)
            hours = int((data["statistics"]["play_time"] / 60)/60)
            minutes = (data["statistics"]["play_time"] / 60) - (hours * 60)
            embed.add_field(name="Odehráno hodin:",
                            value=f':alarm_clock: {hours} h {int(minutes)} min.',
                            inline=False)
            embed.add_field(name="Světové hodnocení: ",
                            value=f':globe_with_meridians: {data["statistics"]["global_ranking"]}',
                            inline=False)
            embed.add_field(name="Odkaz:",
                            value=f'[{data["username"]}](https://osu.ppy.sh/users/{data["id"]})',
                            inline=False)
            await ctx.send(embed=embed)

    @osu.command(name='auth', help="Ukáže tvůj osu profil", usage= "!osu <auth|unauth|inspect> [jmeno] \nauth: nepovinný, propojí tvůj Discord s účtem Osu!\nunauth: nepovinný, odpojí tvůj Discord od účtu Osu!\ninspect: nepovinný, zobrazí zadaný profil ve hře Osu!")
    async def osu_auth(self, ctx,*, jmeno):
        osu_stat = osu_database.find_one({'id': str(ctx.author.id)})
        if osu_stat == None:
            osu_try_name = osu_database.find_one({'name': jmeno})
            if osu_try_name == None:
                await get_token()
                f = requests.get(f'https://osu.ppy.sh/api/v2/users/{jmeno}',
                                 headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
                data = f.json()
                try:
                    embed = discord.Embed(title=data['username'],
                                          description=f'{data["country"]["name"]} :flag_{data["country_code"].lower()}:',
                                          color=0xe6649e)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(
                        url=data["avatar_url"])
                    if data["is_online"] == True:
                        datum = datetime.fromisoformat(data['join_date'])
                        embed.add_field(name="Online: <:online:917365516342030356>", value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}', inline=False)
                    else:
                        datum = datetime.fromisoformat(data['join_date'])
                        embed.add_field(name="Offline: <:offline:917365551435767819>", value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}', inline=False)
                    hours = int((data["statistics"]["play_time"] / 60) / 60)
                    minutes = (data["statistics"]["play_time"] / 60) - (hours * 60)
                    embed.add_field(name="Odehráno hodin:",
                                    value=f':alarm_clock: {hours} h {int(minutes)} min.',
                                    inline=False)
                    embed.add_field(name="Odkaz:",
                                    value=f'[{data["username"]}](https://osu.ppy.sh/users/{data["id"]})',
                                    inline=False)
                    embed.add_field(name="Je tohle tvůj účet?",
                                    value=f'Pokud ano zareaguj níže:',
                                    inline=False)
                    await ctx.send(embed=embed, components = [[Button(label = 'Ano', custom_id = 'button1', style= 3), Button(label = 'Ne', custom_id = 'button2', style= 4)]])

                    def check(m):
                        return m.user == ctx.author
                    user_full_name = ctx.author.name +'#'+ ctx.author.discriminator
                    instance = await self.client.wait_for('button_click', check=check)
                    if instance.component.id == 'button1' and user_full_name == data["discord"]:
                        await instance.respond(type=4,
                                               content=f":white_check_mark: Účet **{jmeno}** propojen",
                                               ephemeral=False)
                        await insert_osu(ctx.author, data['id'], data['username'])
                    elif instance.component.id == 'button1' and user_full_name != data["discord"]:
                        await instance.respond(type=4,
                                               content=f":x: Tento Účet Ti nepatří nebo ho nemáš propojen",
                                               ephemeral=False)
                        embed = discord.Embed(title="Osu Propojení s Discordem",
                                              description="Návod na propojení Osu! účtu s Discordem", color=0xe6649e)
                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/806808047509831703/917191182633824306/768px-Osu21Logo_28201529.png")
                        embed.add_field(name="1. ", value='Jdi na https://osu.ppy.sh/', inline=False)
                        embed.add_field(name="2. ", value='Přihlaš se na svůj osu účet', inline=False)
                        embed.add_field(name="3. ", value='Běž do nastavení', inline=False)
                        embed.add_field(name="4. ", value='Zde zadej svůj nick na Discordu: ', inline=False)
                        embed.set_image(
                            url="https://media.discordapp.net/attachments/806808047509831703/917189198212104262/Discord-Tutorial.png")
                        embed.set_footer(text="Nakonec dej příkaz `!osu auth **tvůj nick v Osu!**`")
                        await ctx.send(embed=embed)
                except:
                    await ctx.send(f':x: Účet **{jmeno}** neexistuje')

                else:
                    await instance.respond(type=4, content= ":x: Zrušeno", ephemeral=False)
            else:
                await ctx.send(':x: Tento účet už si propojil někdo jiný! Proč chceš krást?')
        else:
            await ctx.send(':white_check_mark: Už máš propojený Osu! účet s Discordem')
    @osu.command(name='inspect', help="Ukáže tvůj osu profil", usage= "!osu <auth|unauth|inspect> [jmeno] \nauth: nepovinný, propojí tvůj Discord s účtem Osu!\nunauth: nepovinný, odpojí tvůj Discord od účtu Osu!\ninspect: nepovinný, zobrazí zadaný profil ve hře Osu!")
    async def osu_inspect(self, ctx, *, jmeno):
        try:
            await get_token()
            f = requests.get(f'https://osu.ppy.sh/api/v2/users/{jmeno}',
                             headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
            data = f.json()
            x = requests.get(f"https://osu.ppy.sh/api/v2/users/{data['id']}/beatmapsets/most_played",
                             headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
            graveyard = x.json()
            embed = discord.Embed(title=data['username'],
                                  description=f'{data["country"]["name"]} :flag_{data["country_code"].lower()}:',
                                  color=0xe6649e)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url=data["avatar_url"])
            if data["is_online"] == True:
                datum = datetime.fromisoformat(data['join_date'])
                embed.add_field(name="Online: <:online:917365516342030356>",
                                value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}',
                                inline=False)
            else:
                datum = datetime.fromisoformat(data['join_date'])
                embed.add_field(name="Offline: <:offline:917365551435767819>",
                                value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}',
                                inline=False)
            if graveyard[0]["beatmap"]["status"] == "graveyard":
                embed.add_field(name="Nejhranější mapa",
                                value=f'<:rip:917382794970279956> {graveyard[0]["beatmapset"]["artist"]} - {graveyard[0]["beatmapset"]["title"]}',
                                inline=False)
            else:
                embed.add_field(name="Nejhranější mapa",
                                value=f'<:osu:917383973984940072> {graveyard[0]["beatmapset"]["artist"]} - {graveyard[0]["beatmapset"]["title"]}',
                                inline=False)
            embed.add_field(name="Odehraných map:",
                            value=f'<:osu:917383973984940072> {data["beatmap_playcounts_count"]}',
                            inline=False)
            embed.add_field(name="PP:",
                            value=f':eggplant: {data["statistics"]["pp"]}',
                            inline=False)
            embed.add_field(name="Přesnost:",
                            value=f'<:procento:917386466412351498> {data["statistics"]["hit_accuracy"]}',
                            inline=False)
            hours = int((data["statistics"]["play_time"] / 60) / 60)
            minutes = (data["statistics"]["play_time"] / 60) - (hours * 60)
            embed.add_field(name="Odehráno hodin:",
                            value=f':alarm_clock: {hours} h {int(minutes)} min.',
                            inline=False)
            embed.add_field(name="Světové hodnocení: ",
                            value=f':globe_with_meridians: {data["statistics"]["global_ranking"]}',
                            inline=False)
            embed.add_field(name="Odkaz:",
                            value=f'[{data["username"]}](https://osu.ppy.sh/users/{data["id"]})',
                            inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send(f':x: Účet **{jmeno}** neexistuje')
    @osu.command(name='unauth', help="Ukáže tvůj osu profil", usage= "!osu <auth|unauth|inspect> [jmeno] \nauth: nepovinný, propojí tvůj Discord s účtem Osu!\nunauth: nepovinný, odpojí tvůj Discord od účtu Osu!\ninspect: nepovinný, zobrazí zadaný profil ve hře Osu!")
    async def osu_unauth(self, ctx):
        osu_stat = osu_database.find_one({'id': str(ctx.author.id)})
        if osu_stat != None:
                await get_token()
                f = requests.get(f'https://osu.ppy.sh/api/v2/users/{osu_stat["osu_id"]}/osu',
                                 headers={'Authorization': f'Bearer {os.getenv("OSU_TOKEN")}'})
                data = f.json()
                embed = discord.Embed(title=data['username'],
                                          description=f'{data["country"]["name"]} :flag_{data["country_code"].lower()}:',
                                          color=0xe6649e)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(
                        url=data["avatar_url"])
                if data["is_online"] == True:
                    datum = datetime.fromisoformat(data['join_date'])
                    embed.add_field(name="Online: <:online:917365516342030356>",
                                        value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}',
                                        inline=False)
                else:
                    datum = datetime.fromisoformat(data['join_date'])
                    embed.add_field(name="Offline: <:offline:917365551435767819>",
                                        value=f'Datum připojení: \n{datum.strftime(":calendar_spiral: %d. %m. %Y  :timer: %H:%M")}',
                                        inline=False)
                hours = int((data["statistics"]["play_time"] / 60) / 60)
                minutes = (data["statistics"]["play_time"] / 60) - (hours * 60)
                embed.add_field(name="Odehráno hodin:",
                                    value=f':alarm_clock: {hours} h {int(minutes)} min.',
                                    inline=False)
                embed.add_field(name="Odkaz:",
                                    value=f'[{data["username"]}](https://osu.ppy.sh/users/{data["id"]})',
                                    inline=False)
                embed.add_field(name="Opravdu chceš odpojit tenhle účet?",
                                    value=f'Pokud ano zareaguj níže:',
                                    inline=False)
                await ctx.send(embed=embed, components=[[Button(label='Ano', custom_id='button1', style=3),
                                                             Button(label='Ne', custom_id='button2', style=4)]])

                def check(m):
                    return m.user == ctx.author

                instance = await self.client.wait_for('button_click', check=check)
                if instance.component.id == 'button1':
                    await instance.respond(type=4,
                                               content=f":white_check_mark: Účet **{data['username']}** odpojen",
                                               ephemeral=False)
                    await delete_osu(ctx.author, data['id'])
                else:
                    await instance.respond(type=4, content=":x: Zrušeno", ephemeral=False)
        else:
            await ctx.send(':x: Nemáš propojený Osu! účet s Discordem')

def setup(client):
    client.add_cog(Osu(client))





async def get_token():
    data = {"client_id": 11378, "client_secret": os.getenv('OSU_SECRET'),
            "grant_type": "client_credentials", "scope": "public"}
    f = requests.post('https://osu.ppy.sh/oauth/token', data=data)
    token_data = f.json()
    if token_data['access_token'] != os.getenv('OSU_TOKEN'):
        os.environ['OSU_TOKEN'] = token_data['access_token']

async def insert_osu(user, osu_id, osu_name):
    newuser = {'id': str(user.id), 'osu_id': osu_id, 'osu_name': osu_name}
    osu_database.insert_one(newuser)
async def delete_osu(user, osu_id):
    delete_user = {'id': str(user.id), 'osu_id': osu_id}
    osu_database.delete_one(delete_user)
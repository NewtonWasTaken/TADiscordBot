import discord
import os
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import time
import requests
import asyncio
from google_trans_new import google_translator
import pymongo

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
users = mongo_client['TABOT']['users']
inventory = mongo_client['TABOT']['inventory']
animals = mongo_client['TABOT']['animals']

hunt_list = [':mouse:', ':hamster:', ':bear:', ':knife:', ':mammoth:', ':bird:', ':kangaroo:', ':monkey:', ':rabbit2:', ':unicorn:', '<:kalda:829322764065701889>']
sell_list = [':mouse:', ':hamster:', ':bear:', ':knife:', ':mammoth:', ':bird:', ':kangaroo:', ':monkey:', ':rabbit2:', ':unicorn:', ':archery:', ':spoon:', '<:kalda:829322764065701889>']
price_list = [50, 75, 150, 4000, 200, 500, 250, 200, 600, 5000, 17000, 45000, 0]
fail_text = ['Našel jsi :teddy_bear: hodil jsi ho do popelnice...', 'Našel jsi dva dny staré :newspaper2:, jediný co ses dozvěděl že ', 'Našel jsi :knot: Myslím že ti bude k ničemu...','Našel jsi :knife:, ale byl plastovej xd', 'Našel jsi :french_bread:, a snědl jsi ji, takže teď už nemáš nic :)','Našel jsi :bread:, a snědl jsi ho, takže teď už nemáš nic :)', 'Našel jsi :knot:, takže se konečně můžeš oběsit...']

requests.packages.urllib3.disable_warnings()
translator = google_translator()

class Ekonomika(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(name='inventory', help='Ukáže inventář', usage='!inventory (uživatel-nepovinný)')
    async def inventory_command(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      server = ctx.guild
      await coin_update(user, server)
      stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
      things = animals.find_one({'id': str(user.id), 'server': str(server.id)})
      number = []
      thing_list = []
      coins = stats['money']
      for i in sell_list:
        if i in things:
         number.append(things[i])
      for i in sell_list:
        if i in things:
         thing_list.append(str(i))
      capacity = await capacity_check(user, server)
      my_capacity = stats['capacity']


      try:
       embed=discord.Embed(title="Inventář", description="Toto je seznam věcí které máš:", color=0x1926e1)
       embed.set_author(name=user.name, icon_url= user.avatar_url)
       embed.add_field(name="Peníze", value=f"{coins} <:TACoin:806882594519515146>", inline=True)
       embed.add_field(name=f'Věci {capacity} / {my_capacity} <:otrok:824609734778421258>' , value= "\n".join("{} × {}".format(x, y) for x, y in zip(number, thing_list)) , inline=False)
       embed.set_thumbnail(url=
       'https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png')
       await ctx.send(embed=embed)
      except:
       embed=discord.Embed(title="Inventář", description="Toto je seznam věcí které máš:", color=0x1926e1)
       embed.set_author(name=user.name, icon_url= user.avatar_url)
       embed.add_field(name="Peníze", value=f"{coins} <:TACoin:806882594519515146>", inline=True)
       embed.add_field(name="Věci 0/25 <:otrok:824609734778421258>", value= 'Kde nic tu nic...' , inline=False)
       embed.set_thumbnail(url= 'https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png')
       await ctx.send(embed=embed)

    @commands.command(help='Kvíz o 100 TA Coinů. Jendou za 5 minut. Po zobrazení kvízu se odpovídá zprávou s obsahem 1-4', usage='!kviz <cz> \ncz: nepovinný, kvíz bude přeložen do češtiny')
    async def kviz(self, ctx, language=None):
        if language == None:
            language = 'en'
        user = ctx.author
        server = ctx.guild
        await coin_update(user, server)
        stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
        start = await coin_add(user, server, 'time2', 300)
        pending = 300 - (time.time() - stats['time2'])
        if start == True:
            if language == 'cz':
                f = requests.get('https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple')
                f = f.text
                f = unescape(f)
                questions = json.loads(f)
                answers = []
                x = 1
                en_question = questions['results'][0]['question']
                en_category = questions['results'][0]['category']
                en_correct = questions['results'][0]['correct_answer']
                en_incorrect = questions['results'][0]['incorrect_answers'][0]
                en_incorrect1 = questions['results'][0]['incorrect_answers'][1]
                en_incorrect2 = questions['results'][0]['incorrect_answers'][2]
                question = translator.translate(en_question, lang_tgt='cs')
                category = translator.translate(en_category, lang_tgt='cs')
                answers.append(translator.translate(en_correct, lang_tgt='cs'))
                answers.append(translator.translate(en_incorrect, lang_tgt='cs'))
                answers.append(translator.translate(en_incorrect1, lang_tgt='cs'))
                answers.append(translator.translate(en_incorrect2, lang_tgt='cs'))
                correct = translator.translate(en_correct, lang_tgt='cs')
                random.shuffle(answers)
                embed = discord.Embed(title=category, color=0x378ad7)
                embed.set_thumbnail(
                    url="https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
                embed.add_field(name=question,
                                value=f"[1] {answers[0]} \n [2] {answers[1]} \n [3] {answers[2]} \n [4] {answers[3]}",
                                inline=True)
                await ctx.send(embed=embed)
                for i in answers:
                    if i == correct:
                        number = x
                        break
                    x = x + 1

                def check(m):
                    return m.author == ctx.author and m.content.isdigit()

                try:
                    msg = await self.client.wait_for('message', timeout=10.0, check=check)
                    if msg.content == str(number):
                        await ctx.send('Správná odpověď, dostal jsi 100 <:TACoin:806882594519515146>')
                        result = stats['money'] + 100
                        inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                             {'$set': {'money': result}})
                    else:
                        await ctx.send(f'Špatná odpověď, nic jsi nedostal... Správná odpověď byla **{correct}**')
                except asyncio.TimeoutError:
                    await ctx.send(f'Nestihl jsi odpovědět, nic jsi nedostal... Správná odpověď byla **{correct}**')
            elif language == 'en':
                f = requests.get('https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple')
                f = f.text
                f = unescape(f)
                questions = json.loads(f)
                answers = []
                x = 1
                en_question = questions['results'][0]['question']
                en_category = questions['results'][0]['category']
                answers.append(questions['results'][0]['correct_answer'])
                answers.append(questions['results'][0]['incorrect_answers'][0])
                answers.append(questions['results'][0]['incorrect_answers'][1])
                answers.append(questions['results'][0]['incorrect_answers'][2])
                correct = questions['results'][0]['correct_answer']
                random.shuffle(answers)
                embed = discord.Embed(title=en_category, color=0x378ad7)
                embed.set_thumbnail(
                    url="https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
                embed.add_field(name=en_question,
                                value=f"[1] {answers[0]} \n [2] {answers[1]} \n [3] {answers[2]} \n [4] {answers[3]}",
                                inline=True)
                await ctx.send(embed=embed)
                for i in answers:
                    if i == correct:
                        number = x
                        break
                    x = x + 1

                def check2(m):
                    return m.author == ctx.author and m.content.isdigit()

                try:
                    msg = await self.client.wait_for('message', timeout=10.0, check=check2)
                    if msg.content == str(number):
                        await ctx.send('Správná odpověď, dostal jsi 100 <:TACoin:806882594519515146>')
                        result = stats['money'] + 100
                        inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                             {'$set': {'money': result}})
                    else:
                        await ctx.send(f'Špatná odpověď, nic jsi nedostal... Správná odpověď byla **{correct}**')
                except asyncio.TimeoutError:
                    await ctx.send(f'Nestihl jsi odpovědět, nic jsi nedostal...Správná odpověď byla **{correct}**')
        elif start == False:
            await ctx.send(f'Znova můžeš udělat kvíz za **{int(pending / 60)} minut {int(pending % 60)} sekund**')

    @commands.command(help='Zobrazí seznam věcí co si můžeš koupit.', usage='!shop')
    async def shop(self, ctx):
        embed = discord.Embed(title='Shop', description='Tady si můžeš kupovat různé věci :', color=0x0b49da)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(
            url='https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png')
        embed.add_field(name='[1] :knife: / 5000 <:TACoin:806882594519515146>',
                        value='Knife ti může i padnout. Zvyšuje šance na základní zvířata. S :knife: můžeš naviíc chytit :mammoth: :kangaroo: a :monkey:',
                        inline=False)
        embed.add_field(name='[2] :archery: / 20 000 <:TACoin:806882594519515146>',
                        value='Zvyšuje se šance na zvířata co můžeš chytit s :knife: Navíc můžeš chytit :bird:',
                        inline=False)
        embed.add_field(name='[3] :spoon: / 50 000 <:TACoin:806882594519515146>',
                        value='Zvyšuje se šance na zvířata co můžeš chytit s :knife: a :archery: Navíc můžeš chytit :rabbit2: a :unicorn:',
                        inline=False)
        embed.add_field(name='[4] <:otrok:824609734778421258> / 15 000 <:TACoin:806882594519515146>',
                        value='Kup si otroka a rozšiř si tak místo v inventáři o 50!', inline=False)
        embed.add_field(name='[5]  ⭐SWAG/ 20 000 <:TACoin:806882594519515146>',
                        value='Kup si roli ⭐SWAG, budeš výše v tabu a můžeš měnit přezdívky!!', inline=False)
        embed.set_footer(text='Jakýkoli předmět si můžeš koupit pomocí !buy *čislo předmětu*')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, help='Zakoupení předmětu.', usage='!buy [číslo předmětu]')
    async def buy(self, ctx, number_buy):
        user = ctx.author
        server = ctx.guild
        await coin_update(user, server)
        stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
        capacity = await capacity_check(user, server)
        my_capacity = stats['capacity']
        if capacity >= my_capacity:
            await ctx.send('Nemáš místo v inventáři...')
        else:
            if number_buy == '1':
                try_number = stats['money'] - 5000
                if try_number >= 0:
                    inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                         {'$set': {'money': try_number}})
                    animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {':knife:': 1}})
                    await ctx.send('Koupil sis :knife:')
                else:
                    await ctx.send('Nemáš dostatek peněz na :knife:')
            if number_buy == '2':
                try_number = stats['money'] - 20000
                if try_number >= 0:
                    inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                         {'$set': {'money': try_number}})
                    animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {':archery:': 1}})
                    await ctx.send('Koupil sis :archery:')
                else:
                    await ctx.send('Nemáš dostatek peněz na :archery:')
            if number_buy == '3':
                try_number = stats['money'] - 50000
                if try_number >= 0:
                    inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                         {'$set': {'money': try_number}})
                    animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {':spoon:': 1}})
                    await ctx.send('Koupil sis :spoon:')
                else:
                    await ctx.send('Nemáš dostatek peněz na :spoon:')
            if number_buy == '4':
                try_number = stats['money'] - 15000
                if try_number >= 0:
                    result = stats['capacity'] + 50
                    inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                         {'$set': {'money': try_number}})
                    inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {'capacity': result}})
                    await ctx.send('Koupil sis <:otrok:824609734778421258>')
                else:
                    await ctx.send('Nemáš dostatek peněz na <:otrok:824609734778421258>')
            if number_buy == '5':
                try_number = stats['money'] - 20000
                if try_number >= 0:
                    role = discord.utils.find(lambda r: r.name == '⭐SWAG', ctx.guild.roles)
                    role2 = discord.utils.find(lambda r: r.name == 'Aby Byl Dlaba Spokojen', ctx.guild.roles)
                    if role not in ctx.author.roles:
                        inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                             {'$set': {'money': try_number}})

                        await ctx.author.add_roles(role)
                        await ctx.author.add_roles(role2)
                        await ctx.send('Koupil sis ⭐SWAG')
                    else:
                        await ctx.send('Roli ⭐SWAG už máš!')
                else:
                    await ctx.send('Nemáš dostatek peněz na roli ⭐SWAG')

    @commands.command(help='Pošle danému člověku daný počet TA Coinů', usage='!send [peníze] [uživatel]')
    async def send(self, ctx, money=None, member: discord.Member = None):
        user = ctx.author
        server = ctx.guild
        await coin_update(user, server)
        stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
        stats2 = inventory.find_one({'id': str(member.id), 'server': str(server.id)})
        if member == None:
            await ctx.send('Musíš napsat komu chceš peníze poslat!')
        elif money == None:
            await ctx.send('Musíš napsat kolik chceš dotyčnému poslat!')
        else:
            check_price = stats['money'] - int(money)
            if check_price >= 0:
                result = stats['money'] - int(money)
                result2 = stats2['money'] + int(money)
                inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {'money': result}})
                inventory.update_one({'id': str(member.id), 'server': str(server.id)}, {'$set': {'money': result2}})
                await ctx.send(f'Poslal jsi {member.mention} svých {money} <:TACoin:806882594519515146>')
            else:
                await ctx.send('Nemáš dost <:TACoin:806882594519515146> na tuto platbu xd. Poor')

    @commands.command(help='Prodáš item. Jméno se uvádí podle jména emotu.', usage='!sell [zvíře] (počet-nepovinný)')
    async def sell(self, ctx, item, count=None):
        user = ctx.author
        server = ctx.guild
        await coin_update(user, server)
        stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
        things = animals.find_one({'id': str(user.id), 'server': str(server.id)})
        if count == None:
            count = 1
        if f':{item}:' not in sell_list:
            await ctx.send('Toto zvíře neznám...')
        elif f':{item}:' in sell_list:
            check_item = things[f':{item}:'] - int(count)
            x = 0
            for i in sell_list:
                if i == f':{item}:':
                    pos_of_item = x
                    break
                x += 1
            if check_item >= 0:
                result = things[f':{item}:'] - int(count)
                animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {f':{item}:': result}})
                money_result = stats['money'] + int(count) * price_list[pos_of_item]
                inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {'money': money_result}})

                await ctx.send(
                    f'Prodal jsi {count} :{item}: za {int(count) * price_list[pos_of_item]} <:TACoin:806882594519515146>')
            else:
                await ctx.send(f'Nemáš dostatek :{item}: na prodej...')

    @commands.command(help='Chytáš zvířata. Použítí jednou za 2 minuty.', usage='!hunt')
    async def hunt(self, ctx):
        user = ctx.author
        server = ctx.guild
        await coin_update(user, server)
        capacity = await capacity_check(user, server)
        start = await coin_add(user, server, 'time3', 120)
        stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
        things = animals.find_one({'id': str(user.id), 'server': str(server.id)})
        pending = 120 - (time.time() - stats['time3'])
        my_capacity = stats['capacity']

        if start == True:

            if capacity >= my_capacity:
                await ctx.send('Nemáš dost místa v inventáři...')
            else:
                choice = [0, 1]
                choice = random.choices(choice, [60, 40])

                if choice[0] == 0:
                    if ':spoon:' in things:
                        catch = random.choices(hunt_list, [70, 50, 20, 3, 10, 5, 10, 20, 5, 1, 20])
                    elif ':knife:' in things:
                        catch = random.choices(hunt_list, [50, 30, 15, 3, 5, 0, 3, 5, 0, 0, 20])
                    elif ':archery:' in things:
                        catch = random.choices(hunt_list, [60, 40, 17, 3, 7, 3, 5, 10, 0, 0, 20])
                    else:
                        catch = random.choices(hunt_list, [40, 20, 5, 3, 0, 0, 0, 0, 0, 0, 20])
                    try:
                        if catch[0] == ':knife:':
                            if things[':knife:'] > 0:
                                await ctx.send(':knife: už máš... Nic jsi nenašel.')
                            else:
                                await ctx.send(
                                    f'Našel jsi {catch[0]}!! Tvoje šance na chycení :hamster: jsou 2x vyšší a šance na chycení :bear: se zvýšila o 1,5!!')
                                animals.update_one({'id': str(user.id), 'server': str(server.id)},
                                                   {'$set': {catch[0]: 1}})
                        elif catch[0] == '<:kalda:829322764065701889>':
                            kalda_money = random.choice(range(10, 100))
                            result = stats['money'] + kalda_money
                            await ctx.send(
                                f'Našel jsi {catch[0]} . Okradl jsi ho a našel jsi {kalda_money} <:TACoin:806882594519515146> . <:TriHard:806263536921608212>')
                            inventory.update_one({'id': str(user.id), 'server': str(server.id)},
                                                 {'$set': {'money': result}})
                        else:
                            number_catch = things[catch[0]] + 1
                            animals.update_one({'id': str(user.id), 'server': str(server.id)},
                                               {'$set': {catch[0]: number_catch}})
                            await ctx.send(f'Chytil jsi {catch[0]}')
                    except:
                        animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {catch[0]: 1}})
                        await ctx.send(f'Chytil jsi {catch[0]} Tvůj první kousek <:poggers:824280503590322277>')
                elif choice[0] == 1:
                    catch = random.choices(fail_text)
                    if catch[0] == 'Našel jsi dva dny staré :newspaper2:, jediný co ses dozvěděl že ':
                        f = requests.get('https://newsapi.org/v2/top-headlines?country=cz&apiKey={}'.format(os.getenv('NEWS_TOKEN')))
                        news = f.json()
                        await ctx.send(catch[0] + news['articles'][random.choice(range(0, len(news['articles'])))]['title'])
                    else:
                        await ctx.send(catch[0])
        elif start == False:
            minutes = pending / 60
            await ctx.send(f'Znova můžeš použít příkaz za **{int(minutes)} minut** a **{int(pending % 60)} vteřin**')

    @commands.command(help='Denní odměna TA Coinů, můžeš použít jednou za 24h.', usage='!daily')
    async def daily(self, ctx):
        user = ctx.author
        server = ctx.guild
        await coin_update(user, server)
        stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
        pending_s = 86400 - (time.time() - stats['time'])
        pending_m = pending_s / 60
        pending_h = pending_m / 60
        pending_s_final = pending_s % 60
        pending_m_final = pending_m % 60

        answer = await coin_add_24(user, server, 300)
        if answer == True:
            await ctx.send('Vyzvednul sis denní odměnu 300 <:TACoin:806882594519515146>')
        elif answer == False:
            await ctx.send(
                f'Dnes sis již vyzvedl <:TACoin:806882594519515146>. Znova si jej můžeš vyzvednout za `{int(pending_h)} hodin {int(pending_m_final)} minut {int(pending_s_final)} vteřin`')

    @commands.command(help='Zobrazí jaké zvíře můžeš za kolik prodat.', usage='!prices')
    async def prices(self, ctx):

        embed = discord.Embed(title="Ceny", description="Tady vidíte za kolik můžete co prodat!", color=0x0b12ea)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(
            url="https://images-ext-1.discordapp.net/external/tNcvSCRmdnuc2UTxzxUxvEEamscNLhps_JwSL4_nq4o/https/images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%25253Fsize%25253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
        embed.add_field(name="Věci:", value='\n'.join(
            "{} / {} <:TACoin:806882594519515146>".format(x, y) for x, y in zip(sell_list, price_list)), inline=False)
        await ctx.send(embed=embed)

    @commands.command(help='Ukáže počet TA Coinů které máš', usage='!money (uživatel-nepovinný)')
    async def money(self, ctx, user: discord.Member = None, aliases='balance'):

        server = ctx.guild

        if user == None:
            user = ctx.author
        await coin_update(user, server)
        stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})

        money = stats['money']
        await ctx.send(f'Máš {money} <:TACoin:806882594519515146>')



def setup(client):
    client.add_cog(Ekonomika(client))


async def coin_update(user, server):
    stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
    things = animals.find_one({'id': str(user.id), 'server': str(server.id)})
    if stats == None:
        newuser = {'id': str(user.id), 'server': str(server.id), 'money': 0, 'time': 0, 'time2': 0, 'time3': 0,
                   'capacity': 25}
        inventory.insert_one(newuser)
    if things == None:
        newuser = {'id': str(user.id), 'server': str(server.id)}
        animals.insert_one(newuser)


async def capacity_check(user, server):
    things = animals.find_one({'id': str(user.id), 'server': str(server.id)})
    number_of_things = 0
    for i in sell_list:
        if i in things:
            number_of_things += things[i]
    return (number_of_things)


async def coin_add(user, server, time_clock, time_wait):
    stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
    if stats['server'] == '806808047509831700':
        return(True)
    else:
        if time.time() - stats[time_clock] >= time_wait:
            inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set': {time_clock: time.time()}})
            return (True)
        elif time.time() - stats[time_clock] < time_wait:
            return (False)


def unescape(s):
    s = s.replace("&quot;", "''")
    s = s.replace("&#039;", "'")
    s = s.replace("&amp;", "&")
    return s

async def coin_add_24(user, server, money):
  stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
  if time.time() - stats['time'] > 86400:
    money_update = stats['money'] + money
    inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': money_update, 'time': time.time()}})
    return(True)
  else:
    return(False)
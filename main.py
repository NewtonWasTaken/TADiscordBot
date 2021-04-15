import discord
import os
import random
from discord.ext import commands
from kahoot import client
import json
import time
import requests
import asyncio
from google_trans_new import google_translator
import pymongo
import youtube_dl



requests.packages.urllib3.disable_warnings()
translator = google_translator()
intents = discord.Intents.all()
bot = client()
client = commands.Bot(command_prefix="!")
client.remove_command('help')

password = os.getenv('PASSWORD')
mongo_client = pymongo.MongoClient(f'mongodb+srv://newton:{password}@tabot.ardyf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
users = mongo_client['TABOT']['users']
inventory = mongo_client['TABOT']['inventory']
animals = mongo_client['TABOT']['animals']



hunt_list = [':mouse:', ':hamster:', ':bear:', ':knife:', ':mammoth:', ':bird:', ':kangaroo:', ':monkey:', ':rabbit2:', ':unicorn:', '<:kalda:829322764065701889>']
sell_list = [':mouse:', ':hamster:', ':bear:', ':knife:', ':mammoth:', ':bird:', ':kangaroo:', ':monkey:', ':rabbit2:', ':unicorn:', ':archery:', ':spoon:', '<:kalda:829322764065701889>']
price_list = [50, 75, 150, 4000, 200, 500, 250, 200, 600, 5000, 17000, 45000, 0]
fail_text = ['Našel jsi :teddy_bear: hodil jsi ho do popelnice...', 'Našel jsi dva dny staré :newspaper2:, jediný co ses dozvěděl je že zase prodloužili lockdown...', 'Našel jsi :knot: Myslím že ti bude k ničemu...','Našel jsi :knife:, ale byl plastovej xd', 'Našel jsi :french_bread:, a snědl jsi ji, takže teď už nemáš nic :)','Našel jsi :bread:, a snědl jsi ho, takže teď už nemáš nic :)', 'Našel jsi :knot:, takže se konečně můžeš oběsit...']
pp = ['8D', '8=D', '8==D', '8===D', '8====D', '8=====D', '8======D', '8=======D', '8========D']

ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
life = ['Žiju!', 'Nežiju!']
distribution = [.9, .1]
song_queue = {}

flaska1 = []
flaska2 = []
flaska3 = []
flaska4 = []

@client.event
async def on_message(message):
  if message.author.bot:
    return
  


  await update_data(message.author, message.guild)
  await add_xp(message.author, 20, message.guild)
  await level_up(message.author, message.guild)
  await client.process_commands(message)
  


async def update_data(user, server):
  stats = users.find_one({'id': str(user.id), 'server': str(server.id)})
  if stats == None:
    newuser = {'id': str(user.id), 'server': str(server.id), 'xp': 0, 'level': 1}
    users.insert_one(newuser)
  
    
    

  

async def add_xp(user, xp, server):
  stats = users.find_one({'id': str(user.id), 'server': str(server.id)})
  add = stats['xp'] + xp
  users.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'xp': add}})
   
   
  
  
   

async def level_up(user, server):
  stats = users.find_one({'id': str(user.id), 'server': str(server.id)})
  if server.id == 693009303526703134:
   channel = client.get_channel(826042384558063617)
  if server.id == 806808047509831700:
    channel = client.get_channel(807246401607827536)
  exp = stats['xp']
  lvl_end = stats['level'] + 1
  finish = lvl_end **(1/(1/4))

  if exp >= finish:
    update_level = lvl_end
    users.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'level': update_level}})
    await channel.send('{} má level {}'.format(user.mention, lvl_end))
    



@client.command()
async def rank(ctx, member: discord.Member = None):
  
  if member is None:
    member = ctx.message.author
  server = ctx.message.guild 
  stats = users.find_one({'id': str(member.id), 'server': str(server.id)})
  if stats == None:
    embed=discord.Embed(title="Rank", description="Jméno člena: {}".format(member.mention), color=0x084be7)
    embed.add_field(name="XP:", value= '0/16 XP', inline=True)
    embed.add_field(name="Level:", value='1', inline=True)
    embed.add_field(name="1                                                           2", value=10 * ' :white_large_square: ', inline=False)
    embed.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed=embed)
  
  else:
    lvl_end = stats['level'] + 1
    lvl = stats['level']
    exp = stats['xp']
    
    finish = lvl_end **(1/(1/4))
    finish2 = lvl **(1/(1/4))
    finish3 = finish - finish2
    exp2 = exp - finish2
    boxes = finish3 / 10
    boxes1 = exp2 / boxes
    embed=discord.Embed(title="Rank", description="Jméno člena: {}".format(member.mention), color=0x084be7)
    embed.add_field(name="XP:", value= f'{exp} / {int(finish)} XP', inline=True)
    embed.add_field(name="Level:", value=lvl, inline=True)
    embed.add_field(name=f"{lvl}                                                                {lvl_end}", value=int(boxes1) * ' :blue_square: ' + (10 - int(boxes1)) * ' :white_large_square: ', inline=False)
    embed.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed=embed)
  
  



@client.group(name='flaska', invoke_without_command=True)
async def flaska(ctx):
    flaska1.append(f'<@{ctx.message.author.id}>')
    flaska2.append(f'{ctx.message.author.name}')
    await ctx.send(f'<@{ctx.message.author.id}>' + ' se připojil do flašky!')


@flaska.command(name='list')
async def list_subcommand(ctx):

    enoughPlayers1 = len(flaska1)
    if enoughPlayers1 <= 0:
        await ctx.send('Zatím se nikdo nepřipojil...')
    else:
        flaska4 = list(dict.fromkeys(flaska2))
        await ctx.send(', '.join(flaska4))


@flaska.command(name='start')
async def start_subcommand(ctx):
    flaska3 = list(dict.fromkeys(flaska1))
    enoughPlayers = len(flaska3)
    if enoughPlayers > 1:
        result = random.sample(flaska3, 2)
        await ctx.send(' <:flaska:807228132326899732> '.join(result) +
                       ' Pravda nebo úkol?')
    else:
        await ctx.send('Není dostatek hráčů pro zahájení flašky.')


@flaska.command(name='end')
async def end_subcommand(ctx):
    flaska1.clear()
    flaska2.clear()
    flaska3.clear()
    flaska4.clear()
    await ctx.send('Flaška byla ukončena!')



@client.group(name = 'kahoot', invoke_without_command=True)
async def kahoot(ctx, arg, arg2):
  bot.join(arg, arg2)
  await ctx.send(f'Připojil si se do kahootu: { arg}, se jménem { arg2}')

@kahoot.command(name = 'ddos')
async def ddos_subcommand(ctx, arg, arg2):
  i = 0
  await ctx.send(f'Úspěšně připojeno 100 botů na { arg}')
  while i < 100:
   name = f'{arg2}{i}'
   bot.join(arg, name)
   i = i + 1


@client.group(name='server', invoke_without_command=True)
async def server(ctx):
  await ctx.send('IP našeho serveru je: TercieA.minehut.gg, Je na verzi 1.16.5')
  

@server.command(name = 'status')
async def status_subcommand(ctx):
  response = requests.get('https://api.minehut.com/server/TercieA?byName=true')
  server = response.json()
  count = server['server']['playerCount']
  maxplayers = server['server']['maxPlayers']
  if server['server']['online'] == False:
    embed=discord.Embed(title="Server je offline!", color=0xff0000)
    embed.set_author(name="Minecraft Server Tercie A")
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
    embed.add_field(name="Připoj se na server a do chatu napiš:", value="/join TercieA, pak se odpoj a počkej až se server zapne", inline=False)
    embed.set_footer(text="IP adresa serveru: TercieA.minehut.gg")
    await ctx.send(embed=embed)
  elif server['server']['online'] == True:
    embed=discord.Embed(title="Server je online!", color=0x1fd312)
    embed.set_author(name="Minecraft Server Tercie A")
    embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png')
    embed.add_field(name="Počet lidí na serveru:", value=f'{count} z {maxplayers} \n' + count * ' :blue_square: ' + (10 - count) * ' :white_large_square: ', inline=False)
    embed.set_footer(text="IP adresa serveru: TercieA.minehut.gg")
    await ctx.send(embed=embed)



'''
@server.command(name = 'start')
async def start_server_subcommand(ctx):
  s = requests.post('https://api.minehut.com/users/login', data = login)
  
  r = requests.post('https://api.minehut.com/server/6037e2a8800860017c1f0ee0/start_service')
  await ctx.send('Server byl zapnut!')
  print(r.text)
  print(s.text)
'''
@client.command()
async def nsfw(ctx):
  f = requests.get('https://meme-api.herokuapp.com/gimme/nsfw')
  meme = f.json()
  if ctx.channel.is_nsfw():
    await ctx.send(meme['url'])
  if not ctx.channel.is_nsfw():
    await ctx.send('Tento příkaz může být použit pouze v nsfw kanálu.')

@client.command()
async def meme(ctx):
  f = requests.get('https://meme-api.herokuapp.com/gimme/meme')
  meme = f.json()
  if meme['nsfw'] == False:
    await ctx.send(meme['url'])
  else: 
    meme()

@client.command()
async def shrug(ctx):
 await ctx.send('¯\_(ツ)_/¯')

@client.group(name='student', invoke_without_command=True)
async def student(ctx):
  roasty = open('roasts.txt', 'r')
  roasty2 = roasty.read().splitlines()
  student = random.choice(roasty2)
  await ctx.send(student)
  roasty.close()

@student.command(name = 'add')
async def student_insert(ctx, *, hlaska):
  f = open('roasts.txt', 'a')
  s = open('roasts.txt', 'r')
  roasts = s.read().lower().splitlines()
  if hlaska.lower() in roasts:
    embed=discord.Embed(title="TA Discord bot", color=0xfc0303)
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
    embed.add_field(name="Oh no...", value="Hláška se už nachází v seznamu...", inline=False)
    await ctx.send(embed=embed) 
  elif hlaska.lower() not in roasts:
   f.write(f'\n{hlaska}')
   embed=discord.Embed(title="TA Discord bot", color=0x12e60f)
   embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
   embed.add_field(name="Nice!", value=f"Hláška: '{hlaska}' byla přidána do seznamu!", inline=False)
   await ctx.send(embed=embed)
  f.close()
  s.close()


@client.command()
async def status(ctx):
    rng = random.choices(life, distribution)
    await ctx.send(''.join(rng))


@client.event
async def on_ready():
    print('Connected to {0.user}'.format(client))
    await client.change_presence(activity= discord.Game(name='Cvičí posilko s Vaňkem | !help'))


@client.group(name='help', invoke_without_command=True)
async def help(ctx):
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
    embed.add_field(name="Vlastní commandy <:TACoin:806882594519515146> ", value="`yum` `emote` `kompet` `credit` `shrug` `translate`", inline=False)
    embed.add_field(name="Random věci :slot_machine: ", value="`ucitel` `howgay` `simp` `rng` `pp` `meme` `student` \n`ucitel add` `student add`", inline=False)
    embed.add_field(name="NSFW :underage: ", value = "`boob` `butt` `nsfw`", inline=False)
    embed.add_field(name="Flaška <:flaska:807228132326899732> ", value = "`flaska` `flaska start` `flaska list` `flaska end` ", inline=False)
    embed.add_field(name="Kahoot <:kahoot:813837093494325278> ", value =  "`kahoot` `kahoot ddos` ", inline=False)
    embed.add_field(name="Rank systém :chart_with_upwards_trend: ", value = "`rank` ", inline=False)
    embed.add_field(name="Minecraft server :tent: ", value = "`server` `server status` ", inline=False)
    embed.add_field(name="Ekonomika <:TACoin:806882594519515146> ", value = "`daily` `money` `inventory` `hunt` `send` `shop` `kviz` `kviz cz` `sell` `buy` `prices` ", inline=False)
    embed.add_field(name="Hudba :notes: ", value="`join` `leave` `play **url**` `skip` `pause` `resume`", inline=False)
    embed.set_footer(
        text=
        "Pokud chcete o něčem zjistit více napište !help s čím chcete pomoct, například !help flaska."
    )
    await ctx.send(embed=embed)


@help.command(name='flaska')
async def help_flaska_subcommand(ctx):
    embed = discord.Embed(
        title="Help",
        description=
        "Pokud potřebuješ s čimkoli pomoct, tady jsou všechny příkazy pro Flašku:",
        color=0xff0000)
    embed.set_author(name="TA Discord Bot")
    embed.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png"
    )
    embed.add_field(name="!flaska 'jmeno'",
                    value="Připojíš se do hry.",
                    inline=False)
    embed.add_field(name="!flaska start",
                    value="Začnete točit s flaškou.",
                    inline=False)
    embed.add_field(name="!flaska list",
                    value="Zobrazíte připojené hráče.",
                    inline=False)
    embed.add_field(name="!flaska end",
                    value="Vypnete flašku, a všichni hráči budou smazáni.",
                    inline=False)
    embed.set_footer(
        text=
        "Pokud chcete o něčem zjistit více napište !help s čím chcete pomoct, například !help flaska."
    )
    await ctx.send(embed=embed)


@help.command(name='kahoot')
async def help_kahoot_subcommand(ctx):
  embed = discord.Embed(title="Help",description="Pokud potřebuješ s čimkoli pomoct, tady jsou všechny příkazy pro Kahoot:", color=0xff0000)
  embed.set_author(name="TA Discord Bot")
  embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
  embed.add_field(name="!kahoot 'heslo' 'jmeno'", value="Připojíš se do kahootu se jmeném které napíšeš!", inline=False)
  embed.add_field(name="!kahoot ddos 'heslo' 'jmeno'", value="Připojí 100 botů se zadaným jménem do kahootu.", inline=False)
  embed.set_footer(text="Pokud chcete o něčem zjistit více napište !help s čím chcete pomoct, například !help flaska.")
  await ctx.send(embed=embed)



@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def howgay(ctx, member: discord.Member = None):
  if member is None:
    member = ctx.message.author
  await ctx.send(f'{member.mention} jsi na {random.randrange(1, 100, 3)}% gay. <:rainbow_flag:811896666848100363>')

@client.command()
async def simp(ctx, member: discord.Member = None):
  input = open('classsimp.txt')
  ourclasssimp = [str(number) for number in input.readline().split(',')]

  if member is None:
    member = ctx.message.author
  await ctx.send(f'{member.mention} simpíš{random.choice(ourclasssimp)} na {random.randrange(1, 100, 3)}%. <:SIMP:782941806244921354>')
  input.close()


@client.command(name = 'pp')
async def delka(ctx, member: discord.Member = None):
  if member is None:
    member = ctx.message.author
  await ctx.send(f'{member.mention} máš {random.choice(pp)}')

@client.command()
async def rng(ctx):
  input2 = open('class.txt')
  ourclass = [str(number2) for number2 in input2.readline().split(',')]
  await ctx.send(f'Náhodný člověk z naší třídy:{random.choice(ourclass)}')
  input2.close()

@client.command()
async def yum(ctx):
    await ctx.send('yim yum')


@client.command()
async def pong(ctx):
    await ctx.send(f'Nemyslel jsi ping? {round(client.latency * 1000)}ms')


@client.command()
async def kompet(ctx):
    await ctx.send(
        '<@621353544490024961> , <@551426822299189259>, <@621701863821148166>, <@558659043833675806> pojďte hrát!'
    )


@client.group(name='ucitel', invoke_without_command=True)
async def ucitel(ctx):
  ucitel = open('ucitel.txt', 'r')
  ucitel2 = ucitel.read().splitlines()
  await ctx.send(f'{random.choice(ucitel2)}')
  ucitel.close()

@ucitel.command(name='add')
async def ucitel_insert(ctx, *, hlaska):
  f = open('ucitel.txt', 'a')
  s = open('ucitel.txt', 'r')
  roasts = s.read().lower().splitlines()
  if hlaska.lower() in roasts:
    embed=discord.Embed(title="TA Discord bot", color=0xfc0303)
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
    embed.add_field(name="Oh no...", value="Hláška se už nachází v seznamu...", inline=False)
    await ctx.send(embed=embed)
  elif hlaska.lower() not in roasts:
   f.write(f'\n{hlaska}')
   embed=discord.Embed(title="TA Discord bot", color=0x12e60f)
   embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
   embed.add_field(name="Nice!", value=f"Hláška: '{hlaska}' byla přidána do seznamu!", inline=False)
   await ctx.send(embed=embed)
  f.close()
  s.close()


@client.command()
async def emote(ctx):
    await ctx.send('<:TACoin:806882594519515146>')


@client.command()
async def boob(ctx):
  nsfw = open('nsfw.txt')
  nsfw2 = nsfw.read().splitlines
  await ctx.send(f'{random.choice(nsfw2)}')
  nsfw.close()


@client.command()
async def butt(ctx):
  nsfw = open('nsfw.txt')
  nsfw2 = nsfw.read().splitlines
  await ctx.send(f'{random.choice(nsfw2)}')
  nsfw.close()


@client.command()
async def credit(ctx):
    embed = discord.Embed(
        title="Credits",
        description=
        "Tohoto bota vytvořil: <@551426822299189259> a <@621353544490024961>, spíš <@551426822299189259> xD. ",
        color=0x14db3c)
    embed.set_thumbnail(
        url=
        "https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png"
    )
    await ctx.send(embed=embed)

@client.command()
async def translate(ctx, *, text):
  trans_text = text
  result= translator.translate(trans_text, lang_tgt='cs')
  await ctx.send(result)


@client.command()
async def kviz(ctx, language = None):
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
      question= translator.translate(en_question, lang_tgt='cs')
      category= translator.translate(en_category, lang_tgt='cs')
      answers.append(translator.translate(en_correct, lang_tgt='cs'))
      answers.append(translator.translate(en_incorrect, lang_tgt='cs'))
      answers.append(translator.translate(en_incorrect1, lang_tgt='cs'))
      answers.append(translator.translate(en_incorrect2, lang_tgt='cs'))
      correct = translator.translate(en_correct, lang_tgt='cs')
      random.shuffle(answers)
      embed=discord.Embed(title=category, color=0x378ad7)
      embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
      embed.add_field(name=question, value=f"[1] {answers[0]} \n [2] {answers[1]} \n [3] {answers[2]} \n [4] {answers[3]}", inline=True)
      await ctx.send(embed=embed)
      for i in answers:
        if i == correct:
          number = x
          break
        x = x + 1
      def check (m):
       return m.author == ctx.author and m.content.isdigit()
      try: 
        msg = await client.wait_for('message', timeout=10.0, check=check)
        if msg.content == str(number):
          await ctx.send('Správná odpověď, dostal jsi 100 <:TACoin:806882594519515146>')
          result = stats['money'] + 100
          inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': result}})          
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
      embed=discord.Embed(title=en_category, color=0x378ad7)
      embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%253Fsize%253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
      embed.add_field(name=en_question, value=f"[1] {answers[0]} \n [2] {answers[1]} \n [3] {answers[2]} \n [4] {answers[3]}", inline=True)
      await ctx.send(embed=embed)
      for i in answers:
        if i == correct:
          number = x
          break
        x = x + 1
      def check2 (m):
       return m.author == ctx.author and m.content.isdigit()        
      try: 
        msg = await client.wait_for('message', timeout=10.0, check=check2)
        if msg.content == str(number):
          await ctx.send('Správná odpověď, dostal jsi 100 <:TACoin:806882594519515146>')
          result = stats['money'] + 100
          inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': result}})
        else:
          await ctx.send(f'Špatná odpověď, nic jsi nedostal... Správná odpověď byla **{correct}**')
      except asyncio.TimeoutError:
        await ctx.send(f'Nestihl jsi odpovědět, nic jsi nedostal...Správná odpověď byla **{correct}**')     
 elif start == False:
   await ctx.send(f'Znova můžeš udělat kvíz za **{int(pending / 60)} minut {int(pending % 60)} sekund**')
  
@client.command()
async def shop(ctx):
 embed=discord.Embed(title='Shop', description='Tady si můžeš kupovat různé věci :', color=0x0b49da)
 embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
 embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%3Fsize%3D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png')
 embed.add_field(name='[1] :knife: / 5000 <:TACoin:806882594519515146>', value='Knife ti může i padnout. Zvyšuje šance na základní zvířata. S :knife: můžeš naviíc chytit :mammoth: :kangaroo: a :monkey:', inline=False)
 embed.add_field(name='[2] :archery: / 20 000 <:TACoin:806882594519515146>', value='Zvyšuje se šance na zvířata co můžeš chytit s :knife: Navíc můžeš chytit :bird:', inline=False)
 embed.add_field(name='[3] :spoon: / 50 000 <:TACoin:806882594519515146>', value='Zvyšuje se šance na zvířata co můžeš chytit s :knife: a :archery: Navíc můžeš chytit :rabbit2: a :unicorn:', inline=False)
 embed.add_field(name='[4] <:otrok:824609734778421258> / 15 000 <:TACoin:806882594519515146>', value='Kup si otroka a rozšiř si tak místo v inventáři o 50!', inline=False)
 embed.add_field(name='[5]  ⭐SWAG/ 20 000 <:TACoin:806882594519515146>', value='Kup si roli ⭐SWAG, budeš výše v tabu a můžeš měnit přezdívky!!', inline=False)
 embed.set_footer(text='Jakýkoli předmět si můžeš koupit pomocí !buy *čislo předmětu*')
 await ctx.send(embed=embed)

@client.command(pass_context=True)
async def buy(ctx, number_buy):
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
        inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': try_number}})
        animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{':knife:': 1}})
        await ctx.send('Koupil sis :knife:')
      else:
        await ctx.send('Nemáš dostatek peněz na :knife:')
    if number_buy == '2':
      try_number = stats['money'] - 20000
      if try_number >= 0:
        inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': try_number}})
        animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{':archery:': 1}})
        await ctx.send('Koupil sis :archery:')
      else:
        await ctx.send('Nemáš dostatek peněz na :archery:')
    if number_buy == '3':
      try_number = stats['money'] - 50000
      if try_number >= 0:
        inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': try_number}})
        animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{':spoon:': 1}})
        await ctx.send('Koupil sis :spoon:')
      else:
        await ctx.send('Nemáš dostatek peněz na :spoon:')
    if number_buy == '4':
      try_number = stats['money'] - 15000
      if try_number >= 0:
        result = stats['capacity'] + 50     
        inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': try_number}})
        inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'capacity': result}})
        await ctx.send('Koupil sis <:otrok:824609734778421258>')
      else:
        await ctx.send('Nemáš dostatek peněz na <:otrok:824609734778421258>')
    if number_buy == '5':
      try_number = stats['money'] - 20000
      if try_number >= 0:
        role = discord.utils.find(lambda r: r.name == '⭐SWAG', ctx.guild.roles)
        role2 = discord.utils.find(lambda r: r.name == 'Aby Byl Dlaba Spokojen', ctx.guild.roles)
        if role not in ctx.author.roles:
         inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': try_number}})
        
         await ctx.author.add_roles(role)
         await ctx.author.add_roles(role2)
         await ctx.send('Koupil sis ⭐SWAG')
        else:
          await ctx.send('Roli ⭐SWAG už máš!')
      else:
        await ctx.send('Nemáš dostatek peněz na roli ⭐SWAG')


@client.command()
async def send(ctx, money = None, member: discord.Member = None):
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
      inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': result}})
      inventory.update_one({'id': str(member.id), 'server': str(server.id)}, {'$set':{'money': result2}})
      await ctx.send(f'Poslal jsi {member.mention} svých {money} <:TACoin:806882594519515146>')
    else:
      await ctx.send('Nemáš dost <:TACoin:806882594519515146> na tuto platbu xd. Poor')


@client.command()
async def sell(ctx, item, count = None):
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
     animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{f':{item}:': result}})
     money_result = stats['money'] + int(count) * price_list[pos_of_item]
     inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': money_result}})
     
     await ctx.send(f'Prodal jsi {count} :{item}: za {int(count) * price_list[pos_of_item]} <:TACoin:806882594519515146>')
    else:
      await ctx.send(f'Nemáš dostatek :{item}: na prodej...')

@client.command()
async def hunt(ctx):
  user = ctx.author
  server = ctx.guild
  await coin_update(user, server)
  capacity = await capacity_check(user, server)
  start = await coin_add(user, server, 'time3', 120)
  stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
  things = animals.find_one({'id': str(user.id), 'server': str(server.id)})
  pending = 120 - (time.time() - stats['time3'])
  my_capacity =  stats['capacity']

  if start == True:
    
    if capacity >= my_capacity:
     await ctx.send('Nemáš dost místa v inventáři...')
    else:
      choice = [0, 1]
      choice = random.choices(choice, [40, 50])
      
      
      
      if choice[0] == 0:
        if ':knife:' in things:
         catch = random.choices(hunt_list, [50, 30, 15, 3, 5, 0, 3, 5, 0, 0, 20])
        elif ':archery:' in things:
         catch = random.choices(hunt_list, [60, 40, 17, 3, 7, 3, 5, 10, 0, 0, 20])
        elif ':spoon:' in things:
          catch = random.choices(hunt_list, [70, 50, 20, 3, 10, 5, 10, 20, 5, 1, 20])
        else:
          catch = random.choices(hunt_list, [40, 20, 5, 3, 0, 0, 0, 0, 0, 0, 20])
        try:
          if catch[0] == ':knife:':
            if things[':knife:'] > 0:
              await ctx.send(':knife: už máš... Nic jsi nenašel.')
            else:
              await ctx.send(f'Našel jsi {catch[0]}!! Tvoje šance na chycení :hamster: jsou 2x vyšší a šance na chycení :bear: se zvýšila o 1,5!!') 
              animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{catch[0]: 1}})
          elif catch[0] == '<:kalda:829322764065701889>':
              kalda_money = random.choice(range(10, 100))
              result = stats['money'] + kalda_money
              await ctx.send(f'Našel jsi {catch[0]} . Okradl jsi ho a našel jsi {kalda_money} <:TACoin:806882594519515146> . <:TriHard:806263536921608212>')
              inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money' : result}})
          else:
            number_catch = things[catch[0]] + 1
            animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{catch[0]: number_catch}})
            await ctx.send(f'Chytil jsi {catch[0]}')
        except:
            animals.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{catch[0]: 1}})
            await ctx.send(f'Chytil jsi {catch[0]} Tvůj první kousek <:poggers:824280503590322277>')
      elif choice[0] == 1:
        catch = random.choices(fail_text)
        await ctx.send(catch[0])
  elif start == False:
    minutes = pending / 60
    await ctx.send (f'Znova můžeš použít příkaz za **{int(minutes)} minut** a **{int(pending % 60)} vteřin**')






@client.command()
async def prices(ctx):
 


 embed=discord.Embed(title="Ceny", description="Tady vidíte za kolik můžete co prodat!", color=0x0b12ea)
 embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
 embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/tNcvSCRmdnuc2UTxzxUxvEEamscNLhps_JwSL4_nq4o/https/images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%25253Fsize%25253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
 embed.add_field(name="Věci:", value='\n'.join("{} / {} <:TACoin:806882594519515146>".format(x, y) for x, y in zip(sell_list, price_list)), inline=False)
 await ctx.send(embed=embed)





@client.command(aliases=['inventory'])
async def inventory_command(ctx, user: discord.Member = None):
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



  
@client.command()
async def daily(ctx):
  user = ctx.author
  server = ctx.guild
  await coin_update(user, server)
  stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
  pending_s  = 86400 - (time.time() - stats['time'])
  pending_m = pending_s / 60
  pending_h = pending_m / 60
  pending_s_final = pending_s % 60
  pending_m_final = pending_m % 60
  
  answer = await coin_add_24(user, server, 300)
  if answer == True:
    await ctx.send('Vyzvednul sis denní odměnu 300 <:TACoin:806882594519515146>')
  elif answer == False:
    await ctx.send(f'Dnes sis již vyzvedl <:TACoin:806882594519515146>. Znova si jej můžeš vyzvednout za `{int(pending_h)} hodin {int(pending_m_final)} minut {int(pending_s_final)} vteřin`')




@client.command()
async def money(ctx, user: discord.Member = None, aliases = 'balance'):
  
  server = ctx.guild

  if user == None:
    user = ctx.author
  await coin_update(user, server)
  stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})


  money = stats['money']
  await ctx.send(f'Máš {money} <:TACoin:806882594519515146>')


@client.command()
async def connect(ctx):
    channel = ctx.author.voice
    voice = discord.utils.get(client.voice_clients, guild= ctx.guild)
    if channel == None:
        await ctx.send('Musíš být připojen do kanálu na připojení bota')
    else:
        if voice == None:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
            await ctx.send('Bot připojen na voice!')
            return(True)
        else:
            return (True)
            await ctx.send('Bot už je připojen jinde')



@client.command()
async def leave(ctx):
    channel = ctx.author.voice
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if channel == None:
        await ctx.send('Musíš být připojen do kanálu na odpojení bota')
    elif voice.channel.id == ctx.author.voice.channel.id:
        await voice.disconnect()
        await ctx.send('Bot byl odpojen z voicu!')
    else:
        await ctx.send('Musíš být připojen do stejného kanálu na odpojení bota')
@client.command()
async def play(ctx, *, url):
    blacklist = open('blacklist.txt', 'r')
    blacklist2 = blacklist.read().splitlines()
    if not url in blacklist2:
        if await connect(ctx):
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            song = search(url, ctx.author)
            try:
                song_queue[str(ctx.guild.id)].append(song)
            except:
                song_queue[str(ctx.guild.id)] = []
                song_queue[str(ctx.guild.id)].append(song)
            if not voice.is_playing():
                voice.play(discord.FFmpegPCMAudio(song_queue[str(ctx.guild.id)][0]['source'], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
                voice.is_playing()
                embed = discord.Embed(title="Hudba", color=0x1927e6)
                embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/tNcvSCRmdnuc2UTxzxUxvEEamscNLhps_JwSL4_nq4o/https/images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%25253Fsize%25253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
                embed.add_field(name="Právě hraje", value=f"[{song_queue[str(ctx.guild.id)][0]['title']}]({song_queue[str(ctx.guild.id)][0]['link']})", inline=False)
                embed.add_field(name=f"Song navrhl: ", value=f"{song_queue[str(ctx.guild.id)][0]['user'].mention}", inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Hudba", color=0x1927e6)
                embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/tNcvSCRmdnuc2UTxzxUxvEEamscNLhps_JwSL4_nq4o/https/images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%25253Fsize%25253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
                embed.add_field(name="Přidáno do řady", value=f"[{song['title']}]({song['link']})", inline=False)
                embed.add_field(name=f"Song navrhl: ", value=f"{song['user'].mention}", inline=False)
                await ctx.send(embed=embed)
    else:
        await ctx.send('Tenhle song je blacklistnutý nepouštěj ho chuju!!')

@client.command()
async def skip(ctx):
    channel = ctx.author.voice
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if channel == None:
        await ctx.send('Musíš být připojen do kanálu na skipnutí songu')
    elif voice.channel.id == ctx.author.voice.channel.id:
        if voice.is_playing():
            skip_song(ctx)
        else:
            await ctx.send('Nic nehraje...')
    else:
        await ctx.send('Musíš být připojen do stejného kanálu na skipnutí')

@client.command()
async def pause(ctx):
    channel = ctx.author.voice
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if channel == None:
        await ctx.send('Musíš být připojen do kanálu na pausnutí songu')
    elif voice.channel.id == ctx.author.voice.channel.id:
        if voice.is_playing():
            voice.pause()
            await ctx.send('Pozasatveno :pause_button:')
        else:
            await ctx.send('Nic nehraje...')
    else:
        await ctx.send('Musíš být připojen do stejného kanálu na pause')

@client.command()
async def resume(ctx):
    channel = ctx.author.voice
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if channel == None:
        await ctx.send('Musíš být připojen do kanálu na pausnutí songu')
    elif voice.channel.id == ctx.author.voice.channel.id:

        voice.resume()
        await ctx.send('Pokračujeme... :play_pause:')

    else:
        await ctx.send('Musíš být připojen do stejného kanálu na pause')

def skip_song(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if len(song_queue[str(ctx.guild.id)]) > 0:
        voice.stop()
        asyncio.run_coroutine_threadsafe(ctx.send('Skipnuto :white_check_mark:'), client.loop)
def play_next(ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if len(song_queue[str(ctx.guild.id)]) > 1:
            del song_queue[str(ctx.guild.id)][0]
            voice.play(discord.FFmpegPCMAudio(song_queue[str(ctx.guild.id)][0]['source'], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
            voice.is_playing()
            embed = discord.Embed(title="Hudba", color=0x1927e6)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/tNcvSCRmdnuc2UTxzxUxvEEamscNLhps_JwSL4_nq4o/https/images-ext-1.discordapp.net/external/SMPyCghYQ5glv-QvS8SI3hzsUOwP1As2mTpo6EbNI6Y/https/images-ext-2.discordapp.net/external/fk_Rt54KghVZzB6f4zULyh3zwfwejIFC8YrTSm0n93U/%25253Fsize%25253D1024/https/cdn.discordapp.com/icons/693009303526703134/97eaa6054b8ca49e7dcc44e2fc725792.png")
            embed.add_field(name="Právě hraje", value=f"[{song_queue[str(ctx.guild.id)][0]['title']}]({song_queue[str(ctx.guild.id)][0]['link']})", inline=False)
            embed.add_field(name=f"Song navrhl: ", value=f"{song_queue[str(ctx.guild.id)][0]['user'].mention}", inline=False)
            asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), client.loop)
        else:
            try:
                del song_queue[str(ctx.guild.id)][0]
                asyncio.run_coroutine_threadsafe(ctx.send('Konec řady. :white_check_mark:'), client.loop)
            except:
                asyncio.run_coroutine_threadsafe(ctx.send('Konec řady. :white_check_mark:'), client.loop)


def search(arg, user):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(arg, download=False)
    return {'source': info['formats'][0]['url'], 'title': info['title'], 'link': f'https://www.youtube.com/watch?v={info["id"]}', 'user': user}


async def coin_add_24(user, server, money):
  stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
  if time.time() - stats['time'] > 86400:
    money_update = stats['money'] + money
    inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{'money': money_update, 'time': time.time()}})
    return(True)
  else:
    return(False)

async def coin_update(user, server):
  stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
  things = animals.find_one({'id': str(user.id), 'server': str(server.id)})
  if stats == None: 
   newuser = {'id': str(user.id), 'server': str(server.id), 'money': 0, 'time': 0, 'time2': 0, 'time3': 0, 'capacity': 25}
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
  return(number_of_things)
     

async def coin_add(user, server, time_clock, time_wait):
  stats = inventory.find_one({'id': str(user.id), 'server': str(server.id)})
  if time.time() - stats[time_clock] >= time_wait:
    inventory.update_one({'id': str(user.id), 'server': str(server.id)}, {'$set':{time_clock: time.time()}})
    return(True)
  elif time.time() - stats[time_clock] < time_wait:
    return(False)

def unescape(s):
    s = s.replace("&quot;", "''")
    s = s.replace("&#039;", "'")
    s = s.replace("&amp;", "&")
    return s



client.run(os.getenv('TOKEN'))





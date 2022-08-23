import os
import requests
import re
from discord.ext import commands
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix = '+', case_insensitive=True)
bot.remove_command('help')

def get_champion_url(champion):
  champion = champion.title()
  url = 'https://liquipedia.net/leagueoflegends/'
  furl = f'{url}{champion}'
  furl.replace(' & ','%26')
  furl.replace(' ','_')
  furl.replace("''",'%27')
  return furl

def get_champion_quote(champion):
  url = get_champion_url(champion)
  r = requests.get(url)
 
  # Parsing the HTML
  soup = BeautifulSoup(r.content, 'html.parser')
  quote = soup.find(class_="infobox-center").get_text()
  return quote

def get_champion_ability(champion):
  url = get_champion_url(champion)
  r = requests.get(url)

  soup = BeautifulSoup(r.content, 'html.parser')
  abilities = soup.find_all("div", class_="spellcard wiki-bordercolor-light")
  title_element = ""
  for ability in abilities:
    title_element += ability.find("div", class_="wiki-backgroundcolor-light").get_text()
    title_element += "\n "
  return title_element

def get_ability_description(champion):
  url = get_champion_url(champion)
  r = requests.get(url)

  soup = BeautifulSoup(r.content, 'html.parser')
  abilities = soup.find_all("div", class_="spellcard wiki-bordercolor-light")
  desc_element = ""
  for ability in abilities:
    desc_element += ability.find("div", class_="spellcard-description wiki-bordercolor-light").get_text()
    desc_element += "\n "   
  return desc_element  

def get_champion_splash(champion):
  url = get_champion_url(champion)
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')
  images = soup.find_all('img', {'src':re.compile('.jpg')})
  splash = ""
  for image in images: 
    splash += (image['src']+'\n')
  splash = splash.split("\n")
  return splash[0]  
  
#startup 
@bot.event
async def on_ready():
    print('{0.user} is on the prowl :3'.format(bot))

#commands
@bot.command(description="Help!")
async def help(ctx):
  if ctx.author == bot.user:
    return
  message = 'How to use the bot: '+'\n' +'+[INSERT COMMAND] [INSERT LEAGUE OF LEGENDS CHAMPION]'+ '\n'+ 'List of Commands: '+'\n' +'+quote ' + '\n' + '+ability' + '\n''+Q, +W, +E, +R' + '\n' + '+splash'
  await ctx.send(message)

@bot.command(description="Get League of Legends Champion quote")
async def quote(ctx, *, arg):
  if ctx.author == bot.user:
    return
  quote = get_champion_quote(arg)
  await ctx.send(quote)

@bot.command(description="Get League of Legends Champion abilities")
async def ability(ctx, *, arg):
  if ctx.author==bot.user:
    return
  ability = get_champion_ability(arg)
  ability = ability.replace("\n", ",")
  size = len(ability)
  ability = ability[:size - 2]
  await ctx.send(ability)
  
@bot.command(description = "Get League of Legends Champion passive")
async def passive(ctx, *, arg):
  if ctx.author==bot.user:
    return
  passive = get_champion_ability(arg)
  p = passive.split("\n")
  passive_desc = get_ability_description(arg)
  d = passive_desc.split("\n")
  total = p[0] + ": " + d[0]
  await ctx.send(total)

@bot.command(description = "Get League of Legends Champion Q")
async def Q(ctx, *, arg):
  if ctx.author==bot.user:
    return
  passive = get_champion_ability(arg)
  p = passive.split("\n")
  Q_desc = get_ability_description(arg)
  d = Q_desc.split("\n")
  total = p[1] + ": " + d[1]
  await ctx.send(total)

@bot.command(description = "Get League of Legends Champion W")
async def W(ctx, *, arg):
  if ctx.author==bot.user:
    return
  passive = get_champion_ability(arg)
  p = passive.split("\n")
  W_desc = get_ability_description(arg)
  d = W_desc.split("\n")
  total = p[2] + ": " + d[2]
  await ctx.send(total)

@bot.command(description = "Get League of Legends Champion E")
async def E(ctx, *, arg):
  if ctx.author==bot.user:
    return
  passive = get_champion_ability(arg)
  p = passive.split("\n")
  E_desc = get_ability_description(arg)
  d = E_desc.split("\n")
  total = p[3] + ": " + d[3]
  await ctx.send(total)

@bot.command(description = "Get League of Legends Champion R")
async def R(ctx, *, arg):
  if ctx.author==bot.user:
    return
  passive = get_champion_ability(arg)
  p = passive.split("\n")
  R_desc = get_ability_description(arg)
  d = R_desc.split("\n")
  total = p[4] + ": " + d[4]
  await ctx.send(total)

@bot.command(description = "Get League of Legends Champion splash art")
async def splash(ctx, *, arg):
  if ctx.author==bot.user:
    return
  splash = get_champion_splash(arg)
  url = 'https://liquipedia.net'
  furl = f'{url}{splash}'
  await ctx.send(furl)

my_secret = os.environ['TOKEN']
bot.run(my_secret)
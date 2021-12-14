import discord
import os
import time
import json
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from replit import db
#^ basic imports for other features of discord.py and python ^
from webserver import keep_alive


#save and load funcitons
def dbload(tags):
  with open('database.json') as f:
    tags = json.load(f)
    return tags

def dbsave():
  with open('database.json', 'w') as f:
      json.dump(tags, f)

#returns a list of the keys aka tags
def listKeys(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

client = discord.Client()

client = commands.Bot(command_prefix = '/', help_command=None) #put your own prefix here


#start up
tags = {}
tags = dbload(tags)
global currentTag
currentTag = ""


# commands

@client.command()
async def db(ctx):
  await ctx.send(tags)


@client.command()
async def tag(ctx,tag="-8533"):
  if tag != "-8533":
    tag = tag.lower()
    if tag in listKeys(tags):
      await ctx.send("Set Current Tag To : "+str(tag))
      global currentTag
      currentTag = tag
    else:
      await ctx.send("This tag does not exist... try /list to see if you misspelled an existing tag or use /create to create a new tag")
  else:
    await ctx.send("Current Tag: "+str(currentTag))

@client.command()
async def viewtags(ctx):
  await ctx.send(listKeys(tags))

@client.command()
async def list(ctx):
  if currentTag == "":
    await ctx.send("You have not set a tag! Use /tag to set one!")
  else:
    await ctx.send(sorted(tags[currentTag]))

@client.command()
async def create(ctx,newTagName):
  newTagName = newTagName.lower()
  newTagNameInKeys = newTagName in listKeys(tags)
  if newTagNameInKeys == False:
    tags[newTagName] = []
    await ctx.send("Created Tag: "+str(newTagName))
    dbsave()
  else:
    await ctx.send("Tag already exists!")

@client.command()
async def delete(ctx,tagName):
  tagName = tagName.lower()
  tags.pop(tagName)
  await ctx.send("Deleted Tag: "+str(tagName))
  dbsave()


@client.command()
async def add(ctx,userName):
  userName = userName.lower()
  if currentTag == "":
    await ctx.send("You have not set a tag! Use /tag to set one!")
  else:
    usernameInTag = userName in tags[currentTag]
    if usernameInTag == False:
      tags[currentTag].append(userName)
      await ctx.send("Added user: "+str(userName)+" to "+str(currentTag))
      dbsave()
      print("user saved to db")
    else:
      await ctx.send("This username is already in the tag!")


@client.command()
async def remove(ctx,userName):
  userName = userName.lower()
  if currentTag == "":
    await ctx.send("You have not set a tag! Use /tag to set one!")
  else:
    tags[currentTag].remove(userName)
    await ctx.send("Removed user: "+str(userName)+" to "+str(currentTag))
    dbsave()

#/ss generate search string
@client.command()
async def ss(ctx,particle,prefab="\0"):
  if currentTag == "":
    await ctx.send("You have not set a tag! Use /tag to set one!")
  else:
    ss = ""
    for i in tags[currentTag]:
      ss += particle
      ss += i

    if prefab != "\0":
      prefab = prefab.lower()
      if prefab == "ig":
        ss = "interactable&giftable" + ss
      elif prefab == "ig3":
        ss = "interactable&giftable&!friendlevel3&!lucky" + ss
    await ctx.send(ss)


@client.command()
async def help(ctx):
  helpMsg = "Organize groups of friends into tags!\nTo show your tags use the command /viewtags\nTo start working with a tag use /tag <name-of-tag>\nIf you want to create a new tag use /create <name-of-new-tag> (You can delete tags the same way with /delete\nOnce you have selected a tag use /add <username> or /remove <username> to add and remove people from the tag\nYou can view all the members of a tag by using /list\nTo generate a search string of the users use /ss <particle> example (/ss &) or (/ss &!)"
  await ctx.send(helpMsg)






#ping
@client.event
async def on_ready():
    print("Bot Online (✿ ◠ ‿ ◠ )") #will print "bot online" in the console when the bot is online
#updog message
messageCoolDown = 0.3
@client.command()
async def updog(ctx):
  await ctx.send("Wasa")
  time.sleep(messageCoolDown)
  for i in range(0,6):
    await ctx.send("wasa")
    time.sleep(messageCoolDown)
  await ctx.send("wassaaaaapppp")
  time.sleep(messageCoolDown*3)
  await ctx.send("bitconeeeeeeeeect!")

@client.command()
async def srs(ctx):
  await ctx.send("/j")


keep_alive()
client.run(os.getenv("TOKEN")) 
#get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!
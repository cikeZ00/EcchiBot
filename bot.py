import os
import discord
import time
import logging
import json
from discord.ext import commands
from discord import Game, Embed, Color, Status, ChannelType
from random import randint, sample
from discord.ext.commands import cooldown
from os import path


#Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if path.exists("config.json") == False:
    with open('config.json', 'w') as configout:
        json.dump({
        "token": "Token goes here",
        "prefix": "!",
        "owner": 350765965278969860,
        "danbooru_username": "",
        "danbooru_key": ""
         }, configout)
    print("[INFO] config.json generated!!")
    quit()
else:
    with open("config.json") as f:
        config = json.load(f)

#Cogs
initial_extensions = ['cogs.misc',
                      'cogs.owner',
                      'cogs.nsfw']

# Creating bot instance
bot = commands.Bot(command_prefix=config.get('prefix'), self_bot=False, owner_id=config.get('owner'), case_insensitive=True, help_command=None)

#Loaading cogs

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

#listeners

@bot.event
async def on_ready():
    id = bot.user.id
    bot_user = bot.user.name
    print ("------------------------------------")
    print ("Bot Name: " + bot_user)
    print ("Bot ID: " + str(id))
    print ("discord.py version: " + discord.__version__)
    print ("------------------------------------")
    if path.isfile("presence.txt"):
        with open("presence.txt") as f:
            presence = f.readline()
            await bot.change_presence(activity=discord.Game(name=presence, type=1))
    else:
        with open("presence.txt", "w") as f:
            f.write("Prefix: "+str(config.get('prefix')))
        with open("presence.txt") as f:
            presence = f.readline()
            await bot.change_presence(activity=discord.Game(name=presence, type=1))


#Message on error event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '> [ERROR] This command is on a cooldown, please try again in {:.2f}s'.format(error.retry_after)
        user = ctx.message.author
        await user.send(msg)
    elif isinstance(error, commands.CheckFailure):
        msg = '> [ERROR] You do not have the required permission to use this command!.'
        user = ctx.message.author
        await user.send(msg)
    elif isinstance(error, commands.CommandNotFound):
        msg = '> [ERROR] This command does not exist!'
        user = ctx.message.author
        await user.send(msg)
    elif isinstance(error, commands.MissingRequiredArgument):
        msg = "> [ERROR] Missing required argument(s)!"
        user = ctx.message.author
        await ctx.send(msg)
    elif isinstance(error, ConnectionError):
        print("Fucker ConnectionError. bot")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("> [ERROR] "+str(error))
    else:
        raise error

#Help commands
@bot.command()
async def help(ctx):
    user = ctx.message.author
    helpembed = discord.Embed(color=discord.Color.red())
    helpembed.set_author(name="Help (contact cikeZ00#5068 for help)")
    helpembed.add_field(name="anime", value="Usage: ``anime or anime (tag)``,  random **SFW** image.",inline=False)
    helpembed.add_field(name="hentai", value="Usage: ``hentai or hentai (tag)``,  random **NSFW** image. \n NOTE: ``Only works in NSFW marked channels``",inline=False)
    helpembed.add_field(name="ping", value="Plays ping pong",inline=False)
    helpembed.add_field(name="help", value="Shows help.",inline=False)
    await user.send(embed=helpembed)

# Authentication

if config.get('token') == "Token goes here":
    print("[ERROR] Change token in config!")
elif config.get('token') == "":
    print("[ERROR] No token present!")
else:
    print("[INFO] Starting up and logging in...")
    bot.run(config.get('token'), bot=True, reconnect=True)

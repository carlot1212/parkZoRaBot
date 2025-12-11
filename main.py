import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver
load_dotenv()

token = os.getenv('DISCORD_API_KEY')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    Print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    await bot.process_commands(message)

@bot.command()
async def harmonies(ctx):
    await ctx.send("sfdgvgdsaf")    
    thread = await ctx.message.create_thread(name="Harmonies Scoring")
    await ctx.send("How many tree points did Carlo get?")    

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
import logging
from dotenv import load_dotenv
import os
import webserver
import datetime

import discord
from discord.ext import commands, tasks

from harmonies import harmonies as harmonies_scoring
load_dotenv()

token = os.getenv('DISCORD_API_KEY')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    # start weekly scheduled task when bot is ready
    if not weekly_period_reminder.is_running():
        weekly_period_reminder.start()

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
    await harmonies_scoring(ctx, bot)

@bot.command()
async def add(ctx, *groceries):
   if ctx.channel.name != 'groceries':
      return
   
   groceries = [grocery.strip(',') for grocery in groceries]

   grocery_thread = discord.utils.get(ctx.channel.threads, name="Grocery List")

   if not grocery_thread:
      grocery_thread = await ctx.channel.create_thread(name="Grocery List") 
      for member in ctx.channel.members:
         await grocery_thread.add_user(member)

   for grocery in groceries:
       await grocery_thread.send(grocery)

@bot.command()
async def remove(ctx, *groceries): 
    if ctx.channel.name != 'groceries':
        return
    
    groceries = [grocery.strip(',') for grocery in groceries]

    grocery_thread = discord.utils.get(ctx.channel.threads, name="Grocery List")

    async for message in grocery_thread.history(limit=100):
        if message.content in groceries:
            await message.delete()

@bot.command()
async def done(ctx):
    if ctx.channel.name != 'Grocery List':
        return
    
    await ctx.channel.edit(archived=True)

    groceries_channel = discord.utils.get(ctx.guild.channels, name='groceries')

    async for message in groceries_channel.history(limit=100):
        await message.add_reaction('✅')

period_messages = [
    "It's the menstrual phase. It's period week no more peenar.....unless!",
    "It's the follicular phase. She's going back to normal!",
    "It's the ovulation phase. It's peenar time!",
    "It's the luteal phase. It's almost period week make sure to be extra nice!"
]

async def period_reminder(ctx):
    channel = discord.utils.get(ctx.guild.channels, name='general')
    week_of_the_year = datetime.datetime.now().isocalendar()[1]
    message = period_messages[week_of_the_year % len(period_messages)]
    await channel.send(message)

# Scheduled weekly reminder: runs at 09:00 local time daily, only posts on Mondays
@tasks.loop(time=datetime.time(hour=10, minute=0))
async def weekly_period_reminder():
    week_of_the_year = datetime.datetime.now().isocalendar()[1]
    message = period_messages[week_of_the_year % len(period_messages)]
    for guild in bot.guilds:
        channel = discord.utils.get(guild.channels, name='general')
        if channel and datetime.datetime.now().weekday() == 0:  # Monday == 0
            await channel.send(message)

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
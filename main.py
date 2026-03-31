from concurrent.futures import thread
import logging
from dotenv import load_dotenv
import os
import webserver
import datetime

import discord
from discord.ext import commands, tasks

from scoring import scoring as player_scoring

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
async def scoring(ctx, game: str): 
    await player_scoring(ctx, game.capitalize(), bot)

@bot.command()
async def add(ctx):
    if ctx.channel.name != 'groceries':
        return

    await ctx.channel.send("Whats grocery store would you like to add to?")
    grocery_store_response = await bot.wait_for('message', timeout=300.0)
    grocery_store = grocery_store_response.content.strip().capitalize()

    await ctx.channel.send("What items would you like to add?")
    grocery_items_response = await bot.wait_for('message', timeout=300.0)
    grocery_items = [item.strip() for item in grocery_items_response.content.split(',')]

    grocery_thread = discord.utils.get(ctx.channel.threads, name=f"{grocery_store} Grocery List")

    if not grocery_thread:
      grocery_thread = await ctx.channel.create_thread(name=f"{grocery_store} Grocery List") 
      for member in ctx.channel.members:
         await grocery_thread.add_user(member)

    for item in grocery_items:
        await grocery_thread.send(item)

@bot.command()
async def remove(ctx): 
    if ctx.channel.name != 'groceries':
        return
    
    await ctx.channel.send("Whats grocery store would you like to remove from?")
    grocery_store_response = await bot.wait_for('message', timeout=300.0)
    grocery_store = grocery_store_response.content.strip().capitalize()

    await ctx.channel.send("What items would you like to remove?")
    grocery_items_response = await bot.wait_for('message', timeout=300.0)
    grocery_items = [item.strip() for item in grocery_items_response.content.split(',')]

    grocery_thread = discord.utils.get(ctx.channel.threads, name=f"{grocery_store} Grocery List")

    async for message in grocery_thread.history(limit=100):
        if message.content in grocery_items:
            await message.delete()

period_messages = [
    "It's the menstrual phase. It's period week no more peenar.....unless!",
    "It's the follicular phase. She's going back to normal!",
    "It's the ovulation phase. It's peenar time!",
    "It's the luteal phase. It's almost period week make sure to be extra nice!"
]

def get_time(time):
    if datetime.datetime.now().astimezone().dst() != datetime.timedelta(0):
        time = datetime.time(hour=time + 9, minute=0)
    else:
        time = datetime.time(hour=time + 8, minute=0)
    return time

@tasks.loop(time=get_time(10))
async def weekly_period_reminder():
    week_of_the_year = datetime.datetime.now().isocalendar()[1]
    message = period_messages[week_of_the_year % len(period_messages) - 1]
    for guild in bot.guilds:
        channel = discord.utils.get(guild.channels, name='general')
        if channel and datetime.datetime.now().weekday() == 0:
            await channel.send(message)

@tasks.loop(time=datetime.time(hour=18, minute=0))
async def monthly_rent_reminder():
    for guild in bot.guilds:
        channel = discord.utils.get(guild.channels, name='general')
        if channel and datetime.datetime.now().day == 1:
            await channel.send("Don't forget to pay the rent today!")

habits = {'not_aozora' : ['stretch 🧘‍♂️', 'greens 🥬'],
          'parkchou' : ['weigh ⚖️', 'list 🗒️', 'stretch 🧘‍♂️', 'greens 🥬', 'school 🏫', 'journal 📒', 'water 🍺', 'clean 🧹', 'gym 💪', 'weekly schedule 📆']}

@tasks.loop(time=datetime.time(hour=16, minute=0))
async def daily_habits_reminder():
    for guild in bot.guilds:
        channel = discord.utils.get(guild.channels, name='habits')
        if channel:
            for member in guild.members:
                if not member.bot:
                    await channel.send(f"{member.mention} Daily Habits: {', '.join(habits.get(member.name, []))}")


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
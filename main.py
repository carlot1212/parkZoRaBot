from concurrent.futures import thread
import logging
from dotenv import load_dotenv
import os
import webserver
import datetime
import time

import discord
from discord.ext import commands, tasks

from scoring import player_scoring
from groceries import add_groceries, remove_groceries
from reminders import (
    weekly_period_reminder,
    daily_habits_reminder,
    monthly_rent_reminder as send_monthly_rent_reminder,
)


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

    if not period_reminder.is_running():
        period_reminder.start()
    if not monthly_rent_task.is_running():
        monthly_rent_task.start()
    if not habits_reminder.is_running():
        habits_reminder.start()

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")  

@bot.command()
async def scoring(ctx, game: str): 
    await player_scoring(ctx, game.capitalize(), bot)

@bot.command()
async def add(ctx):
    await add_groceries(ctx, bot)

@bot.command()
async def remove(ctx): 
    await remove_groceries(ctx, bot)

# def get_time(current_time):
#     if time.localtime().tm_isdst:
#         converted_time = datetime.time(hour=current_time + 9, minute=0)
#     else:
#         converted_time = datetime.time(hour=current_time + 8, minute=0)
#     return converted_time

@tasks.loop(time=datetime.time(hour=18, minute=0))
async def period_reminder():
    await weekly_period_reminder(bot)

@tasks.loop(time=datetime.time(hour=18, minute=30))  # Changed to 18:30 to avoid conflict
async def monthly_rent_task():
    await send_monthly_rent_reminder(bot)

@tasks.loop(time=datetime.time(hour=16, minute=0))
async def habits_reminder():
    await daily_habits_reminder(bot)


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
from concurrent.futures import thread
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
async def harmonies(ctx, players, HARMONIES):  

    def check(m):
        # Only accept messages from the same user in the same channel
        return m.author == ctx.author and m.channel == ctx.channel
    
    thread = await ctx.message.create_thread(name="Harmonies Scoring")

    thread.send("Who is playing?")
    response = await bot.wait_for('message', timeout=300.0, check=check)

    for question in questions:
        for player in players:
            await ctx.send(f"{player}, please answer the following question: {question}")
            try:
                # Wait for 30 seconds for a response
                response = await bot.wait_for('message', timeout=300.0, check=check)
                await ctx.send(f"You said: {response.content}")
            except:
                await ctx.send("You took too long!")

    await thread.send("How many tree points did Carlo getvfgyuj?") 
    await ctx.send(f"Started a thread for harmonies scoring: {thread.mention}")

HARMONIES = ["How many tree points did #{player} get?",
            "How many mountain points did #{player} get?",
            "How many plains points did #{player} get?",
            "How many building points did #{player} get?",
            "How many river points did #{player} get?",
            "How many habitat points did #{player} get?"
            ]

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
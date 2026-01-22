from concurrent.futures import thread
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver
from string import Template
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

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    await bot.process_commands(message)

HARMONIES = [Template("How many tree points did $player get?"),
            Template("How many mountain points did $player get?"),
            Template("How many plains points did $player get?"),
            Template("How many building points did $player get?"),
            Template("How many river points did $player get?"),
            Template("How many habitat points did $player get?"),
            Template("How many special habitat points did $player get?"),
            ]

@bot.command()
async def harmonies(ctx):  
    thread = await ctx.message.create_thread(name="Harmonies Scoring")

    await thread.send("Who is playing?")
    players_response = await bot.wait_for('message', timeout=300.0)
    players = players_response.content.split(", ")

    player_scoring = {player: 0 for player in players}
    for question in HARMONIES:
        for player in players:
            await thread.send(question.substitute(player=player))
            response = await bot.wait_for('message', timeout=300.0)
            points = int(response.content)
            player_scoring[player] += points

    await thread.send(f"{players[0]} scored {player_scoring[players[0]]} points and {players[1]} scored {player_scoring[players[1]]} points.")

    if player_scoring[players[0]] > player_scoring[players[1]]:
        await thread.send(f"{players[0]} wins!")
    elif player_scoring[players[1]] > player_scoring[players[0]]:
        await thread.send(f"{players[1]} wins!")
    else:
        await thread.send("It's a tie!")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
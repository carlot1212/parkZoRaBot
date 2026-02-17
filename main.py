import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver

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

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
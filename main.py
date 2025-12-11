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

secret_role = "sweaty gamer"

baby = "bubby cakes"

@bot.event
async def on_ready():
    Print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcoome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - say it again 2x!")

    if "get on" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - say it nicer")

    if "skibidi toilet" in message.content.lower():
        await message.edit()
        await message.channel.send(f"{message.author.mention} - dance time")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"wah sup mah dude {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def love(ctx):
    role = discord.utils.get(ctx.guild.roles, name=baby)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {baby}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="head count", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("😛")
    await poll_message.add_reaction("🤮")

@bot.command()
async def harmonies(ctx):
    await ctx.send("sfdgvgdsaf")    
    thread = await ctx.message.create_thread(name="Harmonies Scoring")
    await ctx.send("How many tree points did Carlo get?")
    

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("AYE welcome to the gang!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("NO. YOU GOTTA JOIN THE GANG FIRST!")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
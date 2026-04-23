import datetime
import discord

PERIOD_MESSAGES = [
    "It's the menstrual phase. It's period week no more peenar.....unless!",
    "It's the follicular phase. She's going back to normal!",
    "It's the ovulation phase. It's peenar time!",
    "It's the luteal phase. It's almost period week make sure to be extra nice!"
]

HABITS = {'not_aozora' : ['stretch 🧘‍♂️', 'greens 🥬'],
          'parkchou' : ['weigh ⚖️', 'list 🗒️', 'stretch 🧘‍♂️', 'greens 🥬', 'water 🍺']}

async def weekly_period_reminder(bot):
    if datetime.datetime.now().weekday() == 0:
        week_of_the_year = datetime.datetime.now().isocalendar()[1]
        message = PERIOD_MESSAGES[week_of_the_year % len(PERIOD_MESSAGES)]
        for guild in bot.guilds:
            channel = discord.utils.get(guild.channels, name='general')
            if channel:
                await channel.send(message)

async def daily_habits_reminder(bot):
    for guild in bot.guilds:
        channel = discord.utils.get(guild.channels, name='habits')
        if channel:
            for member in guild.members:
                if not member.bot:
                    await channel.send(f"{member.mention} Daily Habits: {', '.join(HABITS.get(member.name, []))}")
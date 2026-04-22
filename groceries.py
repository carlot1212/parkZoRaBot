import discord

async def add_groceries(ctx, bot):
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

async def remove_groceries(ctx, bot):
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
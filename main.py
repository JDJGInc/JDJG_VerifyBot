import discord, os, random, asyncio, re, typing
from discord.ext import commands
import ClientConfig, B

bot = ClientConfig.bot

async def status_task():
  await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Looking for Bots to verify"))
  await asyncio.sleep(40)
  await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | {len(bot.users)} users"))
  await asyncio.sleep(40)

async def startup():
  await bot.wait_until_ready()
  await status_task()

@bot.event
async def on_ready():
  print("Bot is Ready")
  print(f"Logged in as {bot.user}")
  print(f"Id: {bot.user.id}")


@bot.command()
async def addbot(ctx, arg=None,*,args=None):
  if arg is None:
    await ctx.send("Please provide an ID.")
  if arg:
    user=re.match(r'<@!?([0-9]+)>$', arg) or re.match(r'([0-9]{15,20})$', arg)
    if user:
      user_id = (user.group(1))
      try:
        user=await commands.UserConverter().convert(ctx,user_id)
      except commands.UserNotFound:
        user = None
      
      if args is None:
        await ctx.send("We don't add bots for no reason.")
      
      if args and user:
        if user.bot is False:
          await ctx.send("Please use a *bot* ID, not a *user* ID.")
        if user.bot:
          embed=discord.Embed(title="Verify Bot",timestamp=(ctx.message.created_at))
          embed.set_author(name=f"Bot Wanted: {user}",icon_url=(user.avatar_url))
          embed.set_footer(text=f"Bot's ID: {user.id}")
          jdjg=bot.get_user(168422909482762240)
          await bot.get_channel(816807453215424573).send(content=jdjg.mention,embed=embed)

          url = f'https://discordapp.com/oauth2/authorize?client_id={user.id}&scope=bot'
          description = f'{args}\n\n[Invite URL]({url})'
          embed = discord.Embed(title='Bot Request', colour=discord.Colour.blurple(), description=description)
          embed.add_field(name='Author', value=f'{ctx.author} (ID: {ctx.author.id})', inline=False)
          embed.add_field(name='Bot', value=f'{user} (ID: {user.id})', inline=False)
          embed.timestamp = ctx.message.created_at
          embed.set_footer(text=ctx.author.id)
          embed.set_author(name=user.id, icon_url=user.avatar_url_as(format='png'))  
          await bot.get_channel(816807453215424573).send(content=jdjg.mention,embed=embed)

      
    if user is None:
      await ctx.send("That's not a valid ID.")
    
B.b()
bot.loop.create_task(startup())
bot.run(os.environ["TOKEN"])

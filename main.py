import asyncio
import os
import random
import re
import sys
import traceback
import typing

import discord
from discord.ext import commands

import B
import ClientConfig

bot = ClientConfig.bot


async def status_task():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.playing, name="Looking for Bots to verify"),
    )
    await asyncio.sleep(40)
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | {len(bot.users)} users"
        ),
    )
    await asyncio.sleep(40)


async def startup():
    await bot.wait_until_ready()
    await status_task()


@bot.event
async def on_ready():
    print("Bot is Ready")
    print(f"Logged in as {bot.user}")
    print(f"Id: {bot.user.id}")


@bot.event
async def on_error(event, *args, **kwargs):
    more_information = sys.exc_info()
    error_wanted = traceback.format_exc()
    traceback.print_exc()
    # print(more_information[0])


@bot.command()
async def addbot(ctx, arg=None, *, args=None):
    if arg is None:
        await ctx.send("Please provide an ID.")

    if arg:
        user = re.match(r"<@!?([0-9]+)>$", arg) or re.match(r"([0-9]{15,20})$", arg)
        if user:
            user_id = user.group(1)
            try:
                user = await commands.UserConverter().convert(ctx, user_id)
            except commands.UserNotFound:
                user = None

            if args is None:
                await ctx.send("We don't add bots for no reason.")

            if args and user:
                if user.bot is False:
                    await ctx.send("Please use a *bot* ID, not a *user* ID.")
                if user.bot:
                    embed = discord.Embed(title="Verify Bot", timestamp=(ctx.message.created_at))
                    embed.set_author(name=f"Bot Wanted: {user}", icon_url=(user.display_avatar.url))
                    embed.set_footer(text=f"Bot's ID: {user.id}")
                    jdjg = bot.get_user(168422909482762240)
                    await bot.get_channel(816807453215424573).send(content=jdjg.mention, embed=embed)

                    url = f"https://discordapp.com/oauth2/authorize?client_id={user.id}&scope=bot"
                    description = f"{args}\n\n[Invite URL]({url})"
                    embed = discord.Embed(title="Bot Request", colour=discord.Colour.blurple(), description=description)
                    embed.add_field(name="Author", value=f"{ctx.author} (ID: {ctx.author.id})", inline=False)
                    embed.add_field(name="Bot", value=f"{user} (ID: {user.id})", inline=False)
                    embed.timestamp = ctx.message.created_at
                    embed.set_footer(text=ctx.author.id)
                    embed.set_author(name=user.id, icon_url=user.display_avatar.with_format("png"))
                    await bot.get_channel(816807453215424573).send(content=jdjg.mention, embed=embed)

                    await ctx.reply(
                        f"We notified the boss that you wanted to add the bot make sure your DMs are open so the boss can dm you on your request, if you don't open your dms to him, you will have your bot instantly denied, and you must request to add your own bot, not other people's bots. You msut also be in our guild.(for safety reasons). If you leave we will kick your bot :eyes:"
                    )

        if user is None:
            await ctx.send("That's not a valid ID.")


B.b()
bot.loop.create_task(startup())
bot.run(os.environ["TOKEN"])

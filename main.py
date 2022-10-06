import discord, asyncio, os
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
import nest_asyncio


intents = discord.Intents.all()
intents.message_content = True
prefix = '-'
bot = commands.Bot(
    command_prefix=prefix,
    intents=intents, 
    help_command=None)
color = 0xF93E3E 

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name=f'{prefix}help'))

@bot.event
async def on_command_error(error):
    if isinstance(error, commands.CommandNotFound):
        return

@bot.event
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
nest_asyncio.apply()
asyncio.run(load_cogs())

@bot.command()
async def help(ctx):
    embed=discord.Embed(
        title="List of commands:", 
        description= "Prefix: `{}`".format(prefix),
        color=color)
    embed.add_field(
        name=":raised_hands:  Fun",
        value="`choose` `penis` `iq` `clown` `reverse` `owo`",
        inline=False)
    embed.add_field(
        name=":musical_note:  Music Quiz", 
        value="`join` `mq` `nowplaying` `skip` `leave`", 
        inline=False)
    embed.add_field(
        name=":frame_photo:  Image", 
        value="`cat` `dog` `duck` `bird` `fox` `food` `coffee`", 
        inline=False)
    embed.add_field(
        name=":wrench:  Utility", 
        value="`ping` `speak`", 
        inline=False)
    await ctx.send(embed=embed)


keep_alive()
load_dotenv()
token = os.getenv("token")
bot.run(token)
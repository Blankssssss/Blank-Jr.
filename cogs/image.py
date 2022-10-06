import discord, requests
from discord.ext import commands
from main import color


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["birb"])
    async def bird(self, ctx):
        try:
            response = requests.get("https://some-random-api.ml/animal/birb").json()
            embed = discord.Embed(
                title="Here's a random bird image!",
                color=color)
            embed.set_image(url=response["image"])
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=discord.Embed(description="Something went wrong. Please try again later.", color=color))

    @commands.command(aliases=["meow", "neko"])
    async def cat(self, ctx):
        try:
            response = requests.get("https://api.thecatapi.com/v1/images/search").json()
            embed = discord.Embed(
                title="Here's a random cat image!",
                color=color)
            embed.set_image(url=response[0]["url"])
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=discord.Embed(description="Something went wrong. Please try again later.", color=color))

    @commands.command(aliases=["cafe"])
    async def coffee(self, ctx):
        try:
            response = requests.get("https://coffee.alexflipnote.dev/random.json").json()
            embed = discord.Embed(
                title="Here's a random coffee image!",
                color=color)
            embed.set_image(url=response["file"])
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=discord.Embed(description="Something went wrong. Please try again later.", color=color))

    @commands.command(aliases=["woof"])
    async def dog(self, ctx):
        try:
            response = requests.get("https://some-random-api.ml/animal/dog").json()
            embed = discord.Embed(
                title="Here's a random dog image!",
                color=color)
            embed.set_image(url=response["image"])
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=discord.Embed(description="Something went wrong. Please try again later.", color=color))

    @commands.command(aliases=["quack"])
    async def duck(self, ctx):
        try:
            response = requests.get("https://random-d.uk/api/v1/random").json()
            embed = discord.Embed(
                title="Here's a random duck image!",
                color=color)
            embed.set_image(url=response["url"])
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=discord.Embed(description="Something went wrong. Please try again later.", color=color))

    @commands.command(aliases=["dish", "meal"])
    async def food(self, ctx):
        try:
            response = requests.get("https://foodish-api.herokuapp.com/api").json()
            embed = discord.Embed(
                title="Here's a random food image!",
                color=color)
            embed.set_image(url=response["image"])
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=discord.Embed(description="Something went wrong. Please try again later.", color=color))

    @commands.command(aliases=["foxy"])
    async def fox(self, ctx):
        try:
            response = requests.get("https://some-random-api.ml/animal/fox").json()
            embed = discord.Embed(
                title="Here's a random fox image!",
                color=color)
            embed.set_image(url=response["image"])
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=discord.Embed(description="Something went wrong. Please try again later.", color=color))


async def setup(bot):
    await bot.add_cog(Image(bot))
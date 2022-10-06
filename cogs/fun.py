import discord, random
from discord.ext import commands
from main import prefix, color


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["random"])
    async def choose(self, ctx, *, choices: str):
        choiceslist = choices.split(",")
        await ctx.send(embed=discord.Embed(
            description="My choice is **{}**.".format(random.choice(choiceslist)),
            color=color))

    @commands.command(aliases=["pp"])
    async def penis(self, ctx, user: discord.Member):
        if user.bot is True:
            await ctx.send(embed=discord.Embed(
                description="That\'s a secret! ( ͡° ͜ʖ ͡°)", 
                color=color))
        else:
            size = random.randint(1, 50)
            dicksize = "=" * size
            await ctx.send(embed=discord.Embed(
                title=f"8{dicksize}D",
                description=
                "{}\'s penis is **{} cm** long.".format(user.display_name, str(size)),
                color=color))

    @commands.command(aliases=["rateiq", "iqrate"])
    async def iq(self, ctx, user: discord.Member):
        if user.bot is True:
            iq = random.randint(200, 500)
        else:
            iq = random.randint(-50, 200)
        if iq >= 160:
            emoji = "🧠"
        elif iq >= 100:
            emoji = "🤯"
        else:
            emoji = "😔"
        await ctx.send(embed=discord.Embed(
            description="{} has an IQ of **{}** {}".format(user.display_name, iq, emoji),
            color=color))

    @commands.command(aliases=["rateclown", "clownrate"])
    async def clown(self, ctx, user: discord.Member):
        if user.bot is True:
            rate = 1000
        else:
            rate = random.choice(range(1, 100))
        emoji = "🤡" 
        await ctx.send(embed=discord.Embed(
            description="{} is **{}%** clown {}".format(user.display_name, rate, emoji),
            color=color))

    @commands.command()
    async def owo(self, ctx, *, message):
        output = ''
        for word in message:
            output += f'{word}'
        output = output.replace('l', 'w')
        output = output.replace('r', 'w')
        output = output.replace('na', 'nya')
        output = output.replace('ne', 'nye')
        output = output.replace('ni', 'nyi')
        output = output.replace('no', 'nyo')
        output = output.replace('nu', 'nyu')
        output = output.replace('ove', 'uv')
        faces = ["(・`ω´・)", ";;w;;", "UwU", ">w<", "^w^", '(。O ω O。)']
        await ctx.send(embed=discord.Embed(
            title=f'{ctx.message.author.display_name} says:',
            description=output + ' ' + random.choice(faces),
            color=color))

    @commands.command(aliases=["reversetext", "rev"])
    async def reverse(self, ctx, *, message):
        def reverse_text(string):
            return string[::-1]
        await ctx.send(embed=discord.Embed(
            description=f"{reverse_text(message)}",
            color=color))

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"You need to provide at least one option. Example: **{prefix}choose `1,2,3`**.",
                color=color))

    @penis.error
    async def penis_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"Please use the correct command: **{prefix}penis `@user`**.",
                color=color))

    @iq.error
    async def iq_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"Please use the correct command: **{prefix}iq `@user`**.",
                color=color))

    @clown.error
    async def clown_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"Please use the correct command: **{prefix}clown `@user`**.",
                color=color))

    @owo.error
    async def owo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"Please use the correct command: **{prefix}owo `text`**.",
                color=color))

    @reverse.error
    async def reverse_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"Please use the correct command: **{prefix}reverse `text`**.",
                color=color))


async def setup(bot):
    await bot.add_cog(Fun(bot))
import discord, asyncio, os, os.path
from discord.ext import commands
from gtts import gTTS
from langdetect import detect
from mutagen.mp3 import MP3
from main import color, prefix


speech_file_path = "temp/speech.mp3"

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def connect(self, ctx):
        if not ctx.author.voice:
            await ctx.send(embed=discord.Embed(
                description="{} is not connected to a voice channel.".format(ctx.author.name),
                color=color))
            return
        else:
            await ctx.author.voice.channel.connect()

    @commands.command(aliases=["say", "s"])
    async def speak(self, ctx, *, message):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice == None:
            await self.connect(ctx)
        
        if len(message) > 500:
            await ctx.send(embed=discord.Embed(
                description="Your text is too long! (Max 500 characters)",
                color=color))
            return
        else:
            if len(os.listdir("temp")) != 0:
                await ctx.send(embed=discord.Embed(
                    description="I'm busy. Please try again later.",
                    color=color))
            else:
                try:
                    language = detect(message)
                    speech = gTTS(text=message, lang=language, slow=False, tld="com")
                    speech.save(speech_file_path)
                    ctx.message.guild.voice_client.play(
                        discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                        source=speech_file_path))
                    
                    file_length = MP3(speech_file_path).info.length
                    await asyncio.sleep(file_length)
                except Exception:
                    await ctx.send(embed=discord.Embed(
                        description="I'm busy. Please try again later.",
                        color=color))
                finally:
                    os.remove(speech_file_path)

    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(
            description=f"Your ping is **{round(self.bot.latency * 1000)} ms.**",
            color=color))

    @speak.error
    async def speak_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"Please use the correct command: **{prefix}speak `hello`**.",
                color=color))
    

async def setup(bot):
    await bot.add_cog(Utility(bot))
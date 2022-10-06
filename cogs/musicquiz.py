import discord, asyncio, random, yt_dlp, json, os, glob
from discord.ext import commands
from yt_dlp import YoutubeDL
from main import color, prefix


ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '/temp/%(title)s.mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

song_data_path_jp = "data/songs_jp.json"
song_data_path_kr = "data/songs_kr.json"
song_data_path_en = "data/songs_en.json"
song_file_path = "temp/*.mp3"

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1.0):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def song_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename), data=data)


class MusicQuiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open(song_data_path_jp) as f:
            data_jp = json.load(f)
        with open(song_data_path_kr) as f:
            data_kr = json.load(f)
        with open(song_data_path_en) as f:
            data_en = json.load(f)
        global data
        data = [data_jp, data_kr, data_en]
        self.song_data = data

    async def connect(self, ctx):
        if not ctx.author.voice:
            await ctx.send(embed=discord.Embed(
                description="{} is not connected to a voice channel.".format(ctx.author.name),
                color=color))
            return
        else:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
    
    async def disconnect(self, ctx):
        if bot_in_voice(self.bot, ctx) is True:
            server = ctx.message.guild
            voice_channel = server.voice_client
            await voice_channel.disconnect()
        else:
            return
        clear_files()

    async def stop(self, ctx):
        if bot_in_voice(self.bot, ctx) is True:
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_channel.stop()
        else:
            return
        
    async def play_song(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        song_index = random.randint(0, len(self.song_data)-1)
        global title, url
        title = self.song_data[song_index][0]
        url = self.song_data[song_index][1]

        try:
            player = await YTDLSource.song_url(url, loop=self.bot.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except AttributeError:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        answer = message.content
        try:
            if title is not None:
                if answer.lower() == title.lower():
                    await message.channel.send(embed=discord.Embed(
                        description="{} is correct! The song was **{}**.".format(message.author.name, title),
                        color=color))
                    ctx = await self.bot.get_context(message)
                    await self.stop(ctx)
                    await self.play_song(ctx)
        except NameError:
            pass

    @commands.command(aliases=["j"])
    async def join(self, ctx):
        await self.connect(ctx)

    @commands.command(aliases=["mq", "start", "startquiz"], pass_context=True)
    async def musicquiz(self, ctx, message):
        await self.stop(ctx)
        await asyncio.sleep(0.5)
        
        if bot_in_voice(self.bot, ctx) is False:
            await self.connect(ctx)
        if message == "jp":
            self.song_data = data[0]
        elif message == "kr":
            self.song_data = data[1]
        elif message == "en":
            self.song_data = data[2]
        else:
            await ctx.send(embed=discord.Embed(
                description="Invalid command. Please try again.",
                color=color))
            return
        await self.play_song(ctx)

        await ctx.send(embed=discord.Embed(
            description='''
            Try guessing the name of this song by typing in this channel!
You can use **{}np** to view the name, or **{}skip** to play the next song.
            '''.format(prefix, prefix),
            color=color))

    @musicquiz.error
    async def musicquiz_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"You need specify the songs' language. Example: **{prefix}mq `jp/kr/en`**.",
                color=color))

    @commands.command(aliases=["np"])
    async def nowplaying(self, ctx):
        if bot_in_voice(self.bot, ctx) is False:
            await ctx.send(embed=discord.Embed(
            description="I am not connected to a voice channel.",
            color=color))
        else:
            try:
                if title == None:
                    await ctx.send(embed=discord.Embed(
                        description="No music is playing!",
                        color=color))
                else:
                    video_info = ytdl.extract_info(url, download=False)
                    video_title = video_info.get("title", None)
                    videoID = url.split("watch?v=")[1].split("&")[0]

                    embed=discord.Embed(
                        title="Now playing:",
                        description="[{}]({})".format(video_title, url),
                        color=color)
                    embed.set_thumbnail(url= "https://img.youtube.com/vi/{}/0.jpg".format(videoID))
                    await ctx.send(embed=embed)
            except Exception:
                pass

    @commands.command(aliases=["next"])
    async def skip(self, ctx):
        if bot_in_voice(self.bot, ctx) is False:
            await ctx.send(embed=discord.Embed(
            description="I am not connected to a voice channel.",
            color=color))
        else:
            try:
                if title == None:
                    await ctx.send(embed=discord.Embed(
                        description="No music is playing!",
                        color=color))
                else:
                    await ctx.send(embed=discord.Embed(
                        description=f"Skipped! The song was **{title}**.",
                        color=color))
                    await self.stop(ctx)
                    await asyncio.sleep(1)
                    await self.play_song(ctx)
            except Exception:
                pass

    @commands.command(aliases=["stop", "stopquiz", "bye"])
    async def leave(self, ctx):
        if bot_in_voice(self.bot, ctx) is False:
            await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel.",
                color=color))
            clear_files()
        else:
            await self.stop(ctx)
            await asyncio.sleep(1)
            await self.disconnect(ctx)
            await ctx.send(embed=discord.Embed(
                description="Left the voice channel.",
                color=color))

def bot_in_voice(bot, ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        return True
    else:
        return False

def clear_files():
    files = glob.glob(song_file_path)
    for f in files:
        os.remove(f)

async def setup(bot):
    await bot.add_cog(MusicQuiz(bot))
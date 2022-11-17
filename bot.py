import discord
from discord.ext import commands
from discord.ext.commands import bot
from pytube import YouTube
import os
import re
from dotenv import load_dotenv


def run_discord_bot():

    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='.', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

        @bot.event
        async def on_message(message):
            ctx = await bot.get_context(message)
            if message.author == bot.user:
                return

            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f'{username} in {channel}: {user_message}')
            if user_message[0:3] == '!yt':
                videoLink = user_message[4:]
                videoName = download_video(videoLink, ctx)
                print(f'{videoName}.mp3')
                await ctx.send(videoName, file=discord.File(f'{videoName}.mp3'))
                os.remove(f'{videoName}.mp3')
                

    bot.run(TOKEN)

def download_video(videoLink , ctx):
    yt = YouTube(videoLink)
    
    # Extracting only audio
    video = yt.streams.filter(only_audio=True).first()
    videoName = re.sub('[^A-Za-z0-9]+', '', yt.title)
    out_file = video.download(filename=videoName)

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

      
    # result of success
    print(videoName + " has been successfully downloaded.")
    
    return videoName
    
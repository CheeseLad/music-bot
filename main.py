#!/usr/bin/env python3

import subprocess
import yt_dlp
import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from config import token
import time

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def download_audio(video_id, output_path='./'):
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path + '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)

def search_audio(search_query):
  command = ['yt-dlp', '--get-id', '--get-title']
  command.insert(1, f'ytsearch1:"{search_query}"')
  result = subprocess.run(command, capture_output=True, text=True)
  data = result.stdout.split('\n')
  if data[0] + ".mp3" in os.listdir('cache/'):
    print("File already exists! Skipping download...")
    return data[0] + ".mp3"
  else:
    download_audio(data[1], 'cache/')
    time.sleep(5)
    return data[0] + ".mp3"


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, *, search_query):
    channel = ctx.author.voice.channel
    file = search_audio(search_query)
    voice_channel = await channel.connect()

    audio_source = f'cache/{file}'  # Replace with the path to your audio file
    await ctx.send(f'Playing {file.strip(".mp3")}')
    voice_channel.play(FFmpegPCMAudio(audio_source), after=lambda e: print('Player error: %s' % e) if e else None)
    
    ctx.voice_client.disconnect()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command. Type !help for a list of commands.')

# Replace 'TOKEN' with your bot token
bot.run(token)
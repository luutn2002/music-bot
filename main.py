import discord
from discord import app_commands
import os
from youtube_search import YoutubeSearch
from buttons import SearchAndAddButtonsView
import urllib
import re
from dotenv import load_dotenv
from playlist import Playlist
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import yt_dlp
import asyncio
import glob

load_dotenv()

ydl_opts = {
  'outtmpl': 'ytbsong.mp3',
  'format': 'bestaudio',
  'postprocessors': [
        {'key': 'SponsorBlock'},
        {'key': 'ModifyChapters', 'remove_sponsor_segments': ['sponsor', 
                                                              'intro', 
                                                              'outro', 
                                                              'selfpromo', 
                                                              'preview', 
                                                              'filler', 
                                                              'interaction', 
                                                              'music_offtopic']}
    ],
  'extract_audio': True
}

token = os.environ['DISCORD_TOKEN']
public_key = os.environ['PUBLIC_KEY']
app_id = os.environ['APP_ID']
dev_id = os.environ['DEV_USER_ID']

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

playlist = Playlist()

def check_vc_connected(interaction):
  for vc in client.voice_clients:
    #check if voice client is already connect
    if interaction.user.voice.channel and interaction.user.voice.channel == vc.channel:
      return True
    
  return False

def get_connected_vc(interaction):
  for vc in client.voice_clients:
    #check if voice client is already connect
    if interaction.user.voice.channel and interaction.user.voice.channel == vc.channel:
      return vc
    
def clear_download_cache():
  for filename in glob.glob("ytbsong*"):
    os.remove(filename) 


async def play_entire_playlist(interaction, vc):
  while(not playlist.song.empty):
    current_song = playlist.get_first()
    await interaction.channel.send(embed=discord.Embed(title=f"Playing: {current_song['name']}", color=0x00ff00))

    #clear cache before download song
    clear_download_cache()
    ytdl = yt_dlp.YoutubeDL(ydl_opts)
    try:
      #download
      ytdl.download(current_song['download_link'])
    except:
      pass

    #play the song ofc
    playlist.drop_first() #Drop downloaded song from playlist
    source = PCMVolumeTransformer(FFmpegPCMAudio(source='ytbsong.mp3'), volume=0.5)
    vc.play(source)
    while vc.is_playing():
      await asyncio.sleep(1)

@tree.command(name="play",
              description="Play some music from playlist")
async def play(interaction):
  #check user of command is in voice channel
  if interaction.user.voice:

    #check empty playlist
    if playlist.song.empty:
      await interaction.response.send_message("Current playlist is empty, please add something to it first.")

    #execute if playlist not empty
    else:
      #connect to channel if not connected to any
      if not check_vc_connected(interaction):
        vc = await interaction.user.voice.channel.connect()
      else:
        vc = get_connected_vc(interaction)
      
      #Check for any playing song
      if vc.is_playing():
        await interaction.response.send_message("Bot is playing a song, please use skip if you want to play the next song.")

      #Now download and play the first song from playlist
      else:
        await interaction.response.send_message("Bot is now playing from playlist.")
        await play_entire_playlist(interaction, vc)
        
  #tell user to connect to voice first
  else:
    await interaction.response.send_message("Please connect to a voice channel to use this command.")

@tree.command(name="search_and_add",
              description="Add music to playlist by youtube keyword searching.")
async def search_and_add(interaction, search_word: str):

  #embed message
  embedVar = discord.Embed(
    title="Showing results from Youtube. Please select a track from the buttons below.",
    color=0x00ff00)
  
  #search result
  results = YoutubeSearch(search_word, max_results=5).to_dict()

  #cache of result
  name_cache = []
  url_cache = []
  #print(results)
  for i, v in enumerate(results):
    embedVar.add_field(
      name=f'{(i+1)}. {v["title"]}',
      value=
      f'Duration: {v["duration"]}, channel: {v["channel"]}, views: {v["views"]}',
      inline=False)
    name_cache.append([v["title"]])
    url_cache.append(f'https://www.youtube.com{v["url_suffix"]}')

  await interaction.response.send_message(embed=embedVar,
                                          view=SearchAndAddButtonsView(playlist,
                                                                       name_cache,
                                                                       url_cache))

@tree.command(name="stop",
              description="Disconnect if bot is in voice channel.")
async def stop(interaction):
  if interaction.user.voice:

    if check_vc_connected(interaction):
      vc = get_connected_vc(interaction)
      await vc.disconnect()
      clear_download_cache()
      await interaction.response.send_message('Bot disconnected from voice channel.')

    else:
      await interaction.response.send_message('Bot not connected to any voice channel.')

  else:
    await interaction.response.send_message('You have to be connected to the same voice channel to disconnect me.')

@tree.command(name="pause",
              description="Pause any playing song.")
async def stop(interaction):
  if interaction.user.voice:

    if check_vc_connected(interaction):
      vc = get_connected_vc(interaction)
      if vc.is_playing():
        vc.pause()
        await interaction.response.send_message('Bot paused playing song.')
      else:
        await interaction.response.send_message('No song is being played.')

    else:
      await interaction.response.send_message('Bot not connected to any voice channel.')

  else:
    await interaction.response.send_message('You have to be connected to the same voice channel to pause me.')

@tree.command(name="check_playlist",
              description="View current playlist.")
async def check_playlist(interaction):
  embedVar = discord.Embed(
    title="Current playlist:",
    color=0x00ff00)
  for index, row in playlist.song.iterrows():
    embedVar.add_field(
      name=f'{(index+1)}. {row["name"]}',
      value="",
      inline=False)
  await interaction.response.send_message(embed=embedVar)

@tree.command(name="resume",
              description="Resume any playing song.")
async def stop(interaction):
  if interaction.user.voice:

    if check_vc_connected(interaction):
      vc = get_connected_vc(interaction)
      if vc.is_paused():
        vc.resume()
        await interaction.response.send_message('Bot resumed playing song.')
      else:
        await interaction.response.send_message('No song is being paused.')

    else:
      await interaction.response.send_message('Bot not connected to any voice channel.')

  else:
    await interaction.response.send_message('You have to be connected to the same voice channel to resume song.')

@tree.command(name='skip', description='Skip playing song.')
async def skip(interaction):
  if interaction.user.voice:

    if check_vc_connected(interaction):
      vc = get_connected_vc(interaction)
      if vc.is_playing():
        vc.stop()
        await interaction.response.send_message('Bot skipped playing song.')
        await play_entire_playlist(interaction, vc)
      else:
        await interaction.response.send_message('No song is being play.')

    else:
      await interaction.response.send_message('Bot not connected to any voice channel.')

  else:
    await interaction.response.send_message('You have to be connected to the same voice channel to skip song.')

@tree.command(name='sync', description='Sync bot command, for developer only.')
async def sync(interaction: discord.Interaction):
  if int(interaction.user.id) == int(dev_id):
    await tree.sync()
    await interaction.response.send_message('Command tree synced.')
  else:
    await interaction.response.send_message('You must be the owner to use this command!')

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(
    type=discord.ActivityType.listening, name="a melody"))
  
if __name__ == '__main__':
  client.run(token)

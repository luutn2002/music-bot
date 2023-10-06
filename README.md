# music-bot
A python music bot for discord server to pull youtube music to voice channel.
## Usage
This bot was originally ran on Ubuntu, so there are only official conda support running.
### Environment setup:
Clone the repo:
```
git clone https://github.com/luutn2002/music-bot.git
```
Create conda environment with:
```
conda create --name {your env name} python=3.8
```
Download requirements and add some of your credentials to a .env file:
```
conda activate  {your env name}
cd music_bot
pip install -r requirements.txt
sudo nano .env
```
Run the bot:
```
python3 music_bot.py
```
### Discord command: 
```/search_and_add``` search for a youtube keyword, select an element to add to your playlist.

```/play``` play songs in playlist and pop it, will stop playing if there are no song left in playlist

```/stop``` disconnect bot from voice channel.

```/skip``` skip current song.

```/pause``` pause current song.

```/resume``` resume song if any are paused.

```/sync``` sync newly added command to bot, for developer.

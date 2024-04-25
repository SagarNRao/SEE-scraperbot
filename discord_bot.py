import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from auxiliary import Scraper
import time

load_dotenv()        

obj = Scraper()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.command()
async def search(ctx, *args):
    arguments = ' '.join(args)
    obj.get_videos(arguments)
    for key in obj.video_dict:
        link = ""
        link = "https://youtube.com" + str(obj.video_dict[key])
        await ctx.send(f'{key}: \n {link}')
        time.sleep(2)
    await ctx.send('Done!')
    
@bot.command()
async def summary(ctx, *args):
    arguments = ' '.join(args)
    if arguments.startswith('index-'):
        try:
            idx = int(arguments[6:])
            keys = list(obj.video_dict.keys())
            key = keys[idx]
            link = obj.video_dict[key]
            summary = obj.get_video_summary(link)
            await ctx.send(f'Here\'s a summay of the video {key}:\n{summary}')
        except:
            await ctx.send('Invalid Command (number likely missing)')

@bot.command()
async def help(ctx):
    options = '''```!search <search querey>```\nShows a list of search results that would appear if you searched the query on YouTube.\n```!summary <query>```\nIf you have already used the !search command before, you can replace the <query> with index-xyz to get the summary for a video from the search results.\nExample: `!summary index-2` will return the summary for the second video from the search results.'''
    await ctx.send(f'**Here is a list of commands:**\n{options}')

bot_token = os.getenv('BOT_TEST_KEY')
bot.run(bot_token)
import discord
from discord.ext import commands
import pywhatkit

import requests
import pandas as pd
import aiohttp
import asyncio


# from apicall import recommendations, length


intents = discord.Intents.default()  # Create an instance of the default intents
client = commands.Bot(command_prefix='!', intents=intents)

search_key_words = ""


@client.event
async def on_ready():
    print('online')


@client.command(aliases=['yt'])
async def youtube(ctx, *, query):
    response = pywhatkit.playonyt(query, open_video=False)
    await ctx.reply(response)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!Search"):
        search_query = message.content[len("!Search"):].lstrip()
        # Create the context
        ctx = await client.get_context(message)
        # Invoke the youtube command
        await ctx.invoke(client.get_command('youtube'), query=search_query)
    if message.content.startswith("!Recommend"):
        words = message.content.split()
        start_index = words.index("!Recommend") if "!Recommend" in words else 0
        end_index = words.index("<@1226551721451585596>")

        search_key_words = words[start_index + 1:end_index]
        search_key_words_str = ' '.join(search_key_words)
        print(search_key_words_str)

        url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=" + \
            str(search_key_words) + \
            "&key=AIzaSyBjfBhJjjdQOAYtcbuRCc_9-0gwUR3d1O0&maxResults=5"

        response = requests.get(url)
        json = response.json()

        df = pd.json_normalize(json['items'])

        # now to get the urls out of the csv
        length = df.shape[0]
        recommendations = []
        youtube_search_standard = "https://www.youtube.com/watch?v="

        for i in range(length):
            to_append = [youtube_search_standard +
                         str(df.loc[i, 'id.videoId'])]
            recommendations.append(to_append)
            df.to_csv('reee.csv', index=False)

        await message.channel.send("Of course! Here are some recommendations!")
        for i in range(length):
            await message.channel.send(recommendations[i])


# client.run(os.getenv('TOKEN'))

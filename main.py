import discord
from discord.ext import commands 
import requests
import asyncio
import aiofiles 
import aiohttp
import re 
import json

bot = commands.Bot(command_prefix="x!")

serverurl = ""
# put your sharex body/form data into here
body = { 
    "key": "example",
    "method": "json",   
    }
imagedir = "" # /i/ as example
@bot.event
async def on_ready():
    print("Connected to API")


@bot.command()
async def upload(ctx, file=""):
    if file:
        url = file
    else:
        try:
            url = ctx.message.attachments[0].url
        except IndexError as e:
            return await ctx.send("No attachment found")
    if not url.endswith(".png") and not url.endswith(".gif") and not url.endswith(".jpg") and not url.endswith(".jpeg"):
        return await ctx.send("File type not supported.")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                search = re.search("([^.]+$)", url)
                ext = search.group(1)
                s = await aiofiles.open('cache/x.{}'.format(ext), mode="wb")
                await s.write(await resp.read())
                await s.close()
    # upload part 
    rurl = "https://jelbrek.icu/upload.php"
    files = {
        'file': open('cache/x.{}'.format(ext), 'rb')
    }
    r = requests.post(rurl, files=dict(files), data=body)
    if r.status_code == 200:
        # parse json
        decode = r.content.decode("utf-8") # convert bytes to string 
        x = json.loads(decode)
        await ctx.send("https:/serverurl/i/" + x["filename"])
    else:
        return await ctx.send("Something went wrong uploading.")





bot.run("NjY4NDI0MzIwNDIyMzc5NTMz.Xisb0g.tGft2ooSsmq9dvMMB-hw0i5xlmY")

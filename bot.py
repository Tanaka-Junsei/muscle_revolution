import asyncio
import datetime
import os
import random
import discord
import logging
from dotenv import load_dotenv
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('PROD_CHANNEL_ID'))
# CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))
TARGET_USER_ID = int(os.getenv('TARGET_USER_ID'))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

NEXT_POST_TIME = None
JST = pytz.timezone('Asia/Tokyo')

# 起動時チェック
@client.event
async def on_ready():
    logging.info('logged in as {0.user}'.format(client))
    client.loop.create_task(check_next_post_time())

async def check_next_post_time():
    global NEXT_POST_TIME
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    while not client.is_closed():
        if NEXT_POST_TIME and datetime.datetime.now(JST) >= NEXT_POST_TIME:
            user = await client.fetch_user(TARGET_USER_ID)
            await channel.send(f'{user.mention} KAZUO is WATCHING YOU')
            NEXT_POST_TIME = None
        await asyncio.sleep(60)

# メッセージ受信時
@client.event
async def on_message(message):
    global NEXT_POST_TIME

    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    if message.content == '/muscle':
        await message.reply('痩せろデブ')
        return

    if message.author.id != TARGET_USER_ID:
        if random.random() < 0.1:
            await message.reply('お前もマッチョにならないか？')
        return

    if not message.attachments:
        return

    for attachment in message.attachments:
        if attachment.content_type.startswith('image/'):
            NEXT_POST_TIME = datetime.datetime.now(JST) + datetime.timedelta(days=1, hours=2)
            await message.reply(f'次は {NEXT_POST_TIME.strftime("%Y-%m-%d %H:%M:%S")} まで')
            return 

client.run(TOKEN)
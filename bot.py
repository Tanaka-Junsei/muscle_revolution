import asyncio
import datetime
import os
import random
import discord
import logging
from dotenv import load_dotenv

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('PROD_CHANNEL_ID'))
# CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))
TARGET_USER_ID = int(os.getenv('TARGET_USER_ID'))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

NEXT_POST_TIME = None

# 起動時チェック
@client.event
async def on_ready():
    logging.info('logged in as {0.user}'.format(client))
    # ループで次の投稿時間をチェック
    client.loop.create_task(check_next_post_time())

# NEXT_POST_TIMEになった時に、指定のチャンネルにメッセージを送信
async def check_next_post_time():
    global NEXT_POST_TIME
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    while not client.is_closed():
        # 次の投稿時間になったらメッセージを送信
        if NEXT_POST_TIME and datetime.datetime.now() >= NEXT_POST_TIME:
            await channel.send('KAZUO is WATCHING YOU')
            NEXT_POST_TIME = None
        await asyncio.sleep(60)

# メッセージ受信時
@client.event
async def on_message(message):
    global NEXT_POST_TIME
    if message.channel.id != CHANNEL_ID:
        return
    if message.author.bot:
        return
    if message.content == '/muscle':
        await message.reply('痩せろデブ')
        return
    # 画像を送信してから次の投稿までの時間を返信
    if message.author.id == TARGET_USER_ID:
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image/'):
                    # 次の画像の投稿時間を設定
                    NEXT_POST_TIME = datetime.datetime.now() + datetime.timedelta(days=1, hours=2)
                    await message.reply(f'次は {NEXT_POST_TIME.strftime("%Y-%m-%d %H:%M:%S")} まで')
                    return
    else:
        # 10%の確率でメッセージを送信
        if random.random() < 0.1:
            await message.reply('お前もマッチョにならないか？')
            return

client.run(TOKEN)

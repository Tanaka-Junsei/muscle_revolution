from dotenv import load_dotenv
import os
import discord
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
# CHANNEL_ID = int(os.getenv('PROD_CHANNEL_ID'))
CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# 起動時チェック
@client.event
async def on_ready():
    logging.info('ログインしました')
    logging.info(CHANNEL_ID)

# メッセージ受信時
@client.event
async def on_message(message):
    logging.info(message.channel.id)
    if message.channel.id != CHANNEL_ID:
        return
    if message.author.bot:
        return
    if message.content == '/neko':
        await message.channel.send('にゃーん')

client.run(TOKEN)

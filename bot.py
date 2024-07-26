from dotenv import load_dotenv
import os
import discord
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# .env ファイルを読み込む
load_dotenv()

# 自分のBotのアクセストークンを取得
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# トークンが正しく読み込まれているかを確認（デバッグ用）
if TOKEN is None:
    logging.error("DISCORD_BOT_TOKEN is not set")
else:
    logging.info(f"Token: {TOKEN}")

# 必要なintentsを設定
intents = discord.Intents.default()
intents.messages = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# 起動時に動作する処理
@client.event
async def on_ready():
    logging.info('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    logging.info(f'メッセージを受信しました: {message.content}')
    if message.author.bot:
        logging.info('Botからのメッセージは無視します')
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == 'おっぱい':
        await message.channel.send('ちくび')
        logging.info('ちくび と返しました')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

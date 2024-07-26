# bot.py

from dotenv import load_dotenv
import os
import discord

# .env ファイルを読み込む
load_dotenv()

# 自分のBotのアクセストークンを取得
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 必要なintentsを設定
intents = discord.Intents.default()
intents.messages = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('ちくび')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

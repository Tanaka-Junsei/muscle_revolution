import asyncio
import datetime
from datetime import datetime, timezone, timedelta
import os
import random
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv
import pytz
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('PROD_CHANNEL_ID'))
# CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))
TARGET_USER_ID = int(os.getenv('TARGET_USER_ID'))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

NEXT_POST_TIME = None
JST = pytz.timezone('Asia/Tokyo')

@bot.event
async def on_ready():
    logging.info(f'logged in as {bot.user}')
    bot.loop.create_task(watch_next_post_time())


@bot.event
async def on_message(message):
    global NEXT_POST_TIME

    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    await bot.process_commands(message)

    if message.author.id != TARGET_USER_ID:
        if random.random() < 0.1:
            await message.reply('お前もマッチョにならないか？')
        return

    if not message.attachments:
        return

    for attachment in message.attachments:
        if attachment.content_type and attachment.content_type.startswith('image/'):
            NEXT_POST_TIME = datetime.now(JST) + timedelta(days=1, hours=2)
            await message.reply(f'次は {NEXT_POST_TIME.strftime("%Y-%m-%d %H:%M:%S")} まで')
            return


async def watch_next_post_time():
    global NEXT_POST_TIME
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)

    while not bot.is_closed():
        # 時間になったらメッセージ送信
        if NEXT_POST_TIME and datetime.now(JST) >= NEXT_POST_TIME:
            user = await bot.fetch_user(TARGET_USER_ID)
            await channel.send(f'{user.mention} KAZUO is WATCHING YOU')
            NEXT_POST_TIME = None

        # 1分おきに確認
        await asyncio.sleep(60)


def is_valid_channel(ctx):
    return ctx.channel.id == CHANNEL_ID


async def fetch_weight_data(channel, after_date):
    messages = [msg async for msg in channel.history(limit=1000, after=after_date)]

    weights = []
    dates = []

    for msg in messages:
        try:
            number = float(msg.content)
            created_at_jst = msg.created_at.astimezone(JST)
            weights.append(number)
            dates.append(created_at_jst)
        except ValueError:
            pass

    return weights, dates


def generate_weight_graph(dates, weights, filename='graph.png'):
    plt.plot(dates, weights, marker='o')
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date')
    plt.ylabel('Weight (kg)')
    plt.title('Weight Over Time')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


@bot.command(name="muscle")
async def muscle_command(ctx):
    if not is_valid_channel(ctx):
        return
    await ctx.reply("痩せろデブ")


@bot.command(name="graph")
async def graph_command(ctx):
    if not is_valid_channel(ctx):
        return

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        logging.warning("Channel not found.")
        return

    start_date_jst = datetime(2025, 1, 7, tzinfo=JST)
    start_date_utc = start_date_jst.astimezone(timezone.utc)

    weights, dates = await fetch_weight_data(channel, after_date=start_date_utc)

    if not weights:
        logging.warning("No weight data found.")
        return

    generate_weight_graph(dates, weights, 'graph.png')

    await ctx.send(file=discord.File('graph.png'))

bot.run(TOKEN)

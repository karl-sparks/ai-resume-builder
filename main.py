import logging
import os

import discord
from discord.message import Message

from dotenv import load_dotenv

from src.sparks_ai import SparksAI

load_dotenv()

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()

intents.message_content = True
intents.presences = True

client = discord.Client(intents=intents)

sparks_ai = SparksAI()


@client.event
async def on_ready():
    logging.info("Logged in as: %s", client.user)


@client.event
async def on_message(msg: Message):
    if msg.author == client.user:
        return

    await sparks_ai.handle_message(msg)


client.run(os.getenv("DISCORD_TOKEN"))

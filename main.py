import logging
import os

import discord
from discord.message import Message

from dotenv import load_dotenv

from SparksAI.sparksai import SparksAI

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

    username = str(msg.author).split("#", maxsplit=1)[0]
    user_message = str(msg.content)

    initial_sent_msg = None
    message_to_send = ""
    buffer = 0
    inside_code = False
    resend_msg = True

    for chunk in sparks_ai.notice_message(username=username, msg=user_message):
        message_to_send += chunk
        if resend_msg and message_to_send.strip():
            initial_sent_msg = await msg.channel.send(message_to_send)
            resend_msg = False

        if message_to_send[-3:] == "```":
            if inside_code:
                await initial_sent_msg.edit(content=message_to_send)
                message_to_send = ""
                resend_msg = True
                buffer = 0
            else:
                await initial_sent_msg.edit(content=message_to_send[:-3])
                resend_msg = True
                message_to_send = message_to_send[-3:]
                buffer = 0

            inside_code = not inside_code

        if len(message_to_send) > 1500 and chunk == "\n":
            await initial_sent_msg.edit(content=message_to_send)
            resend_msg = True
            message_to_send = ""
        elif len(message_to_send) > 1999:
            await initial_sent_msg.edit(content=message_to_send)
            resend_msg = True
            message_to_send = ""
        else:
            if buffer > 300:
                await initial_sent_msg.edit(content=message_to_send)
                buffer = 0
            else:
                buffer += 1

    if message_to_send:
        await initial_sent_msg.edit(content=message_to_send)


client.run(os.getenv("DISCORD_TOKEN"))

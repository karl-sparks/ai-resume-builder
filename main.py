import logging
import os
import re
from typing import Optional
import asyncio

import discord
from discord.message import Message
from discord import errors, DMChannel

from dotenv import load_dotenv

from SparksAI.sparksai import SparksAI
from SparksAI.config import MAX_MESSAGE_LENGTH, BUFFER_SIZE

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


def is_inside_code_block(text):
    """Check if the current context is inside a code block."""
    return len(re.findall(r"```", text)) % 2 != 0


def should_split_message(message):
    """Determine if the message should be split based on length"""
    return len(message) >= MAX_MESSAGE_LENGTH


def split_and_send_message(
    message: str, sent_msg: Message, channel
) -> (str, Optional[Message]):
    """Split the message and handle code blocks if the message exceeds max length."""
    if is_inside_code_block(message):
        # If inside a code block, split at the max length and add code block delimiters
        split_point = len(message)
        first_part = (
            message[:split_point] + "```"
        )  # End the first part with a code block delimiter
        second_part = (
            "```" + message[split_point:]
        )  # Start the second part with a code block delimiter
    else:
        # Find a suitable split point outside of a code block
        split_point = message.rfind("\n") + 1
        if split_point > 0:
            first_part = message[:split_point]
            second_part = message[split_point:]
        else:
            # If no suitable split point is found, split at the max length
            first_part = message
            second_part = ""

    # Send the first part as a new message
    asyncio.create_task(send_and_log_message(first_part, sent_msg, channel))

    return second_part, None


async def send_and_log_message(
    content: str, sent_msg: Optional[Message], channel
) -> Message:
    """Send and log the message."""
    try:
        if not sent_msg:
            sent_msg = await channel.send(content)
        else:
            await sent_msg.edit(content=content)
        return sent_msg
    except errors.HTTPException as e:
        logging.error("Error sending message: %s", e)
        return sent_msg


@client.event
async def on_message(msg: Message):
    if msg.author == client.user:
        return

    if not isinstance(msg.channel, DMChannel):
        return

    username = str(msg.author).split("#", maxsplit=1)[0]
    user_message = str(msg.content)

    message_to_send = ""
    buffer = 0
    sent_msg = None

    async for chunk_a in await sparks_ai.notice_message(
        username=username,
        msg=user_message,
        run_id=f"{username}_{msg.channel.id}_{msg.id}",
    ):
        chunk = chunk_a  # This in place until proper streaming is support by OpenAI Assistants
        message_to_send += chunk

        if should_split_message(message_to_send):
            message_to_send, sent_msg = split_and_send_message(
                message_to_send, sent_msg, msg.channel
            )

        if buffer > BUFFER_SIZE:
            sent_msg = await send_and_log_message(
                content=message_to_send,
                sent_msg=sent_msg,
                channel=msg.channel,
            )
            buffer = 0
        else:
            buffer += len(chunk)

    if message_to_send:
        sparks_ai.memory.get_convo_mem(username=username).add_ai_message(
            message_to_send
        )
        await send_and_log_message(message_to_send, sent_msg, msg.channel)


client.run(os.getenv("DISCORD_TOKEN"))

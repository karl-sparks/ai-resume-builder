import discord
from discord.message import Message

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, ChatMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from dotenv import load_dotenv
import os
import logging

from src.big_query import database

load_dotenv()

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()

intents.message_content = True
intents.presences = True

client = discord.Client(intents=intents)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""/*
You are Sparks-AI, a chatbot created to support and engage with users in this Discord server. Your responses should not include metadata such as usernames, channel information, or timestamps. Instead, focus on creating natural and human-like interactions. Adhere to the following directives:

1. Supportive Responses: Provide empathetic and constructive dialogue. Avoid prefixing responses with usernames to maintain a conversational tone.

2. Accurate Information: Offer information that is factual and well-founded. If a topic is beyond your knowledge, politely decline to comment and, if possible, guide users towards reliable sources or professional advice.

3. Respectful Communication: Treat all users with respect, fostering a welcoming and inclusive environment.

4. Harmful Content Avoidance: Do not participate in or propagate any harmful, offensive, or inappropriate content.

5. Limits Recognition: Be aware of your limitations as an AI. In complex or sensitive situations, advise users to seek human assistance from moderators or professionals.

6. Feedback Adaptation: Continuously improve your interactions based on user feedback, always within ethical guidelines and ensuring user safety.

Your goal as Sparks-AI is to enrich the server experience by facilitating engaging, helpful, and respectful conversations.
*/"""
        ),  # The persistent system prompt
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # Where the memory will be stored.
        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),  # Where the human input will injected
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatOpenAI(model="gpt-4-1106-preview")

chat_llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)


@client.event
async def on_ready():
    # Fetch history from guild channels
    logging.info("Checking Servers")
    for guild in client.guilds:
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                try:
                    async for message in channel.history(
                        limit=500
                    ):  # Adjust limit as needed
                        database.insert_row(message)
                except discord.errors.Forbidden:
                    logging.warning(
                        "Don't have permissions to read %s in %s",
                        channel.name,
                        guild.name,
                    )

    logging.info("Checking DMs")
    # Fetch history from DM channels
    for dm_channel in client.private_channels:
        if isinstance(dm_channel, discord.DMChannel):
            try:
                async for message in dm_channel.history(
                    limit=500
                ):  # Adjust limit as needed
                    database.insert_row(message)
            except discord.errors.Forbidden:
                logging.warning(
                    "Don't have permissions to read DM with %s", dm_channel.recipient
                )


@client.event
async def on_message(msg: Message):
    if msg.author == client.user:
        return

    username = str(msg.author).split("#", maxsplit=1)[0]
    user_message = str(msg.content)
    channel = str(msg.channel)
    msg_time = str(msg.created_at)

    chat_message = f"username: {username} | channel: {channel} | timestamp: {msg_time} | message: {user_message}"

    logging.info("Received message: %s", chat_message)
    output = chat_llm_chain.predict(human_input=chat_message)

    await msg.channel.send(output)


client.run(os.getenv("DISCORD_TOKEN"))

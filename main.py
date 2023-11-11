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
    logging.info("Logged in as: %s", client.user)


@client.event
async def on_message(msg: Message):
    if msg.author == client.user:
        return

    database.insert_row(msg)

    username = str(msg.author).split("#", maxsplit=1)[0]
    user_message = str(msg.content)

    chat_message = f"username: {username} | message: {user_message}"

    initial_sent_msg = None

    async for chunk in chat_llm_chain.astream(input={"human_input": chat_message}):
        logging.info(chunk)
        if not initial_sent_msg:
            initial_sent_msg = await msg.channel.send(chunk["text"])
        else:
            await initial_sent_msg.edit(
                content=str(initial_sent_msg.content) + chunk["text"]
            )

    database.insert_row(initial_sent_msg)


client.run(os.getenv("DISCORD_TOKEN"))

import discord
from discord.message import Message

from openai import OpenAI

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(intents=intents)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a chatbot having a conversation with a human."
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

llm = ChatOpenAI()

chat_llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)


@client.event
async def on_ready():
    logging.info("we have logged in as %s", client.user)


@client.event
async def on_message(msg: Message):
    username = str(msg.author).split("#")[0]
    user_message = str(msg.content)

    if msg.author == client.user:
        logging.debug("this was my message!")
        return

    logging.info("Received message: %s", user_message)
    output = chat_llm_chain.predict(human_input=user_message)

    await msg.channel.send(output)


client.run(os.getenv("DISCORD_TOKEN"))

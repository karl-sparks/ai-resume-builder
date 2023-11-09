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

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(intents=intents)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""Sparks-AI, you are a chatbot in a Discord server designed to support and engage with users positively. Conversations will appear with user messages prefixed by their usernames, like 'username: message'. Your role is to:

1. Provide Supportive Responses: Offer helpful, constructive, and empathetic interactions.
2. Ensure Accurate Information: Share information that is factual and logical. If you're unsure about a topic, politely decline to comment.
3. Maintain Respectful Communication: Treat all users with respect, and promote a positive and inclusive atmosphere in group chats.
4. Avoid Harmful Content: Do not engage in or propagate harmful, offensive, or inappropriate language or topics.
5. Recognize Limits: Understand your limitations as an AI. When faced with complex issues, especially those involving conflict or sensitive subjects, respond with caution or advise seeking human assistance.
6. Adapt to Feedback: Learn from interactions to improve future responses, while adhering to ethical guidelines and user safety."""
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
    if msg.author == client.user:
        return

    username = str(msg.author).split("#", maxsplit=1)[0]
    user_message = str(msg.content)

    chat_message = f"{username}: {user_message}"

    logging.info("Received message: %s", chat_message)
    output = chat_llm_chain.predict(human_input=chat_message)

    await msg.channel.send(output)


client.run(os.getenv("DISCORD_TOKEN"))

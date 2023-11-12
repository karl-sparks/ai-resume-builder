import discord
from discord.message import Message

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, ChatMessage, AIMessage, HumanMessage
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

llm = ChatOpenAI(model="gpt-4-1106-preview", streaming=True)

chat_llm_chain = prompt | llm


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

    chat_hist = database.get_row_by_id(str(msg.author.id), "author_id")

    chat_hist_message = []

    for row in chat_hist:
        if row["author_id"] == "1171714115069284373":
            chat_hist_message.append(AIMessage(content=row["message_content"]))
        else:
            chat_hist_message.append(HumanMessage(content=row["message_content"]))

    logging.info("chat_hist: %s", chat_hist_message)
    initial_sent_msg = None

    message_to_send = ""

    async for chunk in chat_llm_chain.astream(
        input={"human_input": chat_message, "chat_history": chat_hist_message}
    ):
        chunk_text = chunk.content
        if not chunk_text:
            continue
        else:
            message_to_send += chunk_text

            in_code_block = message_to_send.count("```") == 1

            split_msg = message_to_send.rsplit("\n\n", 1)

            if len(split_msg) == 2 and not in_code_block:
                initial_sent_msg = await msg.channel.send(split_msg[0])
                message_to_send = split_msg[1]
                database.insert_row(initial_sent_msg)
            elif len(message_to_send) > 1500:
                initial_sent_msg = await msg.channel.send(message_to_send)
                message_to_send = ""
                database.insert_row(initial_sent_msg)

    if message_to_send:
        initial_sent_msg = await msg.channel.send(message_to_send)
        database.insert_row(initial_sent_msg)


client.run(os.getenv("DISCORD_TOKEN"))

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

logging = logging.getLogger()

llm = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_template(
    "You are a AI, you should be helpful {input_message}"
)

chain = prompt | llm

message = "How do I implement streaming from OpenAI using Langchain and discord.py?"

for chunk in chain.stream(input={"input_message": message}):
    logging.info(chunk)

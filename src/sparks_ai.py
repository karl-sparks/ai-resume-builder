from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from discord.message import Message

import src.config as CONFIG
from src.big_query import database
from src.mind import Mind

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_dict_to_msg_list(rows) -> list:
    chat_hist = []
    for row in rows:
        msg_content = row["author_name"] + ' said "' + row["message_content"] + '"'
        if row["author_id"] == "1171714115069284373":
            chat_hist.append(msg_content)
        else:
            chat_hist.append(msg_content)
    return chat_hist


class SparksAI:
    def __init__(self) -> None:
        logger.info("Init SparksAI()")

        self.mind = Mind(
            path_to_mind_files=CONFIG.MIND_FILE_PATH,
            path_to_starters=CONFIG.STARTER_FILE_PATH,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.mind.get_mind_file("core")),
                SystemMessagePromptTemplate.from_template("{user_mind}"),
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # Where the memory will be stored.
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # Where the human input will injected
            ]
        )

        llm = ChatOpenAI(model="gpt-4-1106-preview", streaming=True, verbose=True)

        self.message_llm = prompt | llm

    async def review_user(self, username: str):
        logger.info("Reviewing User Data")

        mind_file = self.mind.get_mind_file("core")
        user_file = self.mind.get_mind_file(username)
        all_msgs = convert_dict_to_msg_list(database.get_all_rows())

        prompt = PromptTemplate.from_template(
            """
        {mind_file}
        
        Below is all chat messages you have sent and recieved:
        
        {all_msgs}
        
        Review the above messages and write a detailed analysis of {username}. The analysis should include at least the following points but can include any additional information that is useful for future conversations:
        
        1. Main personality traits
        
        2. Likes and dislikes
        
        4. What are their main goals in life
        
        5. How do they want you to behave.
        
        6. List of confirmed data about {username}

        If you can not answer a section, add a placeholder stating more information is required.
        
        This is the previously geneterated analysis for reference:
        
        {user_file}
        """
        )

        llm = ChatOpenAI(model=CONFIG.GPT_MODEL)

        chain = prompt | llm

        analysis = await chain.ainvoke(
            {
                "mind_file": mind_file,
                "all_msgs": all_msgs,
                "username": username,
                "user_file": user_file,
            }
        )

        logger.info("Updating mind file")

        with open(
            CONFIG.MIND_FILE_PATH + "kaimsparks" + "-mind-file.md",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(analysis.content)

        logger.info("Finished review")

        return None

    async def handle_message(self, msg: Message) -> None:
        logger.info("Handling Msg")

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

        initial_sent_msg = None

        message_to_send = ""

        async for chunk in self.message_llm.astream(
            input={
                "human_input": chat_message,
                "chat_history": chat_hist_message,
                "user_mind": self.mind.get_mind_file(username),
            }
        ):
            chunk_text = chunk.content
            if not chunk_text:
                continue
            else:
                message_to_send += chunk_text

                if len(message_to_send) > 1500:
                    initial_sent_msg = await msg.channel.send(message_to_send)
                    message_to_send = ""
                    database.insert_row(initial_sent_msg)

        if message_to_send:
            initial_sent_msg = await msg.channel.send(message_to_send)
            database.insert_row(initial_sent_msg)

        await self.review_user(username=username)

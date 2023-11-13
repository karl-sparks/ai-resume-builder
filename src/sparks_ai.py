from langchain.schema import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from discord.message import Message
import os

import src.config as CONFIG
from src.big_query import database


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
        pass

    def load_core_mind_file(self) -> str:
        file_path = CONFIG.MIND_FILE_PATH + "\core-file.md"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                file_text = file.read()
        else:
            with open(
                CONFIG.MIND_FILE_PATH + "core-file-starter.md", "r", encoding="utf-8"
            ) as file:
                file_text = file.read()

        return file_text

    def self_reflect(self):
        mind_file = self.load_core_mind_file()
        all_msgs = convert_dict_to_msg_list(database.get_all_rows())

        prompt = PromptTemplate.from_template(
            """
                                              {mind_file}
                                              
                                              Below is all chat messages you have sent and recieved:
                                              
                                              {all_msgs}
                                              
                                              Review the above messages and write a detailed analysis of kaimsparks. The analysis should include at least the following points but can include any additional information that is useful for future conversations:
                                              
                                              1. Main personality traits
                                              
                                              2. Likes and dislikes
                                              
                                              4. What are their main goals in life
                                              
                                              5. How do they want you to behave.
                                              
                                              6. List of confirmed data about kaimsparks

                                              If you can not answer a section, add a placeholder stating more information is required.
                                              """
        )

        llm = ChatOpenAI(model="gpt-4-1106-preview")

        chain = prompt | llm

        analysis = chain.invoke({"mind_file": mind_file, "all_msgs": all_msgs})

        with open(
            CONFIG.MIND_FILE_PATH + "kaimsparks" + "-mind-file.md",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(analysis.content)

        return None

    def handle_message(self, msg: Message) -> None:
        msg = None

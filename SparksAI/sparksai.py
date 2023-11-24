import logging
from typing import AsyncIterator
from langchain.memory.chat_message_histories import FileChatMessageHistory
from SparksAI.swarm import Swarm
from SparksAI.memory import AIMemory

logger = logging.getLogger(__name__)


class SparksAI:
    def __init__(self) -> None:
        self.swarm = Swarm()
        self.memory = AIMemory()

    async def notice_message(self, username: str, msg: str) -> AsyncIterator:
        self.memory.get_convo_mem(username=username).add_user_message(msg)

        convo_memory = self.memory.get_convo_mem(username=username).messages
        logger.info("Getting message summary")
        message_summary = await self.swarm.get_archivist(username).ainvoke(
            {"input_message": msg, "memory": convo_memory}
        )

        logger.info("Getting Analyst Comments")
        analyst_review = await self.swarm.get_analyst_agent().ainvoke(
            {"content": f"Context: {message_summary}\n\nUser message: {msg}"}
        )

        inputs_dict = {
            "prior_messages": message_summary.content,
            "analyst_message": analyst_review["output"],
            "input_message": msg,
        }

        logger.info(inputs_dict)

        return self.swarm.get_conversation_agent(username).astream(input=inputs_dict)

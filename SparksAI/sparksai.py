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
        message_summary = await self.swarm.get_archivist(username).ainvoke(
            {"input_message": msg, "memory": convo_memory}
        )
        logger.info(message_summary)

        analyst_review = await self.swarm.get_analyst_agent().ainvoke(
            {"content": f"Context: {message_summary}\n\nUser message: {msg}"}
        )

        logger.info(analyst_review["output"])

        return self.swarm.get_conversation_agent(username).astream(
            {
                "prior_messages": message_summary,
                "analyst_message": analyst_review["output"],
                "input_message": msg,
            }
        )

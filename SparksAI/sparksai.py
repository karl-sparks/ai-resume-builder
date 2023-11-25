"""Contains the core code for running SparksAI"""
import logging
from typing import AsyncIterator

from langchain import agents
from langchain.agents import openai_assistant

from discord import Message, DMChannel

from SparksAI import config
from SparksAI import tools
from SparksAI.swarm import Swarm
from SparksAI.memory import AIMemory
from SparksAI.async_helpers import AreturnMessageIterator

logger = logging.getLogger(__name__)


class SparksAI:
    """Core SparksAI Class, handles noticing messages and generating replies"""

    def __init__(self):
        logging.info("Initialising SparksAI")
        self.swarm = Swarm()
        self.memory = AIMemory()
        self.thread_ids = {}
        agent = openai_assistant.OpenAIAssistantRunnable(
            assistant_id=config.TAV_DECIDER_ID, as_agent=True
        )

        self.decider = agents.AgentExecutor(
            agent=agent,
            tools=tools.SPARKS_AI_TOOLKIT,
            verbose=True,
        )

    async def notice_message(self, username: str, msg: str) -> AsyncIterator:
        self.memory.get_convo_mem(username=username).add_user_message(msg)

        input_msg = {"content": msg}

        if username in self.thread_ids:
            input_msg["thread_id"] = self.thread_ids[username]

        response = await self.decider.ainvoke(input_msg)

        logger.info(response)

        self.thread_ids[username] = response["thread_id"]

        return AreturnMessageIterator(response["output"], 20)

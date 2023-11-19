from typing import AsyncIterator
from SparksAI.swarm import Swarm


class SparksAI:
    def __init__(self) -> None:
        self.swarm = Swarm()

    def notice_message(self, username: str, msg: str) -> AsyncIterator:
        return self.swarm.get_conversation_agent(username).run(msg)

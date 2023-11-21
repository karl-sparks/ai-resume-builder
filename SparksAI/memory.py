from langchain.memory import FileChatMessageHistory


class AIMemory:
    def __init__(self) -> None:
        self.convo_mem = {}

    def get_convo_mem(self, username: str) -> FileChatMessageHistory:
        if username in self.convo_mem:
            return self.convo_mem[username]

        else:
            self.convo_mem[username] = FileChatMessageHistory(f"{username}_memory.txt")

            return self.convo_mem[username]

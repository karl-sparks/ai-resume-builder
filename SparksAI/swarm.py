from langchain.agents import AgentType, Tool, initialize_agent, AgentExecutor
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import FileChatMessageHistory
from langchain.prompts import MessagesPlaceholder
from langchain.utilities import SerpAPIWrapper

from SparksAI.config import MODEL_NAME


class Swarm:
    def __init__(self) -> None:
        self.conversation_swarm = {}
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            streaming=True,
            callbacks=[FinalStreamingStdOutCallbackHandler()],
        )

    def get_conversation_agent(self, username: str) -> AgentExecutor:
        if username in self.conversation_swarm:
            return self.conversation_swarm[username]

        else:
            self.init_conversation_agent(username)

            return self.conversation_swarm[username]

    def init_conversation_agent(self, username: str) -> None:
        if username in self.conversation_swarm:
            return None

        search = SerpAPIWrapper()
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful when you need to answer questions about current events. You should ask targeted questions.",
            ),
        ]

        convo_memory = ConversationBufferMemory(
            memory_key="memory",
            return_messages=True,
            chat_memory=FileChatMessageHistory(f"{username}_memory.txt"),
        )

        agent_kwargs = {
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")]
        }

        convo_agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.OPENAI_MULTI_FUNCTIONS,
            verbose=True,
            memory=convo_memory,
            agent_kwargs=agent_kwargs,
        )

        self.conversation_swarm[username] = convo_agent

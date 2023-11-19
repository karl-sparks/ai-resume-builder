from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from SparksAI.config import MIND_INIT, MODEL_NAME
from SparksAI.mind import Mind


class SparksAI:
    def __init__(self) -> None:
        self.mind = Mind(**MIND_INIT)

        self.llm = ChatOpenAI(model=MODEL_NAME)
        self.prompt = PromptTemplate.from_template("{prompt_str}")
        self.chain = self.prompt | self.llm

    def think(self) -> None:
        new_thought = self.chain.invoke({"prompt_str": self.mind}).content

        self.mind.add_thought(new_thought)

    def notice(self, msg: str) -> None:
        formated_thought = f'You thought "{msg}" at {datetime.now()}'

        self.mind._perception = self.mind._perception + "\n" + formated_thought

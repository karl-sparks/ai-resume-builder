import os
import datetime
import logging

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.utils import add_data_to_json


class SparksAI:
    def __init__(self) -> None:
        self.llm = None
        self.prompt_template = None
        self.llm_model = None
        self.context = None
        self.convo_history = None

    def generate_model(
        self,
        model_engine: str,
        prompt_template: str,
        context: str,
        convo_history: str,
    ) -> None:
        self.llm = ChatOpenAI(model=model_engine)
        self.prompt_template = PromptTemplate.from_template(prompt_template)
        self.llm_model = LLMChain(prompt=self.prompt_template, llm=self.llm)
        self.context = context
        self.convo_history = convo_history

    def ask_ai(self, question: str) -> str:
        """Main function."""

        logging.info("Asking Model...")

        input_data = {
            "context": self.context,
            "convo_history": self.convo_history,
            "question": question,
        }

        answer = self.llm_model.run(**input_data)

        answer_prompt = {
            f"RUN_{datetime.datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')}": {
                "model": self.llm_model.llm.model_name,
                "prompt": self.llm_model.prompt.template.format(**input_data),
                "answer": answer,
            }
        }

        add_data_to_json("answer_prompt.json", answer_prompt)

        logging.info("Returning answer")

        return answer

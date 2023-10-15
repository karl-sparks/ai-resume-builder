"""Main file for the bot."""
import datetime
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils import add_data_to_json

class AIBot:
    """Main class for the bot."""
    def __init__(self, model_name: str, template: PromptTemplate) -> None:
        self.llm = ChatOpenAI(model = model_name)
        self.prompt = template
        self.llm_model = self.generate_model()

    def generate_model(self) -> LLMChain:
        """Generate a model based on the template."""

        return LLMChain(prompt=self.prompt, llm=self.llm)

    def ask_ai(self, input_data: dict) -> str:
        """Main function."""

        print("Asking Model...")

        answer = self.llm_model.run(**input_data)

        answer_prompt = {
            f"RUN_{datetime.datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')}": {
                "model": self.llm_model.llm.model_name,
                "prompt": self.llm_model.prompt.template.format(**input_data),
                "answer": answer
            }
        }

        add_data_to_json('answer_prompt.json', answer_prompt)

        return answer

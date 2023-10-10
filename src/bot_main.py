"""Main file for the bot."""
import datetime
from utils import read_input, add_data_to_json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class AIBot:
    """Main class for the bot."""
    def __init__(self, model_name: str, template: str):
        self.llm = ChatOpenAI(model = model_name)
        self.prompt = PromptTemplate(template=template,
                                input_variables = ["context", "job_title",
                                                "company_name", "job_description"])
        self.llm_model = self.generate_model()

    def generate_model(self) -> LLMChain:
        """Generate a model based on the template."""

        return LLMChain(prompt=self.prompt, llm=self.llm)

    def ask_ai(self, question: str) -> str:
        """Main function."""
        input_template = read_input("input.json")

        print(input_template)
        input_data = {"question": question}

        print("Asking Model...")
        answer = self.llm_model.run(**input_data)

        answer_prompt = {
            f"RUN_{datetime.datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')}": {
                "model": llm_model.llm.model_name,
                "prompt": llm_model.prompt.template.format(**input_data),
                "answer": answer
            }
        }

        add_data_to_json('answer_prompt.json', answer_prompt)

        return answer

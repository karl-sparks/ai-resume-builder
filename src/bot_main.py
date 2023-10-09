"""Main file for the bot."""
import datetime
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def read_input() -> dict:
    """Read the input from the JSON file."""
    with open('input.json', encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data

def generate_model(model_name, template) -> LLMChain:
    """Generate a model based on the template."""
    llm = ChatOpenAI(model = model_name)

    prompt = PromptTemplate(template=template,
                            input_variables = ["context", "job_title",
                                               "company_name", "job_description"])

    return LLMChain(prompt=prompt, llm=llm)

def add_data_to_json(file_path, new_data) -> None:
    """Add new data to a JSON file."""
    # Step 1: Read existing JSON data from the file (if any)
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}  # If the file doesn't exist, start with an empty dictionary

    # Step 2: Modify the data structure (add new data)
    existing_data.update(new_data)

    # Step 3: Write the modified data back to the JSON file
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    print("Data added to JSON file.")

def ask_ai(model_name: str, question: str) -> str:
    """Main function."""
    input_template = read_input()

    input_data = {"question": question}

    llm_model = generate_model(model_name, input_template["template"])

    print("Asking Model...")
    answer = llm_model.run(**input_data)

    answer_prompt = {
        f"RUN_{datetime.datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')}": {
            "model": llm_model.llm.model_name,
            "prompt": llm_model.prompt.template.format(**input_data),
            "answer": answer
        }
    }

    add_data_to_json('answer_prompt.json', answer_prompt)

    return answer
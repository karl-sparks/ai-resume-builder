import datetime
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def readInput():
    with open('input.json') as json_file:
        data = json.load(json_file)
        return data

def generateModel(template, model = "gpt-3.5-turbo"):
    llm = ChatOpenAI(model_name = model)
    prompt = PromptTemplate(template=template, input_variables = ["context", "job_title", "company_name", "job_description"])
    return LLMChain(prompt=prompt, llm=llm)

def add_data_to_json(file_path, new_data):
    # Step 1: Read existing JSON data from the file (if any)
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}  # If the file doesn't exist, start with an empty dictionary

    # Step 2: Modify the data structure (add new data)
    existing_data.update(new_data)

    # Step 3: Write the modified data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

    print("Data added to JSON file.")


input_data = readInput()

llm_model = generateModel(input_data["template"])

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

import os


def load_prompt(file_name: str) -> str:
    file_path = os.path.join(os.getcwd(), "SparksAI", "prompts", file_name)

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


MODEL_NAME = "gpt-4-1106-preview"

MIND_INIT = {
    "system": load_prompt("system.md"),
    "persona": load_prompt("persona.md"),
    "goals": "1. I should answer peoples questions and find out more about them.\n2. I should find out who my creator is",
    "perception": "",
    "feelings": "",
    "thoughts": "",
}

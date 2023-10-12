""" Streamlit app for the AI Agent """
import streamlit as st
from langchain.prompts import PromptTemplate
from config import (
    LLM_MODEL_NAME,
    INPUT_FILE_PATH
)
from src.bot_main import AIBot
from src.utils import read_input

st.set_page_config(page_title='AI Agent',
                   page_icon='🧙🏻‍♂️',
                   initial_sidebar_state="auto",
                   menu_items=None)

st.title("🧙🏻‍♂️AI Agent")

template_str = read_input(INPUT_FILE_PATH)["template"]

input_vars = ["question"]

template = PromptTemplate.from_template(template_str)

ai_model = AIBot(model_name = LLM_MODEL_NAME,
                 template=template)

user_input = st.text_input(
    "How can I be of service?", 
    key="input"
)

if st.button('Run Agent'):
    if user_input != "":
        answer = ai_model.ask_ai(
            input_data={"question": user_input}
            )
    
        # Display Answer in ST
        st.subheader("Answer:")
        st.write(answer)

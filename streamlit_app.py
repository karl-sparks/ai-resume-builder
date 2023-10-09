""" Streamlit app for the AI Agent """
import os
import streamlit as st
from config import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_SIZE,
    BABY_AGI_MODEL_NAME
)
from src.bot_main import ask_ai

st.set_page_config(page_title='AI Agent', page_icon='🧙🏻‍♂️', initial_sidebar_state="auto", menu_items=None)
st.title("🧙🏻‍♂️AI Agent")

# if you just want to use the .env file, uncomment the following lines
# from decouple import config
# if config('OPENAI_API_KEY', default=None) is not None and config('SERPAPI_API_KEY', default=None) is not None:
#     os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
#     os.environ["SERPAPI_API_KEY"] = config('SERPAPI_API_KEY')

st.sidebar.title("Enter Your API Keys 🗝️")
open_api_key = st.sidebar.text_input(
    "Open API Key", 
    value=st.session_state.get('open_api_key', ''),
    help="Get your API key from https://openai.com/",
    type='password'
)

# os.environ["OPENAI_API_KEY"] = open_api_key

serp_api_key = st.sidebar.text_input(
    "Serp API Key", 
    value=st.session_state.get('serp_api_key', ''),
    help="Get your API key from https://serpapi.com/",
    type='password'
)

st.session_state['open_api_key'] = os.environ["OPENAI_API_KEY"]

with st.sidebar.expander('Advanced Settings ⚙️', expanded=False):
    st.subheader('Advanced Settings ⚙️')
    num_iterations = st.number_input(
        label='Max Iterations',
        value=5,
        min_value=2,
        max_value=20,
        step=1
    )
    baby_agi_model = st.text_input('OpenAI Baby AGI Model', BABY_AGI_MODEL_NAME, help='See model options here: https://platform.openai.com/docs/models/overview')


user_input = st.text_input(
    "How can I be of service?", 
    key="input"
)

if st.button('Run Agent'):
    if user_input != "":
        answer = ask_ai(
            model_name=baby_agi_model,
            question=user_input
        )
    
        # Display Answer in ST
        st.subheader("Answer:")
        st.write(answer)
import os
import streamlit as st
from constants import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_SIZE, 
    TODO_CHAIN_MODEL_NAME,
    BABY_AGI_MODEL_NAME
)
from src.agent import run_agent

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
os.environ["OPENAI_API_KEY"] = open_api_key
serp_api_key = st.sidebar.text_input(
    "Serp API Key", 
    value=st.session_state.get('serp_api_key', ''),
    help="Get your API key from https://serpapi.com/",
    type='password'
)
os.environ["SERPAPI_API_KEY"] = serp_api_key


st.session_state['open_api_key'] = open_api_key
st.session_state['serp_api_key'] = serp_api_key

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
    todo_chaining_model = st.text_input('OpenAI TODO Model', TODO_CHAIN_MODEL_NAME, help='See model options here: https://platform.openai.com/docs/models/overview')   
    embedding_model = st.text_input('OpenAI Embedding Model', EMBEDDING_MODEL_NAME, help='See model options here: https://platform.openai.com/docs/guides/embeddings/what-are-embeddings')
    # embedding_size = st.text_input('Embedding Model Size', EMBEDDING_SIZE, help='See model options here: https://platform.openai.com/docs/guides/embeddings/what-are-embeddings')


user_input = st.text_input(
    "How can I be of service?", 
    key="input"
)

if st.button('Run Agent'):
    if user_input != "" and (open_api_key == '' or serp_api_key == ''):
        st.error("Please enter your API keys in the sidebar")
    elif user_input != "":
        run_agent(
            user_input=user_input,
            num_iterations=num_iterations,
            baby_agi_model=baby_agi_model,
            todo_chaining_model=todo_chaining_model,
            embedding_model=embedding_model,
            # embedding_size=embedding_size
        )
    
        # Download the file using Streamlit's download_button() function
        st.download_button(
            label='Download Results',
            data=open('output.txt', 'rb').read(),
            file_name='output.txt',
            mime='text/plain'
        )
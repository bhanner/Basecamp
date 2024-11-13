import streamlit as st
import openai
import time

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.chains import load_chain
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from itinerary.ItineraryQA2 import ItineraryRecommendationList

# This appears to be missing itinerary.ItineraryQA2 as a module, so this won't run.

def set_session(key, value):
    st.session_state[key] = value

def get_session_value(key):
    if key in st.session_state:
        return st.session_state[key]
    else:
        return ""

def get_openai_key_if_needed():
    try:
        llm_provider = get_session_value("llm_provider")
        while llm_provider == "OpenAI" and "openai_key" not in st.session_state:
            st.error('Please add OpenAI Key in left panel and Press Enter')
            time.sleep(3)
    finally:
        return

def setApiKeySessionVar():
    set_session("openai_key", api_key_oi)

st.title("Simple Chat Bot")

sidebar_container = st.sidebar.container()

sidebar_container.write("# Welcome to LLM Generative AI Demos.")
sidebar_container.markdown(
    """
    # demos

    This is a set of examples created to explore
    - OpenAI API functionalities 
    - Langchain and OpenAI API Integration

""")

if llm_provider_oi := sidebar_container.selectbox(
    'Which LLM Provider?',
    ('OpenAI', 'Bedrock'), 
    index=0
    ):
    set_session("llm_provider", llm_provider_oi)

if (get_session_value("llm_provider")==""):
    set_session("llm_provider", "OpenAI")

if get_session_value("llm_provider") == "OpenAI":
    if api_key_oi := sidebar_container.text_input(label= "Open AI Key",
                                                value=get_session_value('openai_key'),
                                                max_chars=None,
                                                key=None,
                                                type="password",
                                                placeholder="Type Your Open AI API Key Here",
                                                disabled=False,
                                                on_change=setApiKeySessionVar,
                                                label_visibility="visible"):
        set_session("openai_key", api_key_oi)

    if llm_model_oi := sidebar_container.selectbox(
        'Which LLM Model?',
        ('gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4'), 
        index=0):
        set_session("llm_model", llm_model_oi)
else:
    if llm_model2_oi := sidebar_container.selectbox(
        'Which LLM Model?',
        ('amazon.titan-tg1-large', 'anthropic.claude-v1'), 
        index=0):
        set_session("llm_model", llm_model2_oi)

user_avatar = "images/user.jpeg"
slalom_avatar = "images/slalom.png"

avatars = {'user': user_avatar, 'assistant': slalom_avatar}

get_openai_key_if_needed()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

import urllib.parse

def get_itinerary_markdown(result): 
    result_md = f"""# Your Recommendations: 
{result.summary}"""

    for itinerary in result.itinerary_list:
        i = ITINERARIES[itinerary.itinerary_code]
        result_md += f"""
## {i["Title"]}

{i["Description"]}

[Click here for more information]({i["URL"]})

{i["URL"]}

![cruise image](http://www.ncl.com/{urllib.parse.quote(i['Hero Image'])})
"""


def get_assistant_response():
    full_response = ""
    content = [ m["content"] for m in st.session_state.messages][-1:][0]

    print(content)
    if get_session_value("llm_provider") == "OpenAI":
        model_name = get_session_value("llm_model")
        temperature = 0.5
        llm = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=get_session_value("openai_key"))
        recommender = ItineraryRecommendationList('/Users/matth/dev/genai/ncl/cruise_2/data/db', llm)
        result = recommender.get_itinerary_recommendations(content)
        response = get_itinerary_markdown(result)
    #else:
    #    model_name = get_session_value("llm_model")
    #    cruise_qa = CruiseEmbeddingQA("bedrock_db", False, CruiseEmbeddingQA.getBedrockLlm(model_name), CruiseEmbeddingQA.getBedrockEmbedding())
    #    response = cruise_qa.ask_a_question(content)

    return response

# Display chat messages from history on app rerun
messages = get_session_value("messages") or []
for message in messages:
    with st.chat_message(message["role"], avatar = avatars[message["role"]]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user", avatar = avatars['user']):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar = avatars["assistant"]):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = get_assistant_response()
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

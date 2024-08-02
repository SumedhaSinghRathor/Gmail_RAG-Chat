import os
import tempfile
import streamlit as st
from embedchain import App

#define the embedchain_bot function
def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"model": "gpt-4-turbo", "temperature": 0.5, "api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}}
        }
    )
    
#create Streamlit app
st.title("Chat with your GMail Inbox: ")
st.caption("This app allows you to chat with your Gmail inbox using OpenAPI")

#get the OpenAPI key from the user
openai_access_token = st.text_input("Enter your OpenAI API Key", type="password")

#set the Gmail filter statically
gmail_filer = "to: me label:inbox"

#add the gmail data to the knowledge base if the OpenAI API key is provided
if openai_access_token:
    #create a temporary directory to store the database
    db_path = tempfile.mkdtemp()
    #create an instance of EmbedChain App
    app = embedchain_bot(db_path, openai_access_token)
    app.add(gmail_filer, data_type="gmail")
    st.success("Added emails from Inbox to the knowledge base!")
    
prompt = st.text_input("Ask any question about your emails: ")

if prompt:
    answer = app.query(prompt)
    st.write(answer)
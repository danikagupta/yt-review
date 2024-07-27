import streamlit as st

def show_navigation():
    with st.container(border=True):
        col1,col2,col3,col4=st.columns(4)
        col1.page_link("streamlit_app.py", label="Home", icon="🏠")
        col2.page_link("pages/1_upload_videos.py", label="Upload URL", icon="1️⃣")
        col3.page_link("pages/2_transcribe_videos.py", label="Transcribe", icon="2️⃣")
        #col3.page_link("pages/chat_with_replicate.py", label="Chat Replicate")
        #col3.page_link("pages/chat_with_LMStudio.py", label="Chat LM Studio")
        #col4.page_link("pages/2_retreival_augmented_chat.py", label="RAG", icon="🌎")
        #cols=st.columns(len(navList)
        # col3.page_link("pages/1_chat_with_AI.py", label="Chat", icon="2️⃣", disabled=True)
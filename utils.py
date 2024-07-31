import streamlit as st
from datetime import datetime

from google.oauth2 import service_account
import json


def current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_google_cloud_credentials():
    # Get Google Cloud credentials from JSON file
    js1 = st.secrets["GOOGLE_KEY"]
    #print(" A-plus Google credentials JS: ", js1)
    credentials_dict=json.loads(js1)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)   
    st.session_state.credentials = credentials
    return credentials
    

def show_navigation():
    with st.container(border=True):
        col1,col2,col3,col4,col5=st.columns(5)
        col1.page_link("streamlit_app.py", label="Home", icon="🏠")
        col2.page_link("pages/1_upload_videos.py", label="Upload URL", icon="1️⃣")
        col2.page_link("pages/2_transcribe_videos.py", label="Transcribe", icon="2️⃣")
        col2.page_link("pages/3_qna.py", label="Q & A", icon="🌎")
        col3.page_link("pages/4_fix_data.py", label="Fix data")
        col4.page_link("pages/11_transcripts_with_answers.py", label="Transcript Q&A", icon="🌎")
        col5.page_link("pages/22_test_slack.py", label="Just testing")
        #col3.page_link("pages/chat_with_LMStudio.py", label="Chat LM Studio")
        #col4.page_link("pages/2_retreival_augmented_chat.py", label="RAG", icon="🌎")
        #cols=st.columns(len(navList)
        # col3.page_link("pages/1_chat_with_AI.py", label="Chat", icon="2️⃣", disabled=True)
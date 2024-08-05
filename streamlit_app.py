import streamlit as st
import os

#from utils import show_navigation
#show_navigation()

@st.dialog("Authentication")
def authenticate():
    st.title("Authentication Required")
    password = st.text_input("Enter the access key:", type="password")
    if password == st.secrets["ACCESS_KEY"]:
        st.session_state["authenticated"] = True
        #print(f"Query params: {st.query_params.to_dict()}")
        st.rerun()

        #st.rerun()
    elif password:
        st.error("Invalid secret key")

def main():
    os.environ["LANGCHAIN_TRACING_V2"]="true"
    os.environ["LANGCHAIN_API_KEY"]=st.secrets['LANGCHAIN_API_KEY']
    os.environ["LANGSMITH_API_KEY"]=st.secrets['LANGCHAIN_API_KEY']
    os.environ['LANGCHAIN_ENDPOINT']="https://api.smith.langchain.com"
    os.environ['LANGCHAIN_PROJECT']="yt-review"

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        authenticate()
    else:
        #st.title("Video Transcription and Q&A")

        user_pages=[
            st.Page("streamlit_app.py", title="Home", icon="🏠"),
            st.Page("ui/12_transcript_list.py", title="Transcript List", icon="1️⃣"),
            st.Page("ui/41_one_video_e2e.py", title="Process One Video", icon="2️⃣"),
            #st.Page("ui/14_transcript_yt_video.py", title="Transcript YT Video", icon="2️⃣"),
            #st.Page("ui/11_transcripts_with_answers.py", title="Transcript Q&A", icon="🌎"),
        ]

        admin_pages=[
            st.Page("ui/1_upload_videos.py", title="Upload URL", icon="1️⃣"),
            st.Page("ui/2_transcribe_videos.py", title="Transcribe", icon="2️⃣"),
            st.Page("ui/3_qna.py", title="Q & A", icon="🌎"),
        ]

        bulk_pages=[
            st.Page("ui/31_processing_stats.py", title="Processing stats", icon="1️⃣"),
            st.Page("ui/32_qna_low_score.py", title="Low score Q-&-A", icon="2️⃣"),
            st.Page("ui/4_fix_data.py", title="Fix data", icon="🌎"),
            st.Page("ui/22_test_slack.py", title="More testing", icon="🌎"),
        ]
        pages={
            "User": user_pages,
            "Admin": admin_pages,
            "Bulk": bulk_pages,
        }
        pg = st.navigation(pages)
        pg.run()
        #st.title("Video Transcription and Q&A")

if __name__ == "__main__":
    main()

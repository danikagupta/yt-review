import streamlit as st

#from utils import show_navigation
#show_navigation()

def authenticate():
    st.title("Authentication Required")
    password = st.text_input("Enter the access key:", type="password")
    if password == st.secrets["ACCESS_KEY"]:
        st.session_state["authenticated"] = True
        st.button("Continue")
        #st.rerun()
    elif password:
        st.error("Invalid secret key")

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        authenticate()
    else:
        #st.title("Video Transcription and Q&A")

        user_pages=[
            st.Page("streamlit_app.py", title="Home", icon="🏠"),
            st.Page("pages/12_transcript_list.py", title="Transcript List", icon="1️⃣"),
            st.Page("pages/14_transcript_yt_video.py", title="Transcript YT Video", icon="2️⃣"),
            st.Page("pages/11_transcripts_with_answers.py", title="Transcript Q&A", icon="🌎"),
        ]

        update_pages=[
            st.Page("pages/1_upload_videos.py", title="Upload URL", icon="1️⃣"),
            st.Page("pages/2_transcribe_videos.py", title="Transcribe", icon="2️⃣"),
            st.Page("pages/3_qna.py", title="Q & A", icon="🌎"),
        ]

        fix_pages=[
            st.Page("pages/4_fix_data.py", title="Fix data"),
            st.Page("pages/22_test_slack.py", title="Just testing"),
        ]
        pages={
            "User": user_pages,
            "Update": update_pages,
            "Fix": fix_pages,
        }
        pg = st.navigation(pages)
        pg.run()
        #st.title("Video Transcription and Q&A")

if __name__ == "__main__":
    main()

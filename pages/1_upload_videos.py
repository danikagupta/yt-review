import streamlit as st

from utils import show_navigation
show_navigation()


from generate_transcript import transcribe_session
from session_info import get_update_session_info

def upload_one_video():
    st.write("Upload Video URL (e.g. https://youtu.be/vgYi3Wr7v_g)")
    #yt_url = st.text_input("Youtube Video URL")
    #if yt_url is not None:
    if yt_url := st.text_input("Youtube Video URL"):
        st.write("Video upload start")
        info=get_update_session_info(yt_url)
        st.table(info)
    else:
        st.write("Upload a video file")

st.title("🎈 Youtube Review Page 2")
upload_one_video()

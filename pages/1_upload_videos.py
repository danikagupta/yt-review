import streamlit as st

from utils import show_navigation
show_navigation()


from generate_transcript import transcribe_session

def upload_one_video():
    st.write("Upload Video URL (e.g. https://youtu.be/vgYi3Wr7v_g)")
    #yt_url = st.text_input("Youtube Video URL")
    #if yt_url is not None:
    if yt_url := st.text_input("Youtube Video URL"):
        st.write("Video uploaded successfully")
        transcript=transcribe_session(yt_url,st.secrets['ASSEMBLYAI_API_KEY'])
        st.write(transcript)
    else:
        st.write("Upload a video file")

st.title("🎈 Youtube Review Page 2")
upload_one_video()

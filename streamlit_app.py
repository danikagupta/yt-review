import streamlit as st

from utils import show_navigation
show_navigation()

from generate_transcript import transcribe_session



st.title("🎈 Youtube Review")
aaa="""
tab1,tab2,tab3=st.tabs(["Upload Video","Review Video","See Analysis"])

def tab_upload_videos():
    st.write("Upload Video URL (e.g. https://youtu.be/vgYi3Wr7v_g)")
    #yt_url = st.text_input("Youtube Video URL")
    #if yt_url is not None:
    if yt_url := st.text_input("Youtube Video URL"):
        st.write("Video uploaded successfully")
        transcript=transcribe_session(yt_url,st.secrets['ASSEMBLYAI_API_KEY'])
        st.write(transcript)
    else:
        st.write("Upload a video file")

with tab1:
    tab_upload_videos()
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
"""

import streamlit as st
from generate_transcript import transcribe_session_core

from utils import show_navigation
show_navigation()

st.title("Transcribe videos")

def transcribe_one_video():
    st.markdown("# Transcribe Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    if yt_url := st.text_input(" "):
        st.write("Transcribing video - Not saving yet")
        trs=transcribe_session_core(yt_url,st.secrets['ASSEMBLY_API_KEY'])
        st.markdown(trs)




st.title("🎈 Youtube Review Page 2")
st.divider()
transcribe_one_video()
st.divider()
transcribe_video_list_file()
st.divider()
transcribe_video_list(st.secrets['SLACK_BOT_TOKEN'])
st.divider()
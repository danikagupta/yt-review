import streamlit as st

from utils import show_navigation
show_navigation()


from generate_transcript import transcribe_session
from session_info import get_update_session_info, extract_video_id

def upload_one_video():
    st.markdown("# Upload Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    if yt_url := st.text_input(" "):
        st.write("Video upload start")
        info=get_update_session_info(yt_url)
        st.table(info)

def upload_video_list_file():
    st.markdown("# Upload Video List File")
    if video_list_file := st.file_uploader("Upload Video List File", type=["csv"]):
        st.write("Video list file upload start")
        video_list=[]
        for line in video_list_file.getvalue().decode().split("\n"):
            yt_url=line.strip()
            if yt_url.lower().startswith("http"):
                st.write(f"Processing :{yt_url}:")
                info=get_update_session_info(yt_url)
                video_list.append(info)
        st.table(video_list)

st.title("🎈 Youtube Review Page 2")
st.divider()
upload_one_video()
st.divider()
upload_video_list_file()

import streamlit as st

from utils import show_navigation
show_navigation()

st.markdown("# Q & A")


def qna_one_video():
    st.markdown("# Q & A One Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    yt_url = st.text_input(" ")
    if st.button("Q & A one video"):
        st.write("Q & A video")
        st.markdown("Not yet implemented")
        #transcribe_one_video_with_firestore(yt_url

def qna_video_list_file():
    st.markdown("Upload a CSV file with a list of video URLs")
    st.markdown("# Q & A Video List File")
    video_list_file = st.file_uploader("Upload Video List File", type=["csv"])
    if st.button("Q & A from file"):
        st.markdown("Not yet implemented")

def qna_video_from_db():
    st.markdown("# Q & A Video from Firestore")
    videoCount = st.slider("Select number of videos", 1, 1000, value=5)
    if st.button("Q & A from DB"):
        st.markdown("Not yet implemented")



st.divider()
qna_one_video()
st.divider()
qna_video_list_file()
st.divider()
qna_video_from_db()
st.divider()
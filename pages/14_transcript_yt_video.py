import streamlit as st

from google_firestore import get_total_transcripts, get_transcripts, get_qna_by_transcript_id, get_transcripts_by_video_id, get_transcripts_by_youtube_url

from streamlit_app import authenticate

from math import ceil


st.sidebar.markdown("# Transcript by Youtube Video")

def main():
    yt_url = st.sidebar.text_input("Provide YouTube URL")
    if st.sidebar.button("Q & A by video"):
        transcripts=get_transcripts_by_youtube_url(yt_url)
        t=transcripts[0]
        st.markdown(f"Video {yt_url}")
        st.markdown(f"Title: {t['title']}")
        st.markdown(f"Timestamp: {t['timestamp']}")
        with st.sidebar.expander("Transcript Debug"):
            st.markdown(t)
        txt=t['transcript']
        with st.expander("Transcript"):
            st.markdown(txt)

        video_id=t['video_id']
        qna_set=get_qna_by_transcript_id(video_id)
        with st.sidebar.expander("Q & A debug"):
            st.write(qna_set)

        qna_display=[]
        for qna in qna_set:
            qna_display.append({'Question':qna['question'],'Answer':qna['answer']})
        st.dataframe(qna_display)
        with st.sidebar.expander("Q & A"):
            for qna in qna_set:
                st.markdown(f"Q: {qna['question']}")
                st.markdown(f"A: {qna['answer']}")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
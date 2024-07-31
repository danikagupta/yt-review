import streamlit as st
from google_firestore import get_qna_by_transcript_id, get_transcripts_by_youtube_url

def show_transcript_qa_one_yt_video(yt_url):
    transcripts=get_transcripts_by_youtube_url(yt_url)
    print(f"Transcripts: {transcripts} for URL :{yt_url}:")
    t=transcripts[0]
    #st.markdown(f"Video {yt_url}")
    #st.markdown(f"Title: {t['title']}")
    #st.markdown(f"Timestamp: {t['timestamp']}")
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
    
    with st.sidebar.expander("Q & A"):
        st.dataframe(qna_display)
    for qna in qna_set:
        st.markdown(f"\n\n### Q: {qna['question']}")
        st.markdown(f"A: {qna['answer']}")  
        if 'score' in qna:
            st.markdown(f"**Score: {qna['score']}**")


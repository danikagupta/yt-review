import streamlit as st
import pandas as pd

from google_firestore import get_all_qna, get_all_transcripts, get_all_videos 


from utils import show_navigation
show_navigation()

from streamlit_app import authenticate

st.markdown("# Processing stats")

def get_video_stats():
    videos=get_all_videos()
    #st.markdown(videos[:1])
    data={'status':[],'duration':[],'timestamp':[]}
    for v in videos:
        data['status'].append(v['data']['status'])
        data['duration'].append(v['data']['duration'])
        data['timestamp'].append(v['data']['timestamp'])
    df=pd.DataFrame(data)
    df2=df.groupby('status').agg(
        count=('status', 'size'),
        earliest_timestamp=('timestamp', 'min'),
        latest_timestamp=('timestamp', 'max'),
        avg_duration=('duration', 'mean'),
    ).reset_index()
    return df2

def get_transcript_stats():
    transcripts=get_all_transcripts()
    #st.markdown(transcripts[:1])
    # data={'status':[],'duration':[],'timestamp':[]}
    data={'status':[],'duration':[]}
    for t in transcripts:
        try:
            data['status'].append(t['data']['status'])
            data['duration'].append(t['data']['duration'])
            #data['timestamp'].append(['data']['timestamp'])
        except Exception as e:
            print(f"Error {e} with {t}")
    df=pd.DataFrame(data)
    df2=df.groupby('status').agg(
        count=('status', 'size'),
        #earliest_timestamp=('timestamp', 'min'),
        #
        #latest_timestamp=('timestamp', 'max'),
        avg_duration=('duration', 'mean'),
    ).reset_index()
    return df2

def get_qna_stats():
    qnas=get_all_qna()
    #st.markdown(videos[:5])
    data={'score':[],'duration':[],'timestamp':[]}
    for qna in qnas:
        score=0
        if 'score' in qna['data']:
            score=qna['data']['score']
        data['score'].append(score)
        data['duration'].append(qna['data']['duration'])
        data['timestamp'].append(qna['data']['timestamp'])
    df=pd.DataFrame(data)
    df2=df.groupby('score').agg(
        count=('score', 'size'),
        earliest_timestamp=('timestamp', 'min'),
        latest_timestamp=('timestamp', 'max'),
        avg_duration=('duration', 'mean'),
    ).reset_index()
    return df2


def main():
    st.button("Refresh")
    st.divider()
    st.markdown("# Videos")
    st.dataframe(get_video_stats())    
    st.divider()
    st.markdown("# Transcripts")
    st.dataframe(get_transcript_stats())    
    st.divider()
    st.markdown("# Q-n-A")
    st.dataframe(get_qna_stats())    
    st.divider()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
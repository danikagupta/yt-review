import streamlit as st

from google_firestore import get_total_transcripts, get_transcripts, get_qna_by_transcript_id, get_transcripts_by_video_id, get_transcripts_by_youtube_url

from streamlit_app import authenticate

from math import ceil


st.markdown("# Transcripts available")

def main():
    transcripts = get_transcripts(1,2000)
    show_list=[]
    for tr in transcripts:
        d=tr['data']
        status=d.get('status','')
        title=d.get('title','')
        timestamp=d.get('timestamp','')
        duration=d.get('duration','')
        youtube_url=d.get('youtube_url','')
        video_id=d.get('video_id','')
        show_list.append({'Title':title,'youtube_url':youtube_url,'timestamp':timestamp,'duration':duration })
        #st.write(f"Transcript: {tr['data']['title']}")
    st.dataframe(show_list)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
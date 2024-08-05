import streamlit as st
import pandas as pd

from google_firestore import get_qna_range
from google_firestore import update_transcript_status_working_on_qna, add_to_qna, update_transcript_status_qna_done, get_new_transcripts

from generate_transcript import transcribe_session_core
from generate_qna import qna_session_core

from session_info import get_update_session_info
from google_firestore import find_ytvideo_by_url, update_video_status_transcribing, add_transcript, update_video_status_transcribe_error, update_video_status_transcribed, get_new_videos

from utils import show_navigation
show_navigation()

from streamlit_app import authenticate

st.markdown("# Process one video end-to-end")

def qna_one_video_with_firestore(url):
    # 1. Mark the transcript in Firestore as "new" => "working_on_qna"
    # 2. Get the transcript
    # 3. Use LLM to get the Answers
    # 4. Store the answers in QnA table
    # 5. Mark the transcript in Firestore as "qna_done"
    st.markdown("QnA for one transcript with Firestore")
    transcript=update_transcript_status_working_on_qna(url,True)
    if transcript:
        #st.markdown(f"Transcript found {transcript} ")
        responses=qna_session_core(transcript.get('transcript'),st.secrets['OPENAI_API_KEY'])
        for resp in responses:
            with st.expander("Response"):
                st.sidebar.markdown(resp)
            add_to_qna(resp,transcript['id'],transcript['youtube_url'],transcript['title'],
                       transcript['duration'],transcript['timestamp'])
        update_transcript_status_qna_done(transcript['id'])
    else:
        st.markdown(f"Transcript not found for {url}")


def transcribe_one_video_with_firestore(url):
    # 1. Mark the video in Firestore as "new" => "transcribing"
    # 2. Transcribe the video
    # 3. Add a record in Firestore for transcribed video
    # 4. Mark the video in Firestore as "transcribed"
    #st.markdown("Transcribe one video with Firestore")
    vids=find_ytvideo_by_url(url)
    vid=vids[0]
    #st.markdown(vid)
    if vid['status']!='new':
        st.markdown(f"Video at {url} already marked as (being) transcribed. Status={vid}")
        return
    #st.markdown(f"Updating status for video at id {vid['id']} to 'transcribing'")
    update_video_status_transcribing(vid['id'])   
    #st.markdown(f"Updated status for video at id {vid['id']} to 'transcribing'") 
    vids=find_ytvideo_by_url(url)
    vid=vids[0]
    #st.markdown(vid) 
    msg=transcribe_session_core(url,st.secrets['ASSEMBLYAI_API_KEY'])
    addedTranscript = add_transcript(msg,vid['id'],url,vid['title'],vid['duration'],vid['timestamp'])
    if(addedTranscript):
        st.markdown("Transcription added to Firestore")
        update_video_status_transcribed(vid['id']) 
    else:
        st.markdown("Error adding transcription to Firestore")
        update_video_status_transcribe_error(vid['id'])
    return msg

def upload_one_video(openai_api_key):
    st.markdown("# Upload Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    yt_url = st.text_input(" ")
    if st.button("Upload One Video"):
        st.write("Starting Video information upload...")
        get_update_session_info(yt_url)
        st.write("Starting Video transcription...")
        transcript=transcribe_one_video_with_firestore(yt_url)
        st.write("Starting Q&A ...")
        qna_one_video_with_firestore(yt_url)
        st.write("Completed ...")

def main():
    upload_one_video(st.secrets['OPENAI_API_KEY']) 
    print(f"MAIN One Video e2e: Completed")


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 

import streamlit as st
from generate_transcript import transcribe_session_core

from google_firestore import find_ytvideo_by_url, update_video_status_transcribing, add_transcript, update_video_status_transcribe_error, update_video_status_transcribed, get_new_videos

from utils import show_navigation
show_navigation()

st.title("Transcribe videos")

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
    addedTranscript = add_transcript(msg,vid['id'],url,vid['title'],vid['duration'])
    if(addedTranscript):
        st.markdown("Transcription added to Firestore")
        update_video_status_transcribed(vid['id']) 
    else:
        st.markdown("Error adding transcription to Firestore")
        update_video_status_transcribe_error(vid['id'])


def transcribe_one_video():
    st.markdown("# Transcribe One Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    yt_url = st.text_input(" ")
    if st.button("Transcribe one video"):
        st.write("Transcribing video")
        transcribe_one_video_with_firestore(yt_url)
        #trs=transcribe_session_core(yt_url,st.secrets['ASSEMBLYAI_API_KEY'])
        #st.markdown(trs)

def transcribe_video_list_file():
    st.markdown("Upload a CSV file with a list of video URLs")
    st.markdown("# Transcribe Video List File")
    video_list_file = st.file_uploader("Upload Video List File", type=["csv"])
    if st.button("Transcribe from file"):
        st.markdown("Not yet implemented")


def transcribe_video_from_db():
    st.markdown("# Transcribe Video from Firestore")
    videoCount = st.slider("Select number of videos", 1, 1000, value=5)
    if st.button("Transcribe from DB"):
        videos=get_new_videos(videoCount)
        for video in videos:
            id=video['id']
            title=video['title']
            url=video['youtube_url']
            duration=video['duration']
            st.markdown(f"Transcribing video {title} at {url} with duration {duration}. Id={id}")
            transcribe_one_video_with_firestore(url)
        st.markdown("Transcription complete for {videoCount} videos")

st.divider()
transcribe_one_video()
st.divider()
transcribe_video_list_file()
st.divider()
transcribe_video_from_db()
st.divider()
import streamlit as st
from generate_qna import qna_session_core

from google_firestore import update_transcript_status_working_on_qna, add_to_qna, update_transcript_status_qna_done, get_new_transcripts


from utils import show_navigation
show_navigation()

from streamlit_app import authenticate

st.markdown("# Q & A")

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
        


def qna_one_video():
    st.markdown("# Q & A One Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    yt_url = st.text_input("   ")
    if st.button("Q & A one video"):
        st.write("Q & A video")
        qna_one_video_with_firestore(yt_url)
        #transcribe_one_video_with_firestore(yt_url

def qna_video_from_db():
    st.markdown("# Q & A Video from Firestore")
    transcriptCount = st.number_input("Select number of transcripts", value=5)
    if st.button("Q & A from DB"):
        transcripts=get_new_transcripts(transcriptCount)
        print(f"Q & A Video From DB: For count {transcriptCount}\n got {transcripts} transcripts")
        for iteration_id,transcript in enumerate(transcripts,start=1):
            id=transcript['id']
            title=transcript['title']
            url=transcript['youtube_url']
            duration=transcript['duration']
            #txt = transcript['transcript']
            st.markdown(f"Iteration {iteration_id}: Q&A transcript {title} at {url} with duration {duration}. Id={id}")
            qna_one_video_with_firestore(url)
        st.markdown(f"QnA complete for {transcriptCount} videos")


def main():
    st.divider()
    qna_one_video()
    st.divider()
    qna_video_from_db()
    st.divider()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
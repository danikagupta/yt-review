import streamlit as st

from google_firestore import get_total_transcripts, get_transcripts, get_qna_by_transcript_id, get_transcripts_by_video_id, get_transcripts_by_youtube_url


from utils import show_navigation
show_navigation()

from streamlit_app import authenticate

from math import ceil


st.markdown("# Transcripts with answers")

per_page = 100

total_transcripts = get_total_transcripts()
total_pages = ceil(total_transcripts / per_page)



def qna_by_video_url():
    st.markdown("# Q & A One Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    yt_url = st.text_input("Provide YouTube URL")
    if st.button("Q & A by video"):
        transcripts=get_transcripts_by_youtube_url(yt_url)
        t=transcripts[0]
        with st.expander("Transcript Debug"):
            st.markdown(t)
        txt=t['transcript']
        with st.expander("Transcript"):
            st.markdown(txt)

        video_id=t['video_id']
        qna_set=get_qna_by_transcript_id(video_id)
        with st.expander("Q & A debug"):
            st.write(qna_set)
        with st.expander("Q & A"):
            for qna in qna_set:
                st.markdown(f"Q: {qna['question']}")
                st.markdown(f"A: {qna['answer']}")


def qna_by_title():
    st.markdown("# Q & A by Title")
    title = st.text_input("Provide Video Title")
    if st.button("Q & A by Title"):
        st.write("Q & A by Title")
        st.write("TO DO")

def paged_list():
    page = st.number_input('Page', min_value=1, max_value=total_pages, value=1)
    transcripts = get_transcripts(page, per_page)
    print(f"Transcript 0: {transcripts[0]}")

    transcript_options = [f"{t['data'].get('title', 'No title')}_{t['data']['timestamp']} " for t in transcripts]
    selected_transcript = st.selectbox('Select a Transcript', transcript_options)
    print(f"Selected Transcript: {selected_transcript}")

    if selected_transcript:
        selected_index = transcript_options.index(selected_transcript)
        transcript_data = transcripts[selected_index]['data']
        st.subheader('Transcript Text')
        print(f"Transcript Data: {transcript_data}")
        st.text_area('', value=transcript_data.get('transcript', 'No text available'), height=200, disabled=True)

        qna_data = get_qna_by_transcript_id(transcripts[selected_index]['id'])
        print(f"QnA Data: {qna_data} for transcript {transcripts[selected_index]['id']}")

        if qna_data:
            st.subheader('Questions and Answers')
            for item in qna_data:
                with st.expander(f"Q: {item['question']}"):
                    st.write(f"A: {item['answer']}")
        else:
            st.info('No Q&A pairs available for this transcript.')

def main():
    st.divider()
    qna_by_video_url()
    st.divider()
    qna_by_title()
    st.divider()
    paged_list()
    st.divider()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
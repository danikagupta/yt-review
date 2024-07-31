import streamlit as st

from google_firestore import get_total_transcripts, get_transcripts, get_qna


from utils import show_navigation
show_navigation()

from streamlit_app import authenticate

from math import ceil


st.markdown("# Transcripts with answers")

per_page = 100

total_transcripts = get_total_transcripts()
total_pages = ceil(total_transcripts / per_page)




def main():
    st.divider()
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

        qna_data = get_qna(transcripts[selected_index]['id'])
        print(f"QnA Data: {qna_data} for transcript {transcripts[selected_index]['id']}")

        if qna_data:
            st.subheader('Questions and Answers')
            for item in qna_data:
                with st.expander(f"Q: {item['question']}"):
                    st.write(f"A: {item['answer']}")
        else:
            st.info('No Q&A pairs available for this transcript.')

    st.divider()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
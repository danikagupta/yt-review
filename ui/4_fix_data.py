import streamlit as st

from google_firestore import fix_transcripts_status_new, fix_transcripts_timestamp, force_transcripts_status_new


from utils import show_navigation
show_navigation()

from streamlit_app import authenticate

st.markdown("# Fix data")


def main():
    st.divider()
    if st.button("Fix transcript status New"):
        fix_transcripts_status_new()
    if st.button("Force transcript status New"):
        force_transcripts_status_new()
    if st.button("Fix transcript timestamp"):
        fix_transcripts_timestamp()
    st.divider()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
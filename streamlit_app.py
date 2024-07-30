import streamlit as st

from utils import show_navigation
show_navigation()

def authenticate():
    st.title("Authentication Required")
    password = st.text_input("Enter the access key:", type="password")
    if password == st.secrets["ACCESS_KEY"]:
        st.session_state["authenticated"] = True
        st.button("Continue")
        #st.rerun()
    elif password:
        st.error("Invalid secret key")


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        st.title("🎈 Youtube Review")
else:
        authenticate() 



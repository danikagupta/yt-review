import streamlit as st
import pandas as pd

from google_firestore import get_qna_range


from utils import show_navigation
show_navigation()

from streamlit_app import authenticate

st.markdown("# Low-scoring answers")

exclude_list=[
     "Were there any parts of the session where students seemed confused or needed further clarification? Were there any notable strengths or areas for improvement that could enhance future training sessions?",
     "Did the teacher assign any homework during the class? If so, what was it?"
]

def main():
    values = st.slider("Define low range", 0, 10, (1, 6))
    min_duration = st.number_input("Min duration in minutes", value=10)
    exclude_yn = st.checkbox("Exclude common low-scoring questions about homework assignment and students being confused", value=True)
    if st.button("Run analysis"):
        qnas=get_qna_range(values[0],values[1])
        dataset=[]
        for qna in qnas:
            qnad=qna['data']
            if exclude_yn and qnad['question'] in exclude_list:
                continue
            if qnad['duration']/60>=min_duration:
                dataset.append({'Title':qnad['title'],'Score':qnad['score'],'Minutes':round(qnad['duration']/60),
                                'Question':qnad['question'],'Answer':qnad['answer'],
                                'Timestamp':qnad['timestamp'],
                                'Youtube URL':qnad['youtube_url']})
        st.dataframe(dataset)    

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
        main()
else:
        authenticate() 
import streamlit as st
import json

from utils import show_navigation
show_navigation()


from generate_transcript import transcribe_session
from session_info import get_update_session_info, extract_video_id
from slack_integration import fetch_channels, fetch_messages, get_df_from_messages

def upload_one_video():
    st.markdown("# Upload Video URL\n Example: https://youtu.be/vgYi3Wr7v_g)")
    if yt_url := st.text_input(" "):
        st.write("Video upload start")
        info=get_update_session_info(yt_url)
        st.table(info)

def upload_video_list_file():
    st.markdown("# Upload Video List File")
    if video_list_file := st.file_uploader("Upload Video List File", type=["csv"]):
        st.write("Video list file upload start")
        video_list=[]
        for line in video_list_file.getvalue().decode().split("\n"):
            yt_url=line.strip()
            if yt_url.lower().startswith("http"):
                st.write(f"Processing :{yt_url}:")
                info=get_update_session_info(yt_url)
                if info:
                    video_list.append(info)
        st.table(video_list)

def upload_video_list_from_slack(slack_bot_token):
    st.markdown("# Upload Video List from Slack")
    days = st.slider("Select number of days", 1, 70, value=None)
    if st.button("Run"):
        channels = fetch_channels(slack_bot_token)
        channel_ids = {channel['name']: channel['id'] for channel in channels}
        channel_id = channel_ids['session-notifications']
        messages = fetch_messages(slack_bot_token, channel_id, days)

        print(f"upload_video_list_from_slack Messages: {messages}")
        with open('messages.txt', 'w') as file:
            json.dump(messages,file)
        df=get_df_from_messages(messages)
        st.markdown(f"### {len(df)} videos found")
        st.table(df)
        video_list=[]
        for i,row in df.iterrows():
            yt_url=row['YouTube URL']
            info=get_update_session_info(yt_url)
            if info:
                video_list.append(info)
        st.table(video_list)
        




st.title("🎈 Youtube Review Page 2")
st.divider()
upload_one_video()
st.divider()
upload_video_list_file()
st.divider()
upload_video_list_from_slack(st.secrets['SLACK_BOT_TOKEN'])
st.divider()

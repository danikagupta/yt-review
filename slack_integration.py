from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import pandas as pd
import json

def fetch_channels(slack_token):
    try:
        client = WebClient(token=slack_token)
        response = client.conversations_list()
        channels = response['channels']
        #st.write(f"Channels: {channels}")
        #print(f"Channels: {channels}")
        return channels
    except SlackApiError as e:
        st.error(f"Error fetching channels: {e.response['error']}")
        return []
    
def fetch_messages(slack_token, channel_id, days,pagesize=100):
    client = WebClient(token=slack_token)
    oldest=datetime.now().timestamp() - days*24*60*60
    latest=datetime.now().timestamp()
    all_messages = []
    cursor=None
    #st.write(f"FETCH MESSAGES: {channel_id}, {start_time.timestamp()}, {end_time.timestamp()}")
    try:
        while True:
            print(f"FETCH MESSAGES: {channel_id}, {oldest}, {latest}")
            if cursor:
                response = client.conversations_history(
                    channel=channel_id,
                    oldest=oldest,
                    latest=latest,
                    cursor=cursor,
                    limit=pagesize
                )
            else:
                response = client.conversations_history(
                    channel=channel_id,
                    oldest=oldest,
                    latest=latest,
                    limit=pagesize
                )
            all_messages.extend(response['messages'])
            cursor = response.get('response_metadata', {}).get('next_cursor')
            if not cursor:
                break
        return all_messages
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        return []
    
def get_df_from_messages(messages):
    # Extract relevant data
    data = []
    for message in messages:
        try:
            if message.get("subtype") == "bot_message":
                title = message["text"].replace("bot:", "")
                timestamp = datetime.fromtimestamp(float(message["ts"]))
                youtube_url = message["attachments"][0]["actions"][0]["url"]
                data.append({
                    "Title": title,
                    "Datetime": timestamp,
                    "YouTube URL": youtube_url
                })
        except Exception as e:
            print(f"Error in get_df_from_messages: {e} while processing message {message}")
    return pd.DataFrame(data)
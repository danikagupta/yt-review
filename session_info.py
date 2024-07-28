
import pandas as pd
import yt_dlp as youtube_dl
import time
from datetime import datetime, timezone

import os
import re

from google_firestore import find_ytvideo_by_url
from google_firestore import add_video_to_firestore

max_retries = 3
delay = 2


def get_ydl_opts_session():
    return {
        'skip_download': True,
        'no_warnings': True,
        'quiet': True,
}

def extract_video_id(url):
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_session_information(url):
    retries = 0
    while retries < max_retries:
        try:
            ydl_opts = get_ydl_opts_session()
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:  
                info = ydl.extract_info(url, download=False)
                #print(f"Getting session information {url} returns {info} ")
                filename = ydl.prepare_filename(info)
                
                return {
                    'url': url,
                    'filename': filename,
                    'title': info['title'],
                    'duration': info['duration'],
                    'upload_date': info.get('upload_date'),
                    'timestamp': datetime.fromtimestamp(info.get('timestamp')),
                    'id': extract_video_id(url),
                }
        except Exception as e:
            retries += 1
            print(
                f"An error occurred during downloading (Attempt {retries}/{max_retries}):",
                str(e),
            )
            if retries >= max_retries:
                raise e
            time.sleep(delay)

def get_update_session_info(url):
    try:
        info=get_session_information(url)
        print(f"GET-UPDATE-SESSION-INFO: Info: {info}")
        new_url=info.get('url')
        print(f"New URL: {new_url}")
        videos=find_ytvideo_by_url(new_url)
        print(f"Videos are: {videos}")
        if videos:
            print(f"Video found in Firestore {videos}")
        else:
            print("New video")
            add_video_to_firestore(info)
            
        return videos
    except Exception as e:
        print(f"Error in get_update_session_info: {e}")
        return None
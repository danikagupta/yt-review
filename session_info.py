from datetime import datetime
import pandas as pd
import yt_dlp as youtube_dl
import time

import os
import re

max_retries = 3
delay = 2

class MyLogger(object):
    def __init__(self, external_logger=lambda x: None):
        self.external_logger = external_logger

    def debug(self, msg):
        print("[debug]: ", msg)
        self.external_logger(msg)

    def warning(self, msg):
        print("[warning]: ", msg)

    def error(self, msg):
        print("[error]: ", msg)


def my_hook(d):
    print("hook", d["status"])
    if d["status"] == "finished":
        print("Done downloading, now converting ...")



def current_time():
    return datetime.now().strftime("%H:%M:%S")

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
                print("Getting session information ", url)
                info = ydl.extract_info(url, download=False)
                print(f"Download YouTube Filesize: {filesize}")
                filename = ydl.prepare_filename(info)
                return {
                    'filename': filename,
                    'title': info['title'],
                    'duration': info['duration'],
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
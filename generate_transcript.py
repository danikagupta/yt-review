import assemblyai as aai
from datetime import datetime
import pandas as pd
import yt_dlp as youtube_dl
import time

import os
import re

import urllib.parse

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

def get_ydl_opts(external_logger=lambda x: None):
    return {
    "format": "bestaudio/best",
    "verbose": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
                "preferredquality": "192",  # set the preferred bitrate to 192kbps
            }
        ],
        "logger": MyLogger(external_logger),
    "outtmpl": "./downloads/audio/%(title)s.%(ext)s",  # Set the output filename directly
    "progress_hooks": [my_hook],
}

def extract_video_id(url):
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def download_video_audio(url, external_logger=lambda x: None):
    retries = 0
    while retries < max_retries:
        try:
            ydl_opts = get_ydl_opts(external_logger)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Going to download ", url)
                info = ydl.extract_info(url, download=False)
                filesize = info.get("filesize", 0)
                print(f"Download YouTube Filesize: {filesize}")
                filename = ydl.prepare_filename(info)
                res = ydl.download([url])
                print("youtube-dl result :", res)
                mp3_filename = os.path.splitext(filename)[0] + '.mp3'
                print('mp3 file name - ', mp3_filename)
                return {
                    'filename': mp3_filename,
                    'title': info['title'],
                    'duration': info['duration'],
                    'filesize': filesize,
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

#def transcribe_yt_assembly2(url,assembly_api_key):
#    aai.settings.api_key = assembly_api_key
#    #config = aai.TranscriptionConfig(speaker_labels=True)
#    config = aai.TranscriptionConfig()
#    transcript = aai.Transcriber().transcribe(url, config)
#    return transcript

def transcribe_yt_assembly3(url,assembly_api_key):
    print(f"TRANSCRIBE-YT-ASSEMBLY3: Downloading audio from {url} with key {assembly_api_key}")
    aai.settings.api_key = assembly_api_key
    config = aai.TranscriptionConfig(speaker_labels=True)
    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        for format in info["formats"][::-1]:
            if format["resolution"] == "audio only" and format["ext"] == "m4a":
                url = format["url"]
                break
        print(f"TRANSCRIBE-YT-ASSEMBLY3: Downloading audio from {url}")
        transcript = aai.Transcriber().transcribe(url, config)
        return transcript
    
def get_video_id(url):
    # Parse the URL to get the query parameters
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    # Extract the 'id' parameter
    video_id = query_params.get('id', [None])[0]
    if video_id:
        return video_id
    video_id = query_params.get('v', [None])[0]
    return video_id
    
def transcribe_yt_assembly_local(url,assembly_api_key):
    print(f"TRANSCRIBE-YT-ASSEMBLY-LOCAL: Downloading audio from {url} with key {assembly_api_key}")

    ydl_opts = {
        'format': 'm4a/bestaudio/best',  # The best audio version in m4a format
        'outtmpl': './downloads/audio/%(id)s.%(ext)s',  # The output name should be the id followed by the extension
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([url])
        print(f"Error Code: {error_code}")

    print("TRANSCRIBE-YT-ASSEMBLY-LOCAL: Finished downloading audio")

    aai.settings.api_key = assembly_api_key
    config = aai.TranscriptionConfig(speaker_labels=True)
    filename=f"./downloads/audio/{get_video_id(url)}.m4a"
    print(f"TRANSCRIBE-YT-ASSEMBLY-LOCAL: Generating transcript for {filename}")
    transcript = aai.Transcriber().transcribe(filename, config)
    print(f"TRANSCRIBE-YT-ASSEMBLY-LOCAL: Obtained transcript from {url}")
    return transcript


def transcribe_session_core(youtube_link,assembly_api_key):
    transcript = transcribe_yt_assembly_local(youtube_link,assembly_api_key)
    if transcript.status == aai.TranscriptStatus.error:
        return f"Error transcribing audio: {transcript.error}"
    
    msg=""
    try:
        for utterance in transcript.utterances:
            try:
                duration=(utterance.end-utterance.start)/1000
                msg=msg+f"{utterance.start//1000} - {duration} : Speaker {utterance.speaker}: {utterance.text}\n"
            except Exception as e:
                print(f"Error processing utterance: {e}")
                msg=msg+f"Error processing utterance: {e}\n"
    except Exception as e:
        print(f"Error processing transcript: {e}")
        msg=msg+f"Error processing transcript: {e}"

    return msg
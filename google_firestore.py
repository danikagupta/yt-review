from google.cloud import firestore
from google.oauth2 import service_account
import json
import hashlib

from utils import get_google_cloud_credentials
   

def find_zoom_session(session_id):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    doc_ref = db.collection(u'videos').document(session_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
    
def update_video_status_transcribing(id):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    doc_ref = db.collection(u'videos').document(id)
    doc_ref.set({
            u'status' : 'transcribing',
            u'dateUpdated' : firestore.SERVER_TIMESTAMP},
            merge=True)

def update_video_status_transcribe_error(id):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    doc_ref = db.collection(u'videos').document(id)
    doc_ref.set({
            u'status' : 'transcribe_error',
            u'dateUpdated' : firestore.SERVER_TIMESTAMP},
            merge=True)
    
def update_video_status_transcribed(id):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    doc_ref = db.collection(u'videos').document(id)
    doc_ref.set({
            u'status' : 'transcribed',
            u'dateUpdated' : firestore.SERVER_TIMESTAMP},
            merge=True)

# update_video_status_transcribing, add_transcript, update_video_status_transcribe_error, update_video_status_transcribed
   
def find_ytvideo_by_url(yt_url):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    collection_ref = db.collection(u'videos')
    query=collection_ref.where('youtube_url', '==', yt_url)
    docs=query.stream()

    # Collect document IDs that match the query
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return results

def add_video_to_firestore(info):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    title=info.get('title')
    duration=info.get('duration')
    youtube_url=info.get('url')
    timestamp=info.get('timestamp')
    hash_id = hashlib.md5(f"{title}-{duration}-{youtube_url}".encode()).hexdigest()
    doc_ref = db.collection(u'videos').document(hash_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Session {hash_id} already exists")
        return
    else:
        print(f"Adding session: {hash_id}")
        doc_ref.set({
            u'title': title,
            u'duration': duration,
            u'youtube_url': youtube_url,
            u'status' : 'new',
            u'timestamp': timestamp,
            u'dateAdded' : firestore.SERVER_TIMESTAMP,
            u'dateUpdated' : firestore.SERVER_TIMESTAMP
        })
        print(f"Session {hash_id} added")
        return

def add_transcript(transcript,video_id,url,title, duration,timestamp):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    doc_ref = db.collection(u'transcripts').document(video_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Transcript for video {video_id} already exists")
        return False
    else:
        print(f"Adding transcript for video: {video_id}")
        doc_ref.set({
            u'transcript': transcript,
            u'video_id': video_id,
            u'youtube_url': url,
            u'title': title,
            u'duration': duration,
            u'timestamp': timestamp,
            u'status' : 'new',
            u'dateAdded' : firestore.SERVER_TIMESTAMP,
            u'dateUpdated' : firestore.SERVER_TIMESTAMP
        })
        print(f"Transcript for video {video_id} added")
        return True

def get_new_videos(count=5):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    collection_ref = db.collection(u'videos')
    query = collection_ref.where('status', '==', 'new').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(count)
    docs = query.stream()
    
    # Collect document IDs that match the query
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return results   


def get_new_transcripts(count=5):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    collection_ref = db.collection(u'transcripts')
    query = collection_ref.where('status', '==', 'new').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(count)
    docs = query.stream()
    
    # Collect document IDs that match the query
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return results 

def update_transcript_status_working_on_qna(url,force=False):
    print("Invoked update_transcript_status_working_on_qna")
    db = firestore.Client(credentials=get_google_cloud_credentials())
    collection_ref = db.collection(u'transcripts')
    query=collection_ref.where('youtube_url', '==', url).order_by('dateAdded', direction=firestore.Query.ASCENDING).limit(1)
    docs = query.stream()
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    print(f"Found {len(results)} transcripts for {url}")
    #print(f"Results: {results}")
    if(len(results)==0):
        print(f"No transcript found for {url}")
        return None
    result=results[0] # Only use first result if there are multiple matches
    if 'status' not in result:
        result['status']='new'
    if result['status']!='new' and not force:
        print(f"Transcript {result['id']} already marked as {result['status']} for {url}. Skipping")
        return None
    doc_ref = db.collection(u'transcripts').document(result['id'])
    doc_ref.set({
        u'status' : 'working_on_qna',
        u'dateUpdated' : firestore.SERVER_TIMESTAMP},
        merge=True)
    return result



def add_to_qna(resp,transcript_id,youtube_url,title,duration,timestamp):
    print(f"Called QnA with parameters:\n {resp}\n Type: {type(resp)}, {transcript_id}, {youtube_url}, {title}, {duration}, {timestamp}")
    db = firestore.Client(credentials=get_google_cloud_credentials())
    question=resp.question
    answer=resp.answer
    hash_id = hashlib.md5(f"{title}-{transcript_id}-{question}-{timestamp}".encode()).hexdigest()
    doc_ref = db.collection(u'qna').document(hash_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Q&A for question {question} already exists for transcript {transcript_id}. Overwriting")
        doc_ref.set({
            u'question': question,
            u'answer': answer,
            u'transcript_id': transcript_id,
            u'youtube_url': youtube_url,
            u'title': title,
            u'duration': duration,
            u'timestamp': timestamp,
            u'dateAdded' : firestore.SERVER_TIMESTAMP,
            u'dateUpdated' : firestore.SERVER_TIMESTAMP
        })
        print(f"Transcript for video {youtube_url} added")
        return False
    else:
        print(f"Adding Q & A for video: {transcript_id}")
        doc_ref.set({
            u'question': question,
            u'answer': answer,
            u'transcript_id': transcript_id,
            u'youtube_url': youtube_url,
            u'title': title,
            u'duration': duration,
            u'timestamp': timestamp,
            u'dateAdded' : firestore.SERVER_TIMESTAMP,
            u'dateUpdated' : firestore.SERVER_TIMESTAMP
        })
        print(f"Transcript for video {youtube_url} added")
        return True

def update_transcript_status_qna_done(transcript_id):
    print("Invoked update_transcript_status_qna_done")
    db = firestore.Client(credentials=get_google_cloud_credentials())
    doc_ref = db.collection(u'transcripts').document(transcript_id)
    doc_ref.set({
            u'status' : 'qna_done',
            u'dateUpdated' : firestore.SERVER_TIMESTAMP},
            merge=True)

#
# Fix
#
def fix_transcripts_status_new():
    print("Invoked fix_transcripts_status_new")
    db = firestore.Client(credentials=get_google_cloud_credentials())
    collection_ref = db.collection(u'transcripts')
    docs=collection_ref.stream()
    for doc in docs:
        data=doc.to_dict()
        if 'status' not in data:
            print(f"Updating transcript {doc.id} to 'new'")
            doc_ref = db.collection(u'transcripts').document(doc.id)
            doc_ref.set({
                u'status' : 'new',
                u'dateUpdated' : firestore.SERVER_TIMESTAMP},
                merge=True)
    print("Finished fix_transcripts_status_new")    

def fix_transcripts_timestamp():  
    print("Invoked fix_transcripts_timestamps")
    db = firestore.Client(credentials=get_google_cloud_credentials())
    collection_ref = db.collection(u'transcripts')
    docs=collection_ref.stream()
    for doc in docs:
        data=doc.to_dict()
        if 'timestamp' not in data: 
            records=find_ytvideo_by_url(data['youtube_url'])
            print(f"Fix transcript {doc.id} records {records}")
            timestamp=records[0]['timestamp']
            doc_ref = db.collection(u'transcripts').document(doc.id)
            doc_ref.set({
                u'timestamp' : timestamp,
                u'dateUpdated' : firestore.SERVER_TIMESTAMP},
                merge=True) 

#
# Display
#

def get_transcripts(page, per_page):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    transcripts = db.collection('transcripts').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(per_page).offset((page - 1) * per_page).stream()
    return [{'id': doc.id, 'data': doc.to_dict()} for doc in transcripts]

def get_total_transcripts():
    db = firestore.Client(credentials=get_google_cloud_credentials())
    return db.collection('transcripts').count().get()[0][0].value

def get_qna(transcript_id):
    db = firestore.Client(credentials=get_google_cloud_credentials())
    qna = db.collection('qna').where('transcriptId', '==', transcript_id).stream()
    return [doc.to_dict() for doc in qna]
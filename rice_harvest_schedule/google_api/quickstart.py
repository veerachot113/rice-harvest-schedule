import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'google_api/credentials.json'
TOKEN_FILE = 'google_api/token.pickle'

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_event(summary, description, start_time, end_time):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Bangkok',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Bangkok',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event


import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'google_api/credentials.json'
TOKEN_FILE = 'google_api/token.pickle'

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_event(summary, description, start_time, end_time, attendees):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Bangkok',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Bangkok',
        },
        'attendees': [{'email': attendee} for attendee in attendees],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 5},  # แจ้งเตือนทางอีเมล 30 นาทีก่อนเริ่มงาน
                {'method': 'popup', 'minutes': 5},  # แจ้งเตือนแบบป๊อปอัพ 10 นาทีก่อนเริ่มงาน
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event

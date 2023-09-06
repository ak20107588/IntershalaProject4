# calendar_api.py
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from pprint import pprint
from datetime import datetime,timedelta,time




SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_calendar_service():
    creds = None
    # token_file = 'path/to/your/token.json' 

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json",SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credential.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(summary, AppointDate,AppointStart, AppointEnd):
    service = get_google_calendar_service()

    # Define event details
    event = {
        'summary': summary,
        'start': {
            'dateTime': AppointStart,
            'timeZone': 'India/Kolkata',  # e.g., 'America/New_York'
        },
        'date': {
            'dateTime': AppointDate,
            'timeZone': 'Your_Time_Zone',
        },
        'end': {
            'dateTime': AppointEnd,
            'timeZone': 'Your_Time_Zone',
        },
        # 'firstname':{
        #     'drfirstname':FirstName,
            
        # }

    }

    # Create the event
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event['id']

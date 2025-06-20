import datetime
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None

    # Use token if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid token, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(summary, start_time, end_time, attendee_email=None):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    if attendee_email:
        event['attendees'] = [{'email': attendee_email}]
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def find_free_slots(duration_minutes=60, max_results=10):
    service = get_calendar_service()

    # Define time range: now to next 7 days
    now = datetime.datetime.utcnow()
    end = now + datetime.timedelta(days=7)

    busy_slots = []
    calendars = service.calendarList().list().execute()
    primary_calendar = calendars['items'][0]['id']

    events = service.events().list(
        calendarId=primary_calendar,
        timeMin=now.isoformat() + 'Z',
        timeMax=end.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    for event in events.get('items', []):
        start = event['start'].get('dateTime')
        end_ = event['end'].get('dateTime')
        if start and end_:
            busy_slots.append((datetime.datetime.fromisoformat(start), datetime.datetime.fromisoformat(end_)))

    # Generate available slots
    free_slots = []
    current = now.replace(minute=0, second=0, microsecond=0)

    while current < end:
        slot_end = current + datetime.timedelta(minutes=duration_minutes)
        overlap = any(bs[0] < slot_end and bs[1] > current for bs in busy_slots)

        if not overlap and current.hour >= 9 and current.hour <= 18:
            free_slots.append((current, slot_end))
            if len(free_slots) >= max_results:
                break

        current += datetime.timedelta(minutes=30)

    return free_slots

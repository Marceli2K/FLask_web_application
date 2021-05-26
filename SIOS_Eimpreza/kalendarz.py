import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import pytz
import datetime


# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

SCOPES = ['https://www.googleapis.com/auth/calendar']


def kalendarz(event):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    start = event.event_starttime.strftime("%Y-%m-%dT%H:%M:00+01:00")
    end = event.event_endtime.strftime("%Y-%m-%dT%H:%M:00+01:00")

    event = {
      'summary': event.event_name,
      'location': '',
      'description': event.event_desc,
      'start': {
        'dateTime': start,
        'timeZone': 'Europe/Warsaw',
      },
      'end': {
        'dateTime': end,
        'timeZone': 'Europe/Warsaw',
      },
     
      
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s')

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

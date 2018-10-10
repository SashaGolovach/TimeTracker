from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.events'


def update(started, ended, name):
    store = file.Storage('token.json')
    creds = store.get()
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    event = {
        'summary': name,
        'start': {
            'dateTime': started,
            'timeZone': 'Europe/Kiev',
        },
        'end': {
            'dateTime': ended,
            'timeZone': 'Europe/Kiev',
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()

from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.events'


def main():
    store = file.Storage('token.json')
    creds = store.get()
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    event = {
        'summary': 'Google I/O 2015',
        'start': {
            'dateTime': '2018-10-07T14:00:00+03:00',
            'timeZone': 'Europe/Kiev',
        },
        'end': {
            'dateTime': '2018-10-07T18:00:00+03:00',
            'timeZone': 'Europe/Kiev',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
    }
    event = service.events().insert(calendarId='primary', body=event).execute()


if __name__ == '__main__':
    main()

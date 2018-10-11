from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.client import flow_from_clientsecrets


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.events'


def get_link():
    flow = flow_from_clientsecrets(
        'credentials.json', scope=SCOPES, redirect_uri='http://localhost')
    return flow.step1_get_authorize_url()


def save_creds(code, id):
    flow = flow_from_clientsecrets(
        'credentials.json', scope=SCOPES, redirect_uri='http://localhost')
    credentials = flow.step2_exchange(code)
    storage = file.Storage('tokens/{0}.json'.format(str(id)))
    storage.put(credentials)


def update(started, ended, name, id):
    store = file.Storage('tokens/{0}.json'.format(str(id)))
    creds = store.get()
    if not creds or creds.invalid:
        flow = flow_from_clientsecrets(
            'credentials.json', scope=SCOPES, redirect_uri='http://localhost')
        auth_uri = flow.step1_get_authorize_url()
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
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

from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


store = file.Storage('token1.json')
flow = flow_from_clientsecrets('credentials.json',
                               scope='https://www.googleapis.com/auth/calendar',
                               redirect_uri='http://178.159.226.158/')
creds = tools.run_flow(flow, store)

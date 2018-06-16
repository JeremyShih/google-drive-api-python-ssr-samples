"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""

from __future__ import print_function
from apiclient.discovery import build
import httplib2
from httplib2 import Http, socks
from oauth2client import file, client, tools

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('credentials.json')
creds = store.get()
p = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_SOCKS5, proxy_host="127.0.0.1", proxy_port=1086)
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, http = Http(proxy_info = p))
service = build('drive', 'v3', http=creds.authorize(Http(proxy_info = p)))

# Call the Drive v3 API
results = service.files().list(
    pageSize=20, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))


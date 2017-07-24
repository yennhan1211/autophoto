import httplib2
import os
import threading
import Queue
import time

import logging

from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Img upload'

class Upload(threading.Thread):
    """docstring for Upload"""
    def __init__(self, name, uplQueue, smsQueue):
        super(Upload, self).__init__()
        self.name = name
        self.mQueue = uplQueue
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
                filePath = self.mQueue.get(True, 0.05)
                logging.info('Uploading file at: ' + filePath)
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Upload, self).join(timeout)

    def doUpload(self):
        logging.info('Upload file ')

    def doResume(self):
        logging.info('Resume upload file ')



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.getcwd()
    credential_path = os.path.join(home_dir,
                                   'credential.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags.noauth_local_webserver = True
        credentials = tools.run_flow(flow, store, flags)
        logging.info('Storing credentials to ' + credential_path)
    return credentials

def insert_file(service, title, description, parent_id, mime_type, filename):
    """Insert new file.

    Args:
        service: Drive API service instance.
        title: Title of the file to insert, including the extension.
        description: Description of the file to insert.
        parent_id: Parent folder's ID.
        mime_type: MIME type of the file to insert.
        filename: Filename of the file to insert.
      Returns:
        Inserted file metadata if successful, None otherwise.
    """
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
      'title': title,
      'description': description,
      'mimeType': mime_type
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        file = service.files().insert(
            body=body,
            media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        # print 'File ID: %s' % file['id']

        return file
    except errors.HttpError as error:
        logging.info ('An error occurred: %s' % error)
        return None

if __name__ == '__main__':
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    insert_file(service, 'anh1.jpg', 'mota1', None, 'image/jpeg', '/home/pi/20170723-033423.jpg')
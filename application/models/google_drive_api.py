from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from io import BytesIO
from io import StringIO
import pandas as pd
import re
import io
from googleapiclient.http import MediaIoBaseDownload
import requests
from tqdm import tqdm
import os.path
from googleapiclient.http import MediaFileUpload
import gspread
from df2gspread import df2gspread as d2g

from oauth2client.service_account import ServiceAccountCredentials
try:
    FILE_DIR = os.path.abspath(os.path.dirname(__file__))
except:
    FILE_DIR = os.path.join(os.getcwd(),'application','models')


# HAVE TO SHARE WORKSHEET WITH THIS
'portfolio@total-furnace-239118.iam.gserviceaccount.com'


class DriveAPI:

    def __init__(self):
        self.service = self.get_gdrive_service()
        self.gc = gspread.service_account(filename=os.path.join(FILE_DIR,'service_account.json'))
        self.main(100)

    def get_gdrive_service(self):
        # If modifying these scopes, delete the file token.pickle.
        # SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']

        creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(FILE_DIR,'token.pickle')):
            with open(os.path.join(FILE_DIR,'token.pickle'), 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(FILE_DIR,'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(FILE_DIR,'token.pickle'), 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)

    def main(self, file_num = 50):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 5 files the user has access to.
        """
        service = self.get_gdrive_service()
        # Call the Drive v3 API
        results = service.files().list(pageSize=file_num, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
        # get the results
        items = results.get('files', [])
        self.items = items
        # list all 20 files & folders
        self.list_files(items)
        self.files_df = pd.DataFrame(items)

    def list_files(self, items):
        """given items returned by Google Drive API, prints them in a tabular way"""
        if not items:
            # empty drive
            print('No files found.')
        else:
            rows = []
            for item in items:
                # get the File ID
                id = item["id"]
                # get the name of file
                name = item["name"]
                try:
                    # parent directory ID
                    parents = item["parents"]
                except:
                    # has no parrents
                    parents = "N/A"
                try:
                    # get the size in nice bytes format (KB, MB, etc.)
                    size = get_size_format(int(item["size"]))
                except:
                    # not a file, may be a folder
                    size = "N/A"
                # get the Google Drive type of file
                mime_type = item["mimeType"]
                # get last modified date time
                modified_time = item["modifiedTime"]
                # append everything to the list
                rows.append((id, name, parents, size, mime_type, modified_time))
            print("Files:")
            # convert to a human readable table
            table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
            # print the table
            print(table)


    def get_size_format(self, b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"


    def search(self, service, query):
        # search for the file
        result = []
        page_token = None
        while True:
            response = service.files().list(q=query,
                                            spaces="drive",
                                            fields="nextPageToken, files(id, name, mimeType)",
                                            pageToken=page_token).execute()
            # iterate over filtered files
            for file in response.get("files", []):
                result.append((file["id"], file["name"], file["mimeType"]))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                # no more files
                break
        return result
    

    def download(self, filename):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/drive.file'
                ]
        service = self.get_gdrive_service()
        # the name of the file you want to download from Google Drive 
        # search for the file by name
        search_result = self.search(service, query=f"name='{filename}'")
        # get the GDrive ID of the file
        file_id = search_result[0][0]
        # make it shareable
        service.permissions().create(body={"role": "reader", "type": "anyone"}, fileId=file_id).execute()
        # download file
        return self.download_file_from_google_drive(file_id, filename)


    def download_file_from_google_drive(self, id, destination):
        def stream_data(chunk):
            try:
                s=str(chunk,'utf-8')
            except:
                s=str(chunk,'latin-1')

            data = StringIO(s)        
            chunk_df=pd.read_csv(data, engine='python', error_bad_lines=False, encoding='utf-8')

            return chunk_df

        def get_confirm_token(response):
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    return value
            return None

        def save_response_content(response, destination):
            CHUNK_SIZE = 32768
            # get the file size from Content-length response header
            file_size = int(response.headers.get("Content-Length", 0))
            # extract Content disposition from response headers
            content_disposition = response.headers.get("content-disposition")
            # parse filename
            filename = re.findall("filename=\"(.+)\"", content_disposition)[0]
            print("[+] File size:", file_size)
            print("[+] File name:", filename)
            progress = tqdm(response.iter_content(CHUNK_SIZE), f"Downloading {filename}", total=file_size, unit="Byte", unit_scale=True, unit_divisor=1024)

            temp_df = pd.DataFrame()
            chunk = None
            for chunk in progress:
                if chunk: # filter out keep-alive new chunks
                    chunk_df = stream_data(chunk)
                    temp_df = pd.concat([chunk_df, temp_df])
                    # update the progress bar
                    progress.update(len(chunk))
            progress.close()

            return temp_df

        # base URL for download
        URL = "https://docs.google.com/uc?export=download"
        # init a HTTP session
        session = requests.Session()
        # make a request
        response = session.get(URL, params = {'id': id}, stream=True)

        print("[+] Downloading", response.url)
        token = get_confirm_token(response)
        # get confirmation token
        if token:
            params = {'id': id, 'confirm':token}
            response = session.get(URL, params=params, stream=True)

        # download to disk
        return save_response_content(response, destination)


    def upload_files(self, folder_name, file_name):
        """
        Creates a folder and upload a file to it
        """
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                'https://www.googleapis.com/auth/drive.file']

        # authenticate account
        service = self.get_gdrive_service()
        self.service = service
        # folder details we want to make
        folder_metadata = {
            "name": folder_name,
            "mimeType": 'application/vnd.google-apps.folder'
        }
        # create the folder
        file = service.files().create(body=folder_metadata, fields="id").execute()

        
        # get the folder id
        folder_id = file.get("id")
        print("Folder ID:", folder_id)
        # upload a file text file
        # first, define file metadata, such as the name and the parent folder ID
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        # upload
        media = MediaFileUpload(file_name, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File created, id:", file.get("id"))

    ##################################
    # Section 2: gspread integration
    ##################################

    def get_sheet_id_by_name(self, sheet_name):
        files_df = self.files_df
        return files_df[files_df.name == sheet_name]['id'].iloc[0]

    def upload_df_to_sheets(self, df, sheet_id, tab):
        gc = gspread.service_account(filename=os.path.join(FILE_DIR,'service_account.json'))
        sh = gc.open_by_key(sheet_id)
        
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(FILE_DIR,'service_account.json'), scope)
        d2g.upload(df, sheet_id, tab, credentials=credentials, row_names=False)

    def download_sheets_to_df_by_name(self, sheet_name):
        '''
        only first sheet
        '''
        gc = gspread.service_account(filename=os.path.join(FILE_DIR,'service_account.json'))
        wks = gc.open(sheet_name).sheet1

        data = wks.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        return df

    def download_sheets_to_df_by_id(self, sheet_id, tab='Sheet1'):
        '''
        only first sheet
        '''
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.get_worksheet(0)
        worksheet = sh.worksheet(tab)
        
        return pd.DataFrame(worksheet.get_all_records())




# # sheet_id = '1fUa9GB3WzUjsAUi-y1V2ao98bx9YnoSn46X5F4oX6R8'
# gdrive = DriveAPI()
# sheet_id = gdrive.get_sheet_id_by_name('SunriseEventsCategories')
# df = gdrive.download_sheets_to_df_by_id(sheet_id,'SunriseEvents')

# gdrive.upload_df_to_sheets(df, sheet_id, 'test')



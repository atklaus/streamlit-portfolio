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
import csv
import io
import requests
import re
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

CREDS_PATH = FILE_DIR

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets']

# HAVE TO SHARE WORKSHEET WITH THIS
'portfolio@total-furnace-239118.iam.gserviceaccount.com'

class GoogleAPI:

    def __init__(self):
        self.get_creds()
        self.gc = gspread.service_account(filename=os.path.join(FILE_DIR,'service_account.json'))

    def get_creds(self):

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(CREDS_PATH,'token.pickle')):
            with open(os.path.join(CREDS_PATH,'token.pickle'), 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(CREDS_PATH,'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(CREDS_PATH,'token.pickle'), 'wb') as token:
                pickle.dump(creds, token)

        self.creds = creds
        self.token = token

    def upload_df_to_sheets(self, df, sheet_name, tab):
        sheet_id = self.search_get_file_id(sheet_name)

        gc = gspread.service_account(filename=os.path.join(CREDS_PATH,'service_account.json'))
        sh = gc.open_by_key(sheet_id)
        
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(CREDS_PATH,'service_account.json'), scope)
        d2g.upload(df, sheet_id, tab, credentials=credentials, row_names=False)

    def download_sheets_to_df(self, sheet_name, tab='Sheet1'):
        '''
        '''
        # sheet_id = self.get_sheet_id_by_name(sheet_name)
        sheet_id = self.search_get_file_id(sheet_name)

        gc = gspread.service_account(filename=os.path.join(CREDS_PATH,'service_account.json'))
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.get_worksheet(0)
        worksheet = sh.worksheet(tab)
        
        return pd.DataFrame(worksheet.get_all_records())

    def create_move_sheet(self):
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        body = {}
        results = sheet.create(body=body).execute()

        # Move the created Spreadsheet to the specific folder.
        drive = build('drive', 'v3', credentials=creds)
        folderId = '1MGICjFhGL7fQwbzBP7CR_ll3YGdPzs3o'
        res = drive.files().update(fileId=results['spreadsheetId'], addParents=folderId, removeParents='root').execute()
        res['id']
        print(res)

    def get_spreadsheet_id(self, spreadsheet_name):
        drive = build('drive', 'v3', credentials=self.creds)
        results = []
        page_token = None

        while True:
            try:
                param = {'q': 'mimeType="application/vnd.google-apps.spreadsheet"'}

                if page_token:
                    param['pageToken'] = page_token

                files = drive.files().list(**param).execute()
                results.extend(files.get('files'))

                # Google Drive API shows our files in multiple pages when the number of files exceed 100
                page_token = files.get('nextPageToken')

                if not page_token:
                    break

            except:
                break

        spreadsheet_id = [result.get('id') for result in results if result.get('name') == spreadsheet_name][0]

        return spreadsheet_id

    def sheet_to_df(self, sheet_name, tab):

        service = build('sheets', 'v4', credentials=self.creds)
        sheet = service.spreadsheets()
        spreadsheet_id = self.get_spreadsheet_id(sheet_name)
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=tab).execute()
        values = result.get('values', [])

        if not values:
            pass
        else:
            rows = sheet.values().get(spreadsheetId=spreadsheet_id,range=tab).execute()
            data = rows.get('values')

        df = pd.DataFrame(data, columns=data[0])
        df = df.drop(0)
        df.reset_index(inplace=True)
        return df

    def open_sheet(self, sheet_name, tab):
        doc = self.gc.open(sheet_name)
        sheet_obj = doc.worksheet(tab)
        self.sheet_obj = sheet_obj
    
    def get_cell_value(self, row, column):
        return self.sheet_obj.cell(row, column).value

    def update_cell_value(self, row, column, value):
        self.sheet_obj.update_cell(row, column, value)

    def insert_row(self, row_values_list, row_index):
        self.sheet_obj.insert_row(row_values_list, row_index)



gdrive = GoogleAPI()
# spreadsheet_id = gdrive.get_spreadsheet_id("IPEDS Data")
df = gdrive.sheet_to_df("IPEDS Data", "IPEDS Data")
df['PDI_Tier'] = df['PDI_Tier'].replace('',None)
df['Apps_Tot_FT'] = df['Apps_Tot_FT'].replace('',None)
df['Adm_Tot_FT'] = df['Adm_Tot_FT'].replace('',None)

df['PDI_Tier']= df['PDI_Tier'].astype(float)
df['Apps_Tot_FT']= df['Apps_Tot_FT'].astype(float)
df['Adm_Tot_FT']= df['Adm_Tot_FT'].astype(float)


# https://stackoverflow.com/questions/66767685/how-to-get-only-filtered-rows-from-google-sheets-to-python-script-using-google-a

# spreadsheet_id = "###" # Please set the Spreadsheet ID.
# sheet_id = "0"  # Please set the sheet name.

# url = 'https://docs.google.com/spreadsheets/d/' + spreadsheet_id + '/gviz/tq?tqx=out:csv&gid=' + str(sheet_id)
# res = requests.get(url, headers={'Authorization': 'Bearer ' + creds.token})
# ar = [row for row in csv.reader(io.StringIO(res.text), delimiter=',')]
# # ar.pop(0) # When you want to remove the header row, you can also use this.
# pd.DataFrame(ar)

# print(ar)

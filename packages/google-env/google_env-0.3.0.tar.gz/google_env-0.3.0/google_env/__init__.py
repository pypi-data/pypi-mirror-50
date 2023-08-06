# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function
import os.path
from os.path import expanduser
import pickle
import re
import shutil
import sys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '17fcDBp5tez9JFtRwucDW5-wq3jgmzq8s-oWcnUljyR0'
SAMPLE_RANGE_NAME = 'Sheet1!A1:B1000'

def write_env_file(values):
    if not os.path.exists(".env"):
        raise ("Missing .env file")

    print("Rewriting .env")
    with open(".env__rewrite", "w") as target:
        with open(".env", "r") as f:
            line = f.readline()
            while line:
                if re.match(r'^# GOOGLE_ENV:.*', line):
                    target.write(line)
                    target.write("\n".join(["{}={}".format(r[0], r[1]) for r in values]))
                    target.write("\n")
                    line = f.readline()
                    while line and not re.match(r'^# END_GOOGLE_ENV.*', line):
                        line = f.readline()
                    if line:
                        target.write(line)
                    else:
                        target.write("# END_GOOGLE_ENV")
                else:
                    target.write(line)
                line = f.readline()

    # Now swap files
    shutil.move(".env__rewrite", ".env")


def get_sheet_id():
    with open(".env") as f:
        line = f.readline()
        while line:
            m = re.match(r'^# GOOGLE_ENV:.*spreadsheets/d/([^/]+)', line)
            if m:
                sheet_id = m.group(1).strip()
                name = "Sheet1"
                m = re.match(r'(.*)!([\w]+)', sheet_id)
                if m:
                    sheet_id = m.group(1)
                    name = m.group(2)

                return sheet_id, name
            line = f.readline()

    raise Exception("Could not find speadsheet link in .env file")

def read_sheet(sheet_id, sheet_range):
    print("Pulling values from sheet: ", sheet_id, sheet_range)

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_file = os.path.join(expanduser("~"), ".googlenv_token")

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_file = 'google_env_creds.json'
            if not os.path.exists(creds_file):
                creds_file = os.path.join(expanduser("~"), creds_file)
            if not os.path.exists(creds_file):
                raise Exception("Can't find {}".format(creds_file))

            flow = InstalledAppFlow.from_client_secrets_file(
                creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    values = result.get('values', [])
    for row in values:
        yield row

def rewrite_env_file():
    if len(sys.argv) > 1 and 'help' in sys.argv[1]:
        print("Injects Google sheets values into .env file in the current directory")
        print("See: https://github.com/incountry/google_env")
    else:
        sheet_id, sheet_name = get_sheet_id()
        sheet_range = sheet_name + '!A1:B1000'

        write_env_file(read_sheet(sheet_id, sheet_range))



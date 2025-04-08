import logging
import string
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



class GoogleSheetConnection:
    def __init__(self, certs:dict):

        self.credentials_dict = certs
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self._connect()
    
    def _create(self,spreadsheet:gspread.spreadsheet.Spreadsheet, worksheet_name)->gspread.worksheet.Worksheet:
        return self._validate(spreadsheet.add_worksheet(title=worksheet_name,rows=2,cols=6))
    
    def _connect(self):
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(self.credentials_dict, self.scope)
        self.client = gspread.authorize(self.creds)
        return self.client

    def _validate(self,worksheet:gspread.worksheet.Worksheet)->gspread.worksheet.Worksheet:
        REQUIRED_COLUMNS = ["Id", "Name", "Count", "Median", "Average", "Min", "Max", "Open", "Close", "Changed"]
        existing_headers = worksheet.row_values(1)

        if not existing_headers or existing_headers[:len(REQUIRED_COLUMNS)] != REQUIRED_COLUMNS:
            worksheet.insert_row(REQUIRED_COLUMNS, index=1)
            logging.info("Worksheet headers validated and updated.")

        return worksheet
    
    def _open_spread(self,spreadsheet:str,worksheet:str="")->gspread.worksheet.Worksheet:
        if worksheet == "":
            return self._validate(self.client.open(spreadsheet).get_worksheet(0))
        else:
            try:
                return self._validate(self.client.open(spreadsheet).worksheet(worksheet))
            except gspread.exceptions.WorksheetNotFound as e:
                spread = self.client.open(spreadsheet)
                logging.warning(f"Worksheet {worksheet} not found. Creating new.")
                worksheet_obj = self._validate(self._create(spreadsheet=spread,worksheet_name=worksheet))
                return worksheet_obj

    def open(self,spreadsheet:str,worksheet:str=""):
        sheet = self._open_spread(spreadsheet,worksheet)
        return sheet.get_all_records()
    
    def update(self,spreadsheet:str,dataframe:pd.DataFrame,worksheet:str=""):
        columns = ["Id", "Name", "Count", "Median", "Average", "Min", "Max", "Open", "Close", "Changed"]
        last_column = get_column_letter(len(columns))
        sheet = self._open_spread(spreadsheet,worksheet)
        data = sheet.get_all_records()
        sheet_df = pd.DataFrame(data)
        if sheet_df.empty:
            sheet.append_rows(dataframe.values.tolist())
            logging.info("Appended all data (Sheet was empty).")
            return
        print(dataframe)
        sheet_df["Id"] = sheet_df["Id"].astype(str)
        dataframe["Id"] = dataframe['Id'].astype(str)

        updates = []
        new_rows = []

        for _, row in dataframe.iterrows():
            row_id = row["Id"]
            
            if row_id in sheet_df["Id"].values:
                row_idx = sheet_df.index[sheet_df["Id"] == row_id][0] + 2
                update_range = f'A{row_idx}:{last_column}{row_idx}' 
                updates.append((update_range, [row.values.tolist()]))
            else: new_rows.append(row.values.tolist())

        if updates:
            sheet.batch_update([{"range": r, "values": v} for r, v in updates])
            logging.info(f"Updated {len(updates)} rows.")

        if new_rows:
            sheet.append_rows(new_rows)
            logging.info(f"Appended {len(new_rows)} new rows.")

def get_column_letter(index: int) -> str:
    """Convert column index (1-based) to Excel-style letter (A, B, C, ..., Z, AA, AB, ...)."""
    result = ""
    while index > 0:
        index -= 1
        result = string.ascii_uppercase[index % 26] + result
        index //= 26
    return result

def get_instance():
    certs = {
            "type": os.environ['G_API_TYPE'],
            "project_id": os.environ['G_API_PROJECT_ID'],
            "private_key_id": os.environ['G_API_PRIVATE_KEY_ID'],
            "private_key": os.environ['G_API_PRIVATE_KEY'],
            "client_email": os.environ['G_API_CLIENT_EMAIL'],
            "client_id": os.environ['G_API_CLIENT_ID'],
            "auth_uri": os.environ['G_API_AUTH_URI'],
            "token_uri": os.environ['G_API_TOKEN_URI'],
            "auth_provider_x509_cert_url": os.environ['G_API_AUTH_PROVIDER_X509_CERT_URL'],
            "client_x509_cert_url": os.environ['G_API_CLIENT_X509_CERT_URL']
        }
    return GoogleSheetConnection(certs)

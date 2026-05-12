import os
import pickle
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1GvMIxMctcnJ1iAyRWqwEkjv_8F8pI-NdVRFLbdrf2C4'

class GoogleSheetsReader:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        # 优先使用Streamlit Secrets（云端部署）
        try:
            import streamlit as st
            if 'gcp_service_account' in st.secrets:
                self.creds = service_account.Credentials.from_service_account_info(
                    st.secrets['gcp_service_account'],
                    scopes=SCOPES
                )
                self.service = build('sheets', 'v4', credentials=self.creds)
                return
        except:
            pass

        # 方式2：使用本地Service Account JSON文件
        if os.path.exists('service_account.json'):
            self.creds = service_account.Credentials.from_service_account_file(
                'service_account.json',
                scopes=SCOPES
            )
            self.service = build('sheets', 'v4', credentials=self.creds)
            return

        # 方式3：使用OAuth（本地开发）
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError(
                        "请先创建 credentials.json 或 service_account.json 文件。\n"
                        "步骤：\n"
                        "1. 访问 https://console.cloud.google.com/\n"
                        "2. 创建项目 -> 启用 Google Sheets API\n"
                        "3. 创建 OAuth 2.0 凭据 -> 下载为 credentials.json\n"
                        "   或创建 Service Account -> 下载为 service_account.json\n"
                        "4. 将文件放到当前目录"
                    )
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)

    def read_sheet(self, sheet_name, range_notation='A:Z'):
        range_name = f'{sheet_name}!{range_notation}'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        values = result.get('values', [])
        if not values:
            return pd.DataFrame()

        df = pd.DataFrame(values[1:], columns=values[0])
        return df

    def get_fb_data(self, market):
        sheet_name = f'FB广告-{market}'
        df = self.read_sheet(sheet_name)
        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            numeric_cols = ['spend', 'impressions', 'clicks', 'purchase_count',
                          'purchase_value', 'add_to_cart_count', 'add_to_cart_value']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def get_sp_data(self, market):
        sheet_name = f'SP广告-{market}'
        df = self.read_sheet(sheet_name, 'A:AI')
        if not df.empty and 'run_date' in df.columns:
            df['run_date'] = pd.to_datetime(df['run_date'], errors='coerce')
            numeric_cols = ['expense', 'ROAS', 'Direct ROAS', 'ACOS', 'Direct ACOS',
                          'Product Impressions', 'Product Clicks', 'Product CTR']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.replace('-', ''), errors='coerce')
        return df

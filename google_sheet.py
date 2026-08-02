import gspread
from datetime import datetime
import os
import json
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=SCOPES
)
client = gspread.authorize(creds)

# Replace with your Google Sheet name
sheet = client.open_by_key("1XkNMCyPqOIYsmHlvlm7EPmEcyoRruUTydnQxb32V5eY").sheet1


def save_participant(username, department):
    sheet.append_row([
        username,
        department,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])
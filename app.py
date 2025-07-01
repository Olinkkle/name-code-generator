import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# Setup Google Sheets connection
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Client Codes").sheet1  # Change if using a different sheet name
    return sheet

# Generate a new unique code
def generate_unique_code(existing_codes, prefix):
    while True:
        code = f"{prefix}-{random.randint(0, 999):03}"
        if code not in existing_codes:
            return code

# Main Streamlit app
st.title("🎫 Name Code Generator (Google Sheets)")

name = st.text_input("Enter your name:")
prefix = st.selectbox("Choose a prefix:", ["C", "P"])

if st.button("Generate Code"):
    if not name.strip():
        st.error("Name cannot be empty.")
    else:
        try:
            sheet = connect_to_sheet()
            records = sheet.get_all_records()
            existing_codes = {row['Code'] for row in records}
            code = generate_unique_code(existing_codes, prefix)
            sheet.append_row([code, name.strip()])
            st.success(f"✅ Code generated: `{code}` and saved to Google Sheets")
        except Exception as e:
            st.error(f"🚨 Error: {e}")

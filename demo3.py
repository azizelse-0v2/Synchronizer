import os
import datetime
import re
import time
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from google.oauth2 import service_account
from googleapiclient.discovery import build

api_id = '25504149'
api_hash = '5cdd1680c1a4f7f49da84b7f6eed0ebb'
phone_number = '+998909044143'
channel_username = 'Nocommenttesting'

SERVICE_ACCOUNT_FILE = 'review-automation007-148b61262097.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

client = TelegramClient('session_name', api_id, api_hash)

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)
docs_service = build('docs', 'v1', credentials=credentials)

async def get_published_days():
    published_days = set()
    async for message in client.iter_messages(channel_username):
        if message.message:
            match = re.search(r"#Day(\d+)", message.message)
            if match:
                published_days.add(int(match.group(1)))
    return published_days

async def publish_document(content, day, link):
    try:
        first_line, rest_of_content = content.split('\n', 1)
        message = f"[{first_line}]({link})\n{rest_of_content}"
        await client.send_message(channel_username, message, link_preview=False)
        print(f"Published: Day {day}")
    except FloodWaitError as e:
        print(f"Flood wait error: Waiting for {e.seconds} seconds.")
        time.sleep(e.seconds)
        await publish_document(content, day, link)

def get_document_content(file_id):
    request = drive_service.files().export_media(fileId=file_id, mimeType='text/plain')
    content = request.execute().decode('utf-8')
    return content

def extract_day_number(content):
    match = re.search(r"#Day(\d+)", content)
    if match:
        return int(match.group(1))
    return None

def get_days_from_full_document(full_document_id):
    full_document = docs_service.documents().get(documentId=full_document_id).execute()
    content = full_document.get('body').get('content')
    days = set()
    for element in content:
        if 'paragraph' in element:
            for text_element in element['paragraph']['elements']:
                if 'textRun' in text_element:
                    text = text_element['textRun']['content']
                    match = re.search(r"Day (\d+)", text)
                    if match:
                        days.add(int(match.group(1)))
    return days

# Function to handle the special cases based on day number
def handle_day_case(extracted_day):
    # Switch case logic for handling different days
    # We use 'match' as a switch-case alternative in Python
    match extracted_day:
        case 1:
            print("Special handling for Day 1")
        case 2:
            print("Special handling for Day 2")
        case 3:
            print("Special handling for Day 3")
        case _:
            print(f"General handling for Day {extracted_day}")

async def main():
    await client.start(phone_number)
    published_days = await get_published_days()
    print(f"Published days: {published_days}")

    full_document_id = None
    query = "name = 'Full' and mimeType = 'application/vnd.google-apps.document'"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if items:
        full_document_id = items[0]['id']
    else:
        print("Full document not found.")
        return

    full_document_days = get_days_from_full_document(full_document_id)
    print(f"Days in full document: {full_document_days}")

    missing_days = full_document_days - published_days
    print(f"Missing days: {missing_days}")

    documents_to_publish = []

    for day in missing_days:
        document_name = f"Day{day}"
        query = f"name contains '{document_name}' and mimeType='application/vnd.google-apps.document'"
        results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        items = results.get('files', [])

        if not items:
            print(f'Document for Day {day} not found.')
        else:
            for item in items:
                file_id = item['id']
                content = get_document_content(file_id)
                extracted_day = extract_day_number(content)
                if extracted_day is not None:
                    link = f"https://docs.google.com/document/d/{file_id}"
                    
                    # Ensure no duplicate day is added
                    if not any(doc[0] == extracted_day for doc in documents_to_publish):
                        documents_to_publish.append((extracted_day, content, link))
                        print(f"Document for Day {extracted_day} ready to publish.")

                        # Switch-case for handling the day number
                        handle_day_case(extracted_day)

    # Sort documents to publish by day number
    documents_to_publish.sort(key=lambda x: x[0])

    for day, content, link in documents_to_publish:
        await publish_document(content, day, link)

with client:
    client.loop.run_until_complete(main())

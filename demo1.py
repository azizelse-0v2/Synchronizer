from telethon.sync import TelegramClient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
import google.auth
import re
import subprocess
import sys

SERVICE_ACCOUNT_FILE = 'review-automation007-f8f92fc64114.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
API_ID = '25504149'
API_HASH = '5cdd1680c1a4f7f49da84b7f6eed0ebb'
CHANNEL_USERNAME = 'Nocommenttesting'
YOUR_EMAIL = 'numonzonovazizbek777@gmail.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
docs_service = build('docs', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

client = TelegramClient('session_name', API_ID, API_HASH)
client.start()

def get_ith_message(i):
    print(f"Fetching the {i}th message from the channel...")
    messages = client.get_messages(CHANNEL_USERNAME, limit=1000)
    filtered_messages = [msg.message for msg in messages if msg.message and msg.message.startswith("#Day")]
    if i < len(filtered_messages):
        print(f"Message found: {filtered_messages[i]}")
        return filtered_messages[i]
    print("No more messages found.")
    return None

def create_google_doc(content, title):
    print(f"Creating Google Doc with title: {title}")
    document = docs_service.documents().create(body={
        'title': title
    }).execute()
    document_id = document['documentId']
    
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': content
            }
        }
    ]
    docs_service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    
    print(f"Google Doc created with ID: {document_id}")
    return document_id

def change_permission(document_id):
    print(f"Changing permissions for document ID: {document_id}")
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    drive_service.permissions().create(
        fileId=document_id,
        body=permission,
        fields='id'
    ).execute()

    permission = {  
        'type': 'user',
        'role': 'writer',
        'emailAddress': YOUR_EMAIL
    }
    drive_service.permissions().create(
        fileId=document_id,
        body=permission,
        fields='id'
    ).execute()
    print(f"Permissions changed for document ID: {document_id}")

def get_document_link(document_id):
    link = f'https://docs.google.com/document/d/{document_id}/edit'
    print(f"Document link: {link}")
    return link

def extract_day_number(message):
    print(f"Extracting day number from message: {message}")
    match = re.match(r"#Day(\d+)", message)
    if match:
        day_number = int(match.group(1))
        print(f"Day number extracted: {day_number}")
        return day_number
    print("No day number found in message.")
    return None

def document_exists(title):
    print(f"Checking if document with title '{title}' exists...")
    response = drive_service.files().list(q=f"name='{title}' and mimeType='application/vnd.google-apps.document'",
                                          spaces='drive',
                                          fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        document_id = files[0]['id']
        print(f"Document found with ID: {document_id}")
        return document_id
    print("Document not found.")
    return None

def update_full_document(full_document_id, full_content):
    if not full_content:
        print("No content to update in the full document.")
        return

    print(f"Updating full document with ID: {full_document_id}")
    requests = []
    for day, link in full_content:
        requests.append({
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': f"Day {day}\n"
            }
        })
        requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 1 + len(f"Day {day}")
                },
                'textStyle': {
                    'link': {
                        'url': link
                    }
                },
                'fields': 'link'
            }
        })
    docs_service.documents().batchUpdate(
        documentId=full_document_id, body={'requests': requests}).execute()
    print(f"Full document updated with new content.")

def save_links_from_document(full_document_id, filename="links_in_full_document.txt"):
    print(f"Extracting and saving links from the full document {full_document_id} to {filename}")
    # Fetch the full document content
    document = docs_service.documents().get(documentId=full_document_id).execute()
    links = []

    # Iterate through document content and extract links
    for element in document.get('body').get('content', []):
        if 'paragraph' in element:
            for text_element in element['paragraph']['elements']:
                if 'textRun' in text_element and 'textStyle' in text_element['textRun']:
                    style = text_element['textRun'].get('textStyle', {})
                    if 'link' in style:
                        link = style['link'].get('url')
                        if link:
                            links.append(link)
    
    # Write the links to a file
    with open(filename, "w") as file:
        for link in links:
            file.write(link + "\n")
    print(f"Links saved to {filename}")

def main():
    print("Starting the main process...")
    i = 0
    full_content = []
    full_document_id = document_exists("Full")
    if not full_document_id:
        full_document_id = create_google_doc("", "Full")
        change_permission(full_document_id)

    full_document = docs_service.documents().get(documentId=full_document_id).execute()
    existing_content = full_document.get('body').get('content')
    existing_days = set()
    for element in existing_content:
        if 'paragraph' in element:
            for text_element in element['paragraph']['elements']:
                if 'textRun' in text_element:
                    text = text_element['textRun']['content']
                    match = re.match(r"Day (\d+)", text)
                    if match:
                        existing_days.add(int(match.group(1)))

    while True:
        message = get_ith_message(i)
        if message is None:
            print("No more messages starting with #Day found.")
            break
        day_number = extract_day_number(message)
        if day_number:
            print(f"Scanned Day {day_number}")
        if day_number and day_number not in existing_days:
            title = f"Day{day_number}"
            document_id = document_exists(title)
            if not document_id:
                document_id = create_google_doc(message, title)
                change_permission(document_id)
                print(f'Document for Day {day_number} created.')
            link = get_document_link(document_id)
            full_content.append((day_number, link))
            print(f'Document for Day {day_number} link: {link}')
        i += 1

    full_content.sort()

    update_full_document(full_document_id, full_content)
    full_link = get_document_link(full_document_id)
    print(f'Full document link: {full_link}')

    # Extract and save links from the full document to a text file
    save_links_from_document(full_document_id)

if __name__ == '__main__':
    main()

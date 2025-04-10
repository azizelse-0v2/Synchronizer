from google.oauth2 import service_account
from googleapiclient.discovery import build
import re
import pyautogui
import pyperclip
import time

SERVICE_ACCOUNT_FILE = 'review-automation007-148b61262097.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
FULL_DOCUMENT_LINK = 'https://docs.google.com/document/d/17SuvGxsblN4IDF0ZOQeZqiu1yzpPgx5JRtPgFT73sCM/edit?tab=t.0'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
docs_service = build('docs', 'v1', credentials=credentials)

def extract_document_id(link):
    print(f"Extracting document ID from link: {link}")
    document_id = link.split('/d/')[1].split('/')[0]
    print(f"Extracted document ID: {document_id}")
    return document_id

def get_full_document_content(document_id):
    print(f"Fetching content of the full document with ID: {document_id}")
    document = docs_service.documents().get(documentId=document_id).execute()
    content = document.get('body').get('content')
    print("Fetched full document content.")
    return content

def extract_links(content):
    print("\nExtracting links from the full document content")
    links = []
    for element in content:
        if 'paragraph' in element:
            for text_element in element['paragraph']['elements']:
                if 'textRun' in text_element and 'link' in text_element['textRun']['textStyle']:
                    link = text_element['textRun']['textStyle']['link']['url']
                    links.append(link)
                    print(f"Found link: {link}")
    print("Extracted all links.")
    return links

def get_day_document_title(link):
    document_id = extract_document_id(link)
    print(f"Fetching content of the day document with ID: {document_id}")
    try:
        document = docs_service.documents().get(documentId=document_id).execute()
        content = document.get('body').get('content')
        for element in content:
            if 'paragraph' in element:
                for text_element in element['paragraph']['elements']:
                    if 'textRun' in text_element:
                        text = text_element['textRun']['content']
                        print(f"Found text: {text}")
                        match = re.match(r"#Day\d+\s+(.*)", text)
                        if match:
                            title = match.group(1)
                            print(f"Extracted title: {title}")
                            return title
    except Exception as e:
        print(f"Error fetching document with ID {document_id}: {e}")
    return None

def login_and_navigate():
    print("Opening the browser in incognito mode and navigating to the login page.")
    pyautogui.hotkey('win', 'r')
    time.sleep(0.2)
    pyautogui.typewrite('chrome --incognito https://dash.infinityfree.com/accounts/if0_38479255/domains/nocommentreviews.lovestoblog.com\n')
    time.sleep(5)

    print("Waiting for the user to complete the Cloudflare CAPTCHA.")
    pyautogui.alert('Please complete the Cloudflare CAPTCHA and then click OK to continue.')

    pyautogui.hotkey('shift','tab')
    pyautogui.hotkey('shift','tab')
    pyautogui.hotkey('shift','tab')
    pyautogui.hotkey('shift','tab')
    pyautogui.typewrite('a.nomonjonov2027@tashkentps.uz')
    pyautogui.hotkey('tab')
    pyautogui.hotkey('tab')
    pyautogui.typewrite(',6iLJ)nunQ&Y,8_')
    pyautogui.press('enter')
    time.sleep(5)

    print("Navigating to the website builder.")
    website_builder_button = pyautogui.locateCenterOnScreen('website_builder_button.png', confidence=0.8)
    if website_builder_button:
        pyautogui.click(website_builder_button)
    else:
        print("The website builder button was not found on the screen.")
        return

    time.sleep(20)

    print("Scrolling down until the specific text is found.")
    text_location = None
    scroll_attempts = 0
    max_scroll_attempts = 1000
    while not text_location and scroll_attempts < max_scroll_attempts:
        try:
            text_location = pyautogui.locateCenterOnScreen('explore_text.png', confidence=0.8)
        except pyautogui.ImageNotFoundException:
            text_location = None

        if not text_location:
            pyautogui.scroll(-250)
            time.sleep(0.5)
            scroll_attempts += 1

    if text_location:
        time.sleep(2)
        print("Specific text found. Performing text operations.")
        pyautogui.doubleClick(text_location)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        pyperclip.copy("Explore my collection of reviewed and summarized articles—I hope you find something intriguing! Link to the list of all article reviews -- CLICK")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'shift', 'left')
        pyautogui.hotkey('ctrl', 'k')
        time.sleep(1)

        https_button = pyautogui.locateOnScreen('https_button.png', confidence=0.8)
        if https_button:
            pyautogui.click(https_button)
            time.sleep(0.5)
            pyperclip.copy(FULL_DOCUMENT_LINK)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            apply_button = pyautogui.locateOnScreen('apply_button.png', confidence=0.8)
            if apply_button:
                pyautogui.click(apply_button)
                time.sleep(0.5)
            else:
                print("apply_button.png not found on the screen.")
        else:
            print("https_button.png not found on the screen.")
        pyautogui.press('right')
        pyautogui.press('enter')
        pyautogui.write("asdf")
        pyautogui.press('enter')
        pyautogui.write("asdf")
        for _ in range(2):
            pyautogui.hotkey('shift', 'ctrl', 'left')

        numbered_list_button = pyautogui.locateOnScreen('numbered_list_button.png', confidence=0.8)
        if numbered_list_button:
            pyautogui.click(numbered_list_button)
            time.sleep(0.5)
            pyautogui.hotkey('right')
            pyautogui.typewrite(['backspace'] * 9, interval=0.01)
        else:
            print("numbered_list_button.png not found on the screen.")
    else:
        print("The specific text was not found on the screen.")

def main():
    print("Starting the main process.")
    login_and_navigate()

    result = []
    full_document_id = extract_document_id(FULL_DOCUMENT_LINK)
    full_content = get_full_document_content(full_document_id)
    links = extract_links(full_content)
    for link in links:
        title = get_day_document_title(link)
        if title:
            result.append((title, link))
    print("Final result:", result)

    for title, link in result:
        print(f"Processing title: {title} with link: {link}")
        pyperclip.copy(title)
        pyautogui.hotkey('ctrl', 'v')


        pyautogui.press('space')

        pyautogui.typewrite(" - link")


        pyautogui.hotkey('ctrl', 'shift', 'left')


        pyperclip.copy(link)
        pyautogui.hotkey('ctrl', 'k')


        time.sleep(0.5)

        https_button = pyautogui.locateOnScreen('https_button.png', confidence=0.8)
        if https_button:
            pyautogui.click(https_button)
            time.sleep(0.1)
        else:
            print("https_button.png not found on the screen.")

        pyautogui.hotkey('ctrl', 'v')


        apply_button = pyautogui.locateOnScreen('apply_button.png', confidence=0.8)
        if apply_button:
            pyautogui.click(apply_button)
            time.sleep(0.1)
        else:
            print("apply_button.png not found on the screen.")

        pyautogui.press('right')


        pyautogui.press('enter')

    pyautogui.hotkey('backspace')
    
    done_button = pyautogui.locateOnScreen('done_button.png', confidence=0.8)
    if done_button:
        pyautogui.click(done_button)
        time.sleep(0.5)
    else:
        print("done_button.png not found on the screen.")

    publish_button = pyautogui.locateOnScreen('publish_button.png', confidence=0.8)
    if publish_button:
        pyautogui.click(publish_button)
        time.sleep(0.5)
    else:
        print("publish_button.png not found on the screen.")

    pyautogui.press('backspace')
    print("Process completed.")
    

if __name__ == '__main__':
    main()
import cv2
import numpy as np
import pyautogui
import pyperclip
import time
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'review-automation007-148b61262097.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
FULL_DOCUMENT_LINK = 'https://docs.google.com/document/d/17SuvGxsblN4IDF0ZOQeZqiu1yzpPgx5JRtPgFT73sCM/edit?tab=t.0'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
docs_service = build('docs', 'v1', credentials=credentials)

def extract_document_id(link):
    return link.split('/d/')[1].split('/')[0]

def get_full_document_content(document_id):
    document = docs_service.documents().get(documentId=document_id).execute()
    return document.get('body').get('content')

def extract_links(content):
    links = []
    for element in content:
        if 'paragraph' in element:
            for text_element in element['paragraph']['elements']:
                if 'textRun' in text_element and 'link' in text_element['textRun']['textStyle']:
                    links.append(text_element['textRun']['textStyle']['link']['url'])
    return links

def get_day_document_title(link):
    document_id = extract_document_id(link)
    try:
        document = docs_service.documents().get(documentId=document_id).execute()
        content = document.get('body').get('content')
        for element in content:
            if 'paragraph' in element:
                for text_element in element['paragraph']['elements']:
                    if 'textRun' in text_element:
                        text = text_element['textRun']['content']
                        match = re.match(r"#Day\d+\s+(.*)", text)
                        if match:
                            return match.group(1)
    except Exception as e:
        print(f"Error: {e}")
    return None

def locate_on_screen_template(template_path, confidence=0.8, grayscale=True, max_scale_variation=0.2):
    screenshot = pyautogui.screenshot()
    screen_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY if grayscale else cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, 0 if grayscale else 1)
    h, w = template.shape[:2]
    best_match = None
    best_val = 0
    for scale in np.linspace(1 - max_scale_variation, 1 + max_scale_variation, 10):
        resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
        res = cv2.matchTemplate(screen_img, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > confidence and max_val > best_val:
            best_val = max_val
            best_match = (max_loc[0] + resized_template.shape[1] // 2,
                          max_loc[1] + resized_template.shape[0] // 2)
    return best_match

def click_template(template_path):
    location = locate_on_screen_template(template_path)
    if location:
        pyautogui.click(location)
        return True
    print(f"{template_path} not found on screen.")
    return False

def login_and_navigate():
    pyautogui.hotkey('win', 'r')
    time.sleep(0.2)
    pyautogui.typewrite('chrome --incognito https://dash.infinityfree.com/accounts/if0_38479255/domains/nocommentreviews.lovestoblog.com\n')
    time.sleep(5)
    pyautogui.alert('Complete Cloudflare CAPTCHA, then click OK.')

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

    click_template('website_builder_button.png')
    time.sleep(20)

    for _ in range(100):
        text_location = locate_on_screen_template('explore_text.png')
        if text_location:
            pyautogui.doubleClick(text_location)
            break
        pyautogui.scroll(-250)
        time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    pyperclip.copy("Explore my collection of reviewed and summarized articles—I hope you find something intriguing! Link to the list of all article reviews -- CLICK")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('ctrl', 'shift', 'left')
    pyautogui.hotkey('ctrl', 'k')

    if click_template('https_button.png'):
        pyperclip.copy(FULL_DOCUMENT_LINK)
        pyautogui.hotkey('ctrl', 'v')
        click_template('apply_button.png')

    pyautogui.press('right')
    pyautogui.press('enter')
    pyautogui.write("asdf")
    pyautogui.press('enter')
    pyautogui.write("asdf")
    for _ in range(2):
        pyautogui.hotkey('shift', 'ctrl', 'left')
    click_template('numbered_list_button.png')
    pyautogui.hotkey('right')
    pyautogui.typewrite(['backspace'] * 9, interval=0.01)

def main():
    login_and_navigate()
    result = []
    full_content = get_full_document_content(extract_document_id(FULL_DOCUMENT_LINK))
    links = extract_links(full_content)
    for link in links:
        title = get_day_document_title(link)
        if title:
            result.append((title, link))

    for title, link in result:
        pyperclip.copy(title)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('space')
        pyautogui.typewrite(" - link")
        pyautogui.hotkey('ctrl', 'shift', 'left')
        pyperclip.copy(link)
        pyautogui.hotkey('ctrl', 'k')
        time.sleep(0.5)
        click_template('https_button.png')
        pyautogui.hotkey('ctrl', 'v')
        click_template('apply_button.png')
        pyautogui.press('right')
        pyautogui.press('enter')

    pyautogui.hotkey('backspace')
    click_template('done_button.png')
    click_template('publish_button.png')
    pyautogui.press('backspace')
    print("Automation complete.")

if __name__ == '__main__':
    main()

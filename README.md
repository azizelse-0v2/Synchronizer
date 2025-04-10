# Demo Automation and Synchronization App

This project provides an automation and synchronization application with a GUI interface, designed to interact with Telegram, Google Docs, and web services. The application allows you to fetch and publish Telegram messages to Google Docs, manage missing days from Google Docs, and delete specific messages from Telegram channels. The app is built with Python and uses several popular libraries like `Telethon`, `google-api-python-client`, and `Tkinter` for the GUI.

## Features

- **Feature One**: Fetch messages from a Telegram channel and save them to Google Docs.
- **Feature Two**: Extract links from Google Docs and save the content to a website.
- **Feature Three**: Fetch Google Docs links and post missing days.
- **Feature Four**: Delete messages with a specific hashtag (`#Day`) from a Telegram channel.

## GUI

The application uses a Tkinter-based GUI, which displays a list of features along with their respective icons. Each feature can be triggered via buttons, and the output of the executed scripts is shown in a terminal-like section of the GUI. 

## Setup

To run this project, follow the steps below to install the necessary dependencies and run the application.

### Prerequisites

- Python 3.x
- A Telegram account with the necessary permissions to interact with the target Telegram channel.
- A Google Cloud project with the appropriate credentials (`review-automation007-148b61262097.json`) for Google Docs API.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/azizelse-0v2/demo-automation.git
   cd demo-automation
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Place your Google Cloud credentials file (review-automation007-148b61262097.json) in the project directory.

Run the application:

bash
Copy
Edit
python full.py
Libraries Used
telethon: To interact with Telegram API.

google-api-python-client: To interact with Google Docs and Drive API.

PIL (Python Imaging Library): To handle image processing for icons.

tkinter: To build the GUI interface.

License
This project is licensed under the MIT License - see the LICENSE file for details.

yaml
Copy
Edit

---

### `requirements.txt`:

```txt
telethon==1.24.0
google-api-python-client==2.80.0
google-auth==2.16.0
google-auth-oauthlib==0.4.6
google-auth-httplib2==0.1.0
Pillow==9.1.1
tk==0.1.0

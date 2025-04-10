import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import threading
import io

# Load a transparent image
def load_transparent_image(file, size=(60, 60)):
    img = Image.open(file).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Function to run the script in the background
def run_script(script_name):
    process = subprocess.Popen([sys.executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end='')
    for line in process.stderr:
        print(line, end='')

# Feature functions that call run_script in a separate thread
def feature_one():
    threading.Thread(target=run_script, args=("demo1.py",), daemon=True).start()

def feature_two():
    threading.Thread(target=run_script, args=("demo2.py",), daemon=True).start()

def feature_three():
    threading.Thread(target=run_script, args=("demo3.py",), daemon=True).start()

def feature_four():
    threading.Thread(target=run_script, args=("demo4.py",), daemon=True).start()

# Main GUI Setup
root = tk.Tk()
root.title("Demo Application")
root.geometry("1000x600")
root.configure(bg='#2c3e50')
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Load transparent icons
telegram_icon = load_transparent_image("telegram.png")
google_docs_icon = load_transparent_image("google_docs.png")
web_icon = load_transparent_image("web.png")
delete_icon = load_transparent_image("delete.png")
arrow_icon = load_transparent_image("arrow.png")

# Title label
background_label = tk.Label(root, text="Synchronizer", font=("Helvetica", 36, "bold"), fg="white", bg='#2c3e50')
background_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

# Main Frame
main_frame = tk.Frame(root, bg='#2c3e50')
main_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# Terminal Frame
terminal_frame = tk.Frame(root, bg='#2c3e50')
terminal_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
terminal_frame.grid_rowconfigure(0, weight=1)
terminal_frame.grid_columnconfigure(0, weight=1)

# Function to add feature description with icons
def add_feature_description(parent, text, icon1, icon2):
    frame = tk.Frame(parent, bg='#2c3e50')
    frame.pack(pady=2, fill=tk.BOTH, expand=True)
    frame.grid_columnconfigure(1, weight=1)

    icon_label1 = tk.Label(frame, image=icon1, bg="#2c3e50")
    icon_label1.grid(row=0, column=0, padx=5)

    arrow_label = tk.Label(frame, image=arrow_icon, bg="#2c3e50")
    arrow_label.grid(row=0, column=1, padx=5)

    icon_label2 = tk.Label(frame, image=icon2, bg="#2c3e50")
    icon_label2.grid(row=0, column=2, padx=5)

    label_text = tk.Label(frame, text=text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="w")
    label_text.grid(row=0, column=3, sticky="w", padx=10)

# Add feature descriptions
add_feature_description(main_frame, "Fetch Telegram messages and save to Google Docs", telegram_icon, google_docs_icon)
add_feature_description(main_frame, "Extract links from Google Docs and save content to the website", google_docs_icon, web_icon)
add_feature_description(main_frame, "Fetch Google Docs links and post the missing days", google_docs_icon, google_docs_icon)
add_feature_description(main_frame, "Delete messages with a specific hashtag from Telegram", telegram_icon, delete_icon)

# Buttons Frame
button_frame = tk.Frame(main_frame, bg='#2c3e50')
button_frame.pack(pady=10, fill=tk.BOTH, expand=True)
button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_rowconfigure(1, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

# Button styles
button_style = {
    "font": ("Helvetica", 14, "bold"),
    "bg": "#3498db",
    "fg": "white",
    "activebackground": "#2980b9",
    "activeforeground": "white",
    "relief": tk.RAISED,
    "bd": 5,
    "width": 15,
    "height": 2
}

# Define buttons
button1 = tk.Button(button_frame, text="Feature One", command=feature_one, **button_style)
button1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

button2 = tk.Button(button_frame, text="Feature Two", command=feature_two, **button_style)
button2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

button3 = tk.Button(button_frame, text="Feature Three", command=feature_three, **button_style)
button3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

button4 = tk.Button(button_frame, text="Feature Four", command=feature_four, **button_style)
button4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Terminal Output widget
terminal_text = tk.Text(terminal_frame, wrap=tk.WORD, bg='black', fg='white', font=("Helvetica", 10))
terminal_text.grid(row=0, column=0, sticky="nsew")

# Class to redirect stdout and stderr to the terminal_text widget
class RedirectText(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

# Redirect stdout and stderr
sys.stdout = RedirectText(terminal_text)
sys.stderr = RedirectText(terminal_text)

# Run the main loop
root.mainloop()

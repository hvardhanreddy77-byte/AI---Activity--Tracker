
import json

import os
import time
from datetime import datetime

import pygetwindow as gw

# ---------------------------------
# PATHS
# ---------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOGS_DIR, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")

LOG_FILE = os.path.join(
    LOGS_DIR,
    f"{today}.json"
)

INTERVAL = 15

# ---------------------------------
# CREATE FILE IF NOT EXISTS
# ---------------------------------

if not os.path.exists(LOG_FILE):

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# ---------------------------------
# ACTIVE WINDOW
# ---------------------------------

def get_active_title():

    try:

        window = gw.getActiveWindow()

        if window:
            return window.title

    except:
        pass

    return None

# ---------------------------------
# SITE DETECTION
# ---------------------------------

def get_site(title):

    t = title.lower()

    if "youtube" in t:
        return "YouTube"

    if "leetcode" in t:
        return "LeetCode"

    if "chatgpt" in t:
        return "ChatGPT"

    if "visual studio code" in t:
        return "VS Code"

    if "github" in t:
        return "GitHub"

    if "brave search" in t:
        return "Brave Search"

    if "students.bmsce" in t:
        return "College"

    if "brave" in t:
        return "Brave"

    return "Other"

# ---------------------------------
# LOAD LOG
# ---------------------------------

def load_log():

    try:

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []

# ---------------------------------
# SAVE LOG
# ---------------------------------

def save_log(data):

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

# ---------------------------------
# TRACKER
# ---------------------------------

print("Tracker Started...")
print("Logging to:", LOG_FILE)

last_title = None


while True:
    try:
        title = get_active_title()
    except Exception as e:
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} : {str(e)}\n")
        time.sleep(5)
        

        if not title:
            time.sleep(INTERVAL)
            continue

        if title == last_title:
            time.sleep(INTERVAL)
            continue

        last_title = title

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "site": get_site(title),
            "title": title
        }

        data = load_log()
        data.append(entry)
        save_log(data)

        print(entry)

        time.sleep(INTERVAL)
import json
import traceback
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

# How often to check active window
INTERVAL = 15

# ---------------------------------
# CREATE LOG FILE IF NEEDED
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

    except Exception:
        pass

    return None

# ---------------------------------
# SITE DETECTION
# ---------------------------------

def get_site(title):

    if not title:
        return "Other"

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

    except Exception:
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

last_title = get_active_title()
last_time = time.time()

while True:

    try:

        time.sleep(INTERVAL)

        current_title = get_active_title()

        if not current_title:
            continue

        # Same window → keep counting time
        if current_title == last_title:
            continue

        duration = int(
            time.time() - last_time
        )

        # Save previous activity
        entry = {

            "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "site":
            get_site(last_title),

            "title":
            last_title,

            "duration_seconds":
            duration
        }

        data = load_log()
        data.append(entry)
        save_log(data)

        # Start tracking new window
        last_title = current_title
        last_time = time.time()

    except Exception:

        with open(
            "error.log",
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"\n{datetime.now()}\n"
            )

            f.write(
                traceback.format_exc()
            )

            f.write("\n")

        time.sleep(5)
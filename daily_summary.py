import json
import os
from collections import Counter
from datetime import datetime

from ollama import chat
from plyer import notification

# ---------------------------------
# TODAY'S LOG FILE
# ---------------------------------

today = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = f"logs/{today}.json"

# ---------------------------------
# LOAD LOG
# ---------------------------------

try:
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

except FileNotFoundError:
    print(f"No log file found: {LOG_FILE}")
    exit()

if not data:
    print("No activity found")
    exit()

# ---------------------------------
# CATEGORIZATION
# ---------------------------------

def categorize(title):

    t = title.lower()

    coding_keywords = [
        "leetcode",
        "github",
        "visual studio code",
        "python",
        "playwright",
        "ollama",
        ".py",
        "coding",
        "programming"
    ]

    learning_keywords = [
        "chatgpt",
        "tutorial",
        "course",
        "guide",
        "documentation",
        "ai",
        "machine learning",
        "how to",
        "mistakes"
    ]

    college_keywords = [
        "students.bmsce",
        "attendance",
        "cie",
        "semester",
        "college",
        "assignment",
        "exam"
    ]

    entertainment_keywords = [
        "youtube",
        "song",
        "music",
        "movie",
        "video",
        "teaser",
        "trailer",
        "spotify"
    ]
    system_keywords = [
    "cmd.exe",
    "task scheduler",
    "file explorer",
    "windows powershell",
    "search",
    "startup"
    ]

    for word in coding_keywords:
        if word in t:
            return "Coding"

    for word in learning_keywords:
        if word in t:
            return "Learning"

    for word in college_keywords:
        if word in t:
            return "College"

    for word in entertainment_keywords:
        if word in t:
            return "Entertainment"
    for word in system_keywords:
        if word in t:
            return "System"

    return "Other"


# ---------------------------------
# TIME SPENT ANALYSIS
# ---------------------------------

INTERVAL = 15  # seconds between logs

category_time = Counter()
title_time = Counter()

for entry in data:

    title = entry.get("title", "")

    if not title:
        continue

    category = categorize(title)

    category_time[category] += INTERVAL
    title_time[title] += INTERVAL

# ---------------------------------
# CATEGORY BREAKDOWN
# ---------------------------------

total_seconds = sum(category_time.values())

breakdown = ""

for category in [
    "Coding",
    "Learning",
    "Entertainment",
    "College",
    "Other"
]:

    seconds = category_time.get(category, 0)

    minutes = round(seconds / 60, 1)

    percent = round(
        seconds * 100 / total_seconds,
        1
    ) if total_seconds else 0

    breakdown += (
        f"{category}: "
        f"{minutes} minutes "
        f"({percent}%)\n"
    )

# ---------------------------------
# TOP ACTIVITIES BY TIME
# ---------------------------------

top_activities = sorted(
    title_time.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

top_text = ""

for title, seconds in top_activities:

    minutes = round(seconds / 60, 1)

    top_text += (
        f"- {title}: "
        f"{minutes} minutes\n"
    )

# ---------------------------------
# MOST TIME SPENT
# ---------------------------------

most_title, most_seconds = max(
    title_time.items(),
    key=lambda x: x[1]
)

most_minutes = round(
    most_seconds / 60,
    1
)
# ---------------------------------
# AI PROMPT
# ---------------------------------
prompt = f"""
You are a personal productivity analyst.

MOST TIME SPENT:

{most_title}
({most_minutes} minutes)

CATEGORY BREAKDOWN:

{breakdown}

TOP ACTIVITIES:

{top_text}

Your task:

1. Tell me what I spent most time on.
2. Mention the exact titles of the top 3 activities.
3. Estimate whether the day was:
   - Mostly Productive
   - Balanced
   - Mostly Entertainment
4. Give one specific observation.
5. Give one suggestion.

Do not give generic advice.
Use the activity titles provided.

Use this format:

TODAY

Most Time Spent:
...

Top Activities:
1. ...
2. ...
3. ...

Productive:
...

Learning:
...

Entertainment:
...

SUMMARY:
...

TOMORROW:
...
"""
# ---------------------------------
# OLLAMA
# ---------------------------------

print("\nTOP ACTIVITIES:")
print(top_text)

print("CATEGORY BREAKDOWN:")
print(breakdown)

print("Analyzing activity...\n")

response = chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

summary = response["message"]["content"]

# ---------------------------------
# PRINT
# ---------------------------------

print(summary)

# ---------------------------------
# SAVE SUMMARY
# ---------------------------------

os.makedirs("summaries", exist_ok=True)

SUMMARY_FILE = f"summaries/{today}.txt"

with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
    f.write(summary)

# ---------------------------------
# NOTIFICATION
# ---------------------------------

short_summary = (
    f"Most time: {most_title}\n"
    f"Time spent: {most_minutes} min"
)

notification.notify(
    title="📊 Daily Summary",
    message=short_summary,
    timeout=20
)

# ---------------------------------
# OPEN SUMMARY
# ---------------------------------
print("Summary path:", SUMMARY_FILE)
print("Exists:", os.path.exists(SUMMARY_FILE))
print(os.path.abspath(SUMMARY_FILE))
os.startfile(os.path.abspath(SUMMARY_FILE))

print(f"\nSummary saved to: {SUMMARY_FILE}")
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os
import sqlite3
import re

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

SESSION_STRING = os.getenv("SESSION_STRING")

client = TelegramClient(
    StringSession(SESSION_STRING),
    api_id,
    api_hash
)

# =========================
# Create DB + Table
# =========================

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TEXT
)
""")

conn.commit()
conn.close()

# =========================
# Allowed Channels
# =========================

ALLOWED_CHANNELS = [
    "KLU Placements -2027 batch (official)",
    "2027 BATCH - KL Placements Announcement",
    "CareerBridge - Job | Internship | Upskill",
    "MyCareernet: Jobs, Hackathons, Hiring Events",
    "Jobs | Internships | Placement | Interviews",
    "Arsh Goyal : Youtube",
    "AI Jobs | Artificial Intelligence"
]

# =========================
# Keywords
# =========================

KEYWORDS = [
    "intern",
    "internship",
    "job",
    "hiring",
    "apply",
    "developer",
    "engineer",
    "sde",
    "graduate",
    "fresher",
    "off campus",
    "software",
    "placement",
    "opportunity"
]

# =========================
# Listener
# =========================

@client.on(events.NewMessage)
async def handler(event):

    print("\n📨 EVENT RECEIVED")

    chat = await event.get_chat()

    channel_name = getattr(chat, "title", "Private Chat")
    channel_username = getattr(chat, "username", None)

    print("📢 Channel:", channel_name)

    if channel_name not in ALLOWED_CHANNELS:
        print("❌ Channel Not Allowed")
        return

    text = event.text or ""

    print("📝 Text Length:", len(text))

    text_lower = text.lower()

    if not any(keyword in text_lower for keyword in KEYWORDS):
        print("❌ No Matching Keyword")
        return

    print("✅ Passed Filters")

    print("\n========== JOB POST ==========")
    print("Channel :", channel_name)
    print("Username:", channel_username)
    print("Message :", event.id)

    # =========================
    # Extract Link
    # =========================

    links = re.findall(r'https?://\S+', text)

    job_link = None

    if links:
        job_link = links[0]
        print("🔗 Text URL:", job_link)

    # Telegram Button URLs

    if not job_link and event.message.buttons:

        print("🔘 Buttons Found")

        for row in event.message.buttons:
            for button in row:

                url = getattr(button, "url", None)

                if url:
                    job_link = url
                    print("🔗 Button URL:", url)
                    break

            if job_link:
                break

    # Telegram Post URL

    if not job_link:

        if channel_username:
            job_link = (
                f"https://t.me/"
                f"{channel_username}/"
                f"{event.id}"
            )

            print("🔗 Telegram URL:", job_link)

        else:
            job_link = "No Link Found"

            print("⚠️ No Link Found")

    job_title = text[:200]

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM jobs WHERE title=?",
        (job_title,)
    )

    existing = cursor.fetchone()

    if existing:

        print("⚠️ Duplicate Job Ignored")

    else:

        cursor.execute(
            """
            INSERT INTO jobs(title, link, created_at)
            VALUES(?, ?, datetime('now'))
            """,
            (
                job_title,
                job_link
            )
        )

        conn.commit()

        print("✅ Job Saved")
        print("💾 Saved To Database")
        print("🔗 Link:", job_link)

    conn.close()


client.start()

print("🚀 PlaceMate Listener Running...")

client.run_until_disconnected()
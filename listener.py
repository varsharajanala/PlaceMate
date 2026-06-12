
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

ALLOWED_CHANNELS = [
    "KLU Placements -2027 batch (official)",
    "2027 BATCH - KL Placements Announcement",
    "CareerBridge - Job | Internship | Upskill",
    "MyCareernet: Jobs, Hackathons, Hiring Events",
    "Jobs | Internships | Placement | Interviews",
    "Arsh Goyal : Youtube",
    "AI Jobs | Artificial Intelligence"
]

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


@client.on(events.NewMessage)
async def handler(event):

    chat = await event.get_chat()

    channel_name = getattr(chat, "title", "Private Chat")
    channel_username = getattr(chat, "username", None)

    if channel_name not in ALLOWED_CHANNELS:
        return

    text = event.text or ""

    text_lower = text.lower()

    if not any(keyword in text_lower for keyword in KEYWORDS):
        return

    print("\n========== JOB POST ==========")
    print("Channel :", channel_name)
    print("Username:", channel_username)
    print("Message :", event.id)

    # 1. Try URL from message text
    links = re.findall(r'https?://\S+', text)

    job_link = None

    if links:
        job_link = links[0]

    # 2. Try URL from Telegram buttons
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

    # 3. Telegram post fallback
    if not job_link:

        if channel_username:
            job_link = (
                f"https://t.me/"
                f"{channel_username}/"
                f"{event.id}"
            )

        else:
            job_link = "No Link Found"

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
        print("🔗 Link:", job_link)

    conn.close()


client.start()

print("🚀 PlaceMate Listener Running...")

client.run_until_disconnected()

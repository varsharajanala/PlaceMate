from telethon import TelegramClient
from dotenv import load_dotenv
import os
import sqlite3
from datetime import date
import re

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient(
    "placemate_session",
    api_id,
    api_hash
)

CHANNELS = [
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


async def main():

    today = date.today()

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    dialogs = await client.get_dialogs()

    for dialog in dialogs:

        if dialog.name not in CHANNELS:
            continue

        print(f"\n📢 Checking: {dialog.name}")

        async for msg in client.iter_messages(
            dialog.entity,
            limit=200
        ):

            if not msg.text:
                continue

            if msg.date.date() != today:
                continue

            text = msg.text

            text_lower = text.lower()

            if not any(
                keyword in text_lower
                for keyword in KEYWORDS
            ):
                continue

            links = re.findall(
                r'https?://\S+',
                text
            )

            job_link = (
                links[0]
                if links
                else "No Link Found"
            )

            job_title = text[:200]

            cursor.execute(
                "SELECT id FROM jobs WHERE title=?",
                (job_title,)
            )

            existing = cursor.fetchone()

            if existing:
                print("⚠️ Duplicate Ignored")
                continue

            cursor.execute(
                """
                INSERT INTO jobs(title, link)
                VALUES(?, ?)
                """,
                (
                    job_title,
                    job_link
                )
            )

            print("✅ Saved")

    conn.commit()
    conn.close()

    print("\n🎉 Today's Jobs Imported Successfully!")


with client:
    client.loop.run_until_complete(main())
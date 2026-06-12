
from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)
import sqlite3

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 PlaceMate Bot is Active!"
    )


async def addjob(update: Update, context: ContextTypes.DEFAULT_TYPE):

    title = " ".join(context.args)

    if not title:
        await update.message.reply_text(
            "Usage: /addjob Job Name"
        )
        return

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO jobs(title) VALUES(?)",
        (title,)
    )

    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"✅ Job Added:\n{title}"
    )


async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, link
        FROM jobs
        WHERE status='Pending'
        """
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        await update.message.reply_text(
            "No Pending Jobs 🎉"
        )
        return

    for index, job in enumerate(rows, start=1):

        keyboard = []

        if job[2] and job[2] != "No Link Found":
            keyboard.append([
                InlineKeyboardButton(
                    "🔗 Open Job",
                    url=job[2]
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "✅ Applied",
                callback_data=f"applied_{job[0]}"
            )
        ])

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        await update.message.reply_text(
            f"{index}. 📌 {job[1]}",
            reply_markup=reply_markup
        )


async def applied(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /applied JobID"
        )
        return

    job_id = context.args[0]

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE jobs SET status='Applied' WHERE id=?",
        (job_id,)
    )

    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"✅ Job {job_id} marked as Applied"
    )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Chat ID: {update.effective_chat.id}"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM jobs"
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status='Pending'"
    )
    pending = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status='Applied'"
    )
    applied_count = cursor.fetchone()[0]

    conn.close()

    await update.message.reply_text(
        f"📊 PlaceMate Stats\n\n"
        f"📌 Total Jobs: {total}\n"
        f"⏳ Pending: {pending}\n"
        f"✅ Applied: {applied_count}"
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    if data.startswith("applied_"):

        job_id = data.split("_")[1]

        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE jobs SET status='Applied' WHERE id=?",
            (job_id,)
        )

        conn.commit()
        conn.close()

        await query.edit_message_text(
            "✅ Marked as Applied"
        )


async def reminder_job(context):

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, link
        FROM jobs
        WHERE status='Pending'
        """
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=(
            f"⚠️ Pending Applications\n\n"
            f"Total Pending: {len(rows)}"
        )
    )

    for index, job in enumerate(rows[:10], start=1):

        title = job[1]
        link = job[2]

        keyboard = []

        if link and link != "No Link Found":
            keyboard.append([
                InlineKeyboardButton(
                    "🔗 Open Job",
                    url=link
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "✅ Applied",
                callback_data=f"applied_{job[0]}"
            )
        ])

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"{index}. 📌 {title}",
            reply_markup=reply_markup
        )


async def cleanup_old_jobs(context):

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM jobs
    WHERE datetime(created_at)
    < datetime('now', '-1 day')
    """)

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    if deleted > 0:
        print(f"🗑 Deleted {deleted} expired jobs")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addjob", addjob))
app.add_handler(CommandHandler("jobs", jobs))
app.add_handler(CommandHandler("applied", applied))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(button_handler))

app.job_queue.run_repeating(
    reminder_job,
    interval=1800,
    first=10
)

app.job_queue.run_repeating(
    cleanup_old_jobs,
    interval=3600,
    first=60
)

print("🚀 PlaceMate Bot Running...")

app.run_polling()

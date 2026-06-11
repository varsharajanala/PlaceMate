from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)
import sqlite3

TOKEN = "8536189015:AAE7FI3iO__EbRSz45Il7FX00JfBdbiF4xQ"
CHAT_ID = 6189440183


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Placement Reminder Bot is Active!"
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
        "SELECT id, title FROM jobs WHERE status='Pending'"
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        await update.message.reply_text(
            "No Pending Jobs 🎉"
        )
        return

    for job in rows:

        keyboard = [[
            InlineKeyboardButton(
                "✅ Applied",
                callback_data=f"applied_{job[0]}"
            )
        ]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"📌 {job[1]}",
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
        "SELECT id, title FROM jobs WHERE status='Pending'"
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return

    message = "⚠️ Pending Applications\n\n"

    for job in rows:
        message += f"{job[0]}. {job[1]}\n"

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addjob", addjob))
app.add_handler(CommandHandler("jobs", jobs))
app.add_handler(CommandHandler("applied", applied))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CallbackQueryHandler(button_handler))

# Reminder every 6 hours
app.job_queue.run_repeating(
    reminder_job,
    interval=21600,
    first=10
)

print("Bot Running...")

app.run_polling()
# 🚀 PlaceMate

PlaceMate is an automated placement opportunity aggregator built using Python, Telethon, Telegram Bot API, and SQLite.

It continuously monitors selected Telegram placement channels, extracts job and internship opportunities, stores them in a database, and sends personalized reminders through a Telegram bot.

---

## ✨ Features

### 📢 Automatic Job Collection

* Monitors multiple Telegram placement channels
* Captures new job and internship posts automatically
* Filters only placement-related opportunities

### 🔗 Direct Apply Links

* Extracts application URLs from:

  * Message content
  * Telegram buttons
  * Channel post links (fallback)

### 📋 Job Tracking

* Stores opportunities in SQLite database
* Prevents duplicate entries
* Tracks application status

### 🤖 Telegram Bot

Commands:

```bash
/start
/jobs
/stats
/myid
```

### ✅ Application Management

* Mark opportunities as Applied
* View Pending Applications
* Track placement progress

### ⏰ Smart Reminders

* Sends pending job reminders every 30 minutes
* Includes direct Apply buttons
* Shows latest opportunities automatically

### 🗑 Auto Cleanup

* Removes outdated opportunities
* Keeps only fresh placement posts
* Database stays clean automatically

---

## 🏗 Architecture

Telegram Channels
↓
Telethon Listener
↓
SQLite Database
↓
Telegram Bot
↓
User Notifications

---

## 🛠 Tech Stack

* Python
* Telethon
* Python Telegram Bot
* SQLite
* Python Dotenv

---

## 📁 Project Structure

```text
telegram-job-reminder-bot/
│
├── bot.py
├── listener.py
├── fetch_today_jobs.py
├── db.py
├── jobs.db
├── .env
├── requirements.txt
├── README.md
└── placemate_session.session
```

---

## ⚙️ Setup

### Clone Repository

```bash
git clone <repository-url>
cd telegram-job-reminder-bot
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create `.env`

```env
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH

BOT_TOKEN=YOUR_BOT_TOKEN
CHAT_ID=YOUR_CHAT_ID
```

---

## ▶️ Run Database Setup

```bash
python db.py
```

---

## ▶️ Start Listener

```bash
python listener.py
```

---

## ▶️ Start Bot

```bash
python bot.py
```

---

## 📲 Supported Channels

* KLU Placements -2027 batch (official)
* 2027 BATCH - KL Placements Announcement
* CareerBridge - Job | Internship | Upskill
* MyCareernet: Jobs, Hackathons, Hiring Events
* Jobs | Internships | Placement | Interviews
* Arsh Goyal : Youtube
* AI Jobs | Artificial Intelligence

---

## 📊 Future Enhancements

* Job categorization (Internship / Full-Time / Hackathon)
* Deadline tracking
* Company-wise search
* Resume matching
* Placement analytics dashboard
* Web application (placemate.app)
* AI-powered job recommendations

---

## 👨‍💻 Author

**Varsha Rajanala**

Built to simplify placement preparation and opportunity tracking for students.

---

## 📄 License

This project is open-source and available under the MIT License.

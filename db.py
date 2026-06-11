import sqlite3

conn = sqlite3.connect("jobs.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")
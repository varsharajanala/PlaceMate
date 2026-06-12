import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(jobs)")

for row in cursor.fetchall():
    print(row)

conn.close()

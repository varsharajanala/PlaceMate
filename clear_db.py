import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM jobs")

conn.commit()
conn.close()

print("Database Cleared")
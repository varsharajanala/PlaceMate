
import sqlite3

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

print(f"✅ Deleted {deleted} old jobs")

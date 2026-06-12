import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM jobs
WHERE id NOT IN (
    SELECT MIN(id)
    FROM jobs
    GROUP BY title
)
""")

conn.commit()

print("✅ Duplicates Removed")

conn.close()
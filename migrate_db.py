
import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE jobs
    ADD COLUMN created_at TEXT
    """)

    print("✅ created_at column added")

except Exception as e:
    print("Already exists:", e)

cursor.execute("""
UPDATE jobs
SET created_at = datetime('now')
WHERE created_at IS NULL
""")

conn.commit()
conn.close()

print("✅ Migration Complete")

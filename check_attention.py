import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, title, link
FROM jobs
ORDER BY id DESC
LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:
    print("\n-------------------")
    print("ID:", row[0])
    print("TITLE:", row[1])
    print("LINK:", row[2])

conn.close()

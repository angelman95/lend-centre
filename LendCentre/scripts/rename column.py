import sqlite3


db_path = "instance/database.db"

# connect to db
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
ALTER TABLE inventory RENAME COLUMN "Left/right handed" TO Handedness;
               ''')

conn.commit()
conn.close()

print("Success!")
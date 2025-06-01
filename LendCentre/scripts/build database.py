import sqlite3
import csv

db_path = "instance/database.db"
csv_path = "inventory.csv"

# connect to db
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# make new inventory table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Barcode TEXT,
    Item TEXT,
    Type TEXT,
    Brand TEXT,
    Model TEXT,
    Colour TEXT,
    Connectivity TEXT,
    Strings INTEGER,
    "Left/right handed" TEXT
)
''')

# read an insert csv data
with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = [
        (
            row['Barcode'],
            row['Item'],
            row['Type'],
            row['Brand'],
            row['Model'],
            row['Colour'],
            row['Connectivity'],
            row['Strings'],
            row['Left/right handed']
        )
        for row in reader
    ]

    cursor.executemany('''
        INSERT INTO inventory (
            Barcode, Item, Type, Brand, Model, Colour, Connectivity, Strings, "Left/right handed"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', rows)


# make new students table
conn.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uniqueID TEXT NOT NULL,
    reg TEXT NOT NULL        
)
''')

conn.commit()
conn.close()

print("Tables created and csv imported!")
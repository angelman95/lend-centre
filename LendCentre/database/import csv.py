import sqlite3
import pandas as pd


## SCRIPT TO IMPORT CSV INVENTORY DATA AS AN SQL DATABASE ##

# load csv
csv_file = "A:\Projects\PycharmProjects\LendCentre\database\inventory.csv"
df = pd.read_csv(csv_file)

# connect to database
conn = sqlite3.connect('inventory.db')

# write dataframe to new table
df.to_sql('inventory.db', conn, if_exists='replace', index=False)

conn.close()

print("CSV data imported into the database successfully.")
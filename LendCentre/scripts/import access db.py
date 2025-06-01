import pyodbc
import sqlite3


## SCRIPT TO IMPORT ACCESS DATABASE ##


def convert_access_to_sqlite(access_db_path, sqlite_db_path):
    # Connect to Access DB
    access_conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={access_db_path};'
    )

    print("Connecting with:", access_conn_str)

    access_conn = pyodbc.connect(access_conn_str)
    access_cursor = access_conn.cursor()

    # Connect to SQLite DB
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()

    # Get list of tables
    tables = [
        row.table_name
        for row in access_cursor.tables(tableType='TABLE')
    ]

    for table in tables:
        print(f"Processing table: {table}")

        # Get column info
        access_cursor.execute(f"SELECT * FROM [{table}]")
        columns = [column[0] for column in access_cursor.description]

        # Create table in SQLite
        column_defs = ", ".join([f'"{col}" TEXT' for col in columns])
        create_stmt = f'CREATE TABLE "{table}" ({column_defs});'
        sqlite_cursor.execute(f'DROP TABLE IF EXISTS "{table}";')
        sqlite_cursor.execute(create_stmt)

        # Copy data row-by-row
        rows = access_cursor.fetchall()
        for row in rows:
            placeholders = ", ".join(["?"] * len(row))
            insert_stmt = f'INSERT INTO "{table}" VALUES ({placeholders});'
            sqlite_cursor.execute(insert_stmt, row)

        sqlite_conn.commit()

    # Cleanup
    access_cursor.close()
    access_conn.close()
    sqlite_conn.close()
    print(f"Conversion completed! SQLite DB saved at: {sqlite_db_path}")

# Example usage
if __name__ == "__main__":
    access_file = "A:\Projects\PycharmProjects\LendCentre\scripts\store-room-inventory.accdb"
    sqlite_file = "inventory.db"
    convert_access_to_sqlite(access_file, sqlite_file)

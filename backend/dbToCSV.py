import pandas as pd
import sqlite3
import os

def exportDatabaseToCsv(dbPath='movies.db', csvOutputPath='exported_movies.csv'):
    # 1. Verify the database exists
    if not os.path.exists(dbPath):
        print(f"Error: {dbPath} not found. Run initDatabase first.")
        return

    # 2. Connect and query
    dbConn = sqlite3.connect(dbPath)
    print(f"Reading data from {dbPath}...")
    # 'SELECT *' grabs all fields, including blanks which become empty cells
    exportedData = pd.read_sql('SELECT * FROM movies', dbConn)
    
    # 3. Save to CSV
    # index=False ensures we don't add an extra 'row number' column
    exportedData.to_csv(csvOutputPath, index=False)
    
    dbConn.close()
    print(f"Success! Database exported to: {os.path.abspath(csvOutputPath)}")

if __name__ == "__main__":
    exportDatabaseToCsv()
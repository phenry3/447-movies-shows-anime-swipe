import pandas as pd
import sqlite3
import os

def initDatabase(csvPath='final_recommender_dataset.csv', dbPath='movies.db'):
    if not os.path.exists(csvPath):
        print(f"Error: {csvPath} not found.")
        return

    # 1. Loading CSV
    print(f"Reading {csvPath}...")
    # We use low_memory=False to avoid DtypeWarnings with large datasets
    df = pd.read_csv(csvPath)

    # 2. Connect to SQLite
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    # 3. Handle the Primary Key
    # Since you want 'title' as the Primary Key, we ensure no duplicates exist in the dataframe first
    initial_count = len(df)
    df = df.drop_duplicates(subset=['title'])
    if len(df) < initial_count:
        print(f"Removed {initial_count - len(df)} duplicate titles to maintain Primary Key integrity.")

    # 4. Build the DB
    print(f"Building {len(df)} rows into the 'movies' table...")
    
    try:
        # Use 'title' as the index so pandas treats it as the primary identifier
        df.set_index('title', inplace=True)
        
        # if_exists='replace' will drop the table and recreate it
        df.to_sql('movies', conn, if_exists='replace', index=True, index_label='title')
        
        # Optional: Verify the schema by adding a UNIQUE constraint/index manually if needed, 
        # but to_sql with index=True usually handles the basics.
        
        conn.commit()
        print(f"Success. Database created at: {os.path.abspath(dbPath)}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initDatabase()
import pandas as pd
import sqlite3
import os

def export_to_algo_csv(dbPath='movies.db', outputPath='csv_for_algo.csv'):
    # Check if the database actually exists
    if not os.path.exists(dbPath):
        print(f"Error: Database '{dbPath}' not found. Did you run the import script first?")
        return

    print(f"Connecting to {dbPath}...")
    conn = sqlite3.connect(dbPath)

    try:
        # Load the 'movies' table into a DataFrame
        # This will include 'title' as a column since it was the index
        df = pd.read_sql_query("SELECT * FROM movies", conn)
        
        # Export to the requested filename
        df.to_csv(outputPath, index=False)
        print(f"Success! Data exported to: {outputPath}")
        print(f"Total rows exported: {len(df)}")
        
    except Exception as e:
        print(f"An error occurred during export: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # If running from the root, we point to the backend folder
    # If you 'cd backend' first, you can just use 'movies.db'
    export_to_algo_csv()
import pandas as pd
import sqlite3
import os

def export_to_algo_csv(dbPath='movies.db', outputPath='csv_for_algo.csv'):
    if not os.path.exists(dbPath):
        print(f"Error: Database '{dbPath}' not found.")
        return

    conn = sqlite3.connect(dbPath)

    # Pull ONLY the 5 specific columns needed
    query = """
    SELECT 
        title,
        production_companies, 
        genres, 
        production_countries, 
        original_language, 
        keywords 
    FROM movies
    """
    
    df = pd.read_sql_query(query, conn)
    
    # Export to CSV. 
    # Note: index=False prevents pandas from adding an extra unnamed numerical column. 
    df.to_csv(outputPath, index=False)
    
    print(f"Success! Data exported to: {outputPath}")
    conn.close()

if __name__ == "__main__":
    export_to_algo_csv()
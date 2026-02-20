import pandas as pd
import sqlite3
import os

def initDatabase(csvPath='tmdb_5000_movies.csv', dbPath='movies.db'):
    # loading csv
    print(f"reading {csvPath}")
    dataFile = pd.read_csv(csvPath)
    
    # connect or create
    conn = sqlite3.connect(dbPath)
    
    # use pandas object to build db from csv
    print(f"building {len(dataFile)} rows into the 'movies' table")
    dataFile.to_sql('movies', conn, if_exists='replace', index=False)

    conn.close()
    print(f"success. Database created at: {os.path.abspath(dbPath)}")

if __name__ == "__main__":
    initDatabase()
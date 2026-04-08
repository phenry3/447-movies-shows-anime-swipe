import sqlite3
import pandas as pd
from final_csv_to_db import initDatabase
from final_db_to_csv import export_to_algo_csv
from rec_algo import MovieRecommender

class MovieBackend:
    def __init__(self, db_path='movies.db'):
        self.db_path = db_path
        self._create_tables()
        self.recommender = MovieRecommender() 

    def _create_tables(self):
        conn = sqlite3.connect(self.db_path)
              
        # Create users
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                google_id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                email_verified BOOLEAN,
                name TEXT,
                picture TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


        """Creates matches and dislikes tables with the same structure as movies with google_id as link to user."""
        conn.execute("CREATE TABLE IF NOT EXISTS matches AS SELECT * FROM movies WHERE 1=0")
        conn.execute("CREATE TABLE IF NOT EXISTS dislikes AS SELECT * FROM movies WHERE 1=0")

        try:
            conn.execute("ALTER TABLE matches ADD COLUMN google_id TEXT REFERENCES users(google_id)")
            conn.execute("ALTER TABLE dislikes ADD COLUMN google_id TEXT REFERENCES users(google_id)")
        except:
            pass  # columns already exist

        conn.commit()
        conn.close()

    # --- Run your existing scripts ---
    def run_import(self):
        """Triggers final_csv_to_db.py logic."""
        initDatabase()

    def run_export(self):
        """Triggers final_db_to_csv.py logic."""
        export_to_algo_csv()

    # --- Matches Logic ---
    def add_match(self, title):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO matches SELECT * FROM movies WHERE title = ?", (title,))
        conn.commit()
        conn.close()

    def remove_match(self, title):
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM matches WHERE title = ?", (title,))
        conn.commit()
        conn.close()

    def get_matches(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM matches", conn)
        conn.close()
        return df.to_dict(orient='records')
    
    def get_match_titles(self):
        return [m['title'] for m in self.get_matches() if m.get('title')]
        

    # --- Dislike Logic ---
    def add_dislike(self, title):
        """Moves movie from 'movies' to 'dislikes' table."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO dislikes SELECT * FROM movies WHERE title = ?", (title,))
        conn.commit()
        conn.close()

    def remove_dislike(self, title):
        """Removes movie from 'dislikes' table."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM dislikes WHERE title = ?", (title,))
        conn.commit()
        conn.close()

    def get_dislikes(self):
        """Returns all disliked movies as a list of dictionaries."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM dislikes", conn)
        conn.close()
        return df.to_dict(orient='records')
    
    def get_dislike_titles(self):
        return [d['title'] for d in self.get_dislikes() if d.get('title')]
    
    # --- Algo Logic ---
    def get_rec(self):
        return self.recommender.serving_rec(self.get_match_titles(), self.get_dislike_titles())

if __name__ == "__main__":
    app = MovieBackend()
    
    # Example usage:
    # app.add_match("Toy Story")
    # app.add_dislike("Jumanji")
    # print("Matches:", app.get_matches())
    # print("Dislikes:", app.get_dislikes())

    
    print(app.get_dislike_titles())
    print(app.get_match_titles())
    
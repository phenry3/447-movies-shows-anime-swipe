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
    
    # --- User Logic ---
    def create_user(self, google_id, email, email_verified, name, picture):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("INSERT OR IGNORE INTO users (google_id, email, email_verified, name, picture) VALUES (?, ?, ?, ?, ?)",
                            (google_id, email, email_verified, name, picture))
        conn.commit()
        conn.close()
        return "created" if cursor.rowcount else "already exists"

    def delete_user(self, google_id):
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM matches WHERE google_id = ?", (google_id,))
        conn.execute("DELETE FROM dislikes WHERE google_id = ?", (google_id,))
        conn.execute("DELETE FROM users WHERE google_id = ?", (google_id,))
        conn.commit()
        conn.close()

    def get_user_profile_info(self, google_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM users WHERE google_id = ?", (google_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    # --- Matches Logic ---
    def add_match(self, title, google_id):
        # 1. check if google_id exists
        # 2. add based on user_id

        conn = sqlite3.connect(self.db_path)
        user = conn.execute("SELECT 1 FROM users WHERE google_id = ?", (google_id,)).fetchone()
        if not user:
            conn.close()
            return "Error: google_id not found"
        
        # makes sure doesnt exist
        conn.execute("INSERT INTO matches SELECT *, ? FROM movies WHERE title = ? AND NOT EXISTS (SELECT 1 FROM matches WHERE title = ? AND google_id = ?)", 
             (google_id, title, title, google_id))
        
        conn.commit()
        conn.close()

        return "success"

    def remove_match(self, title, google_id):
        # 1. check if google_id exists
        # 2. remove based on user_id match
        conn = sqlite3.connect(self.db_path)
        user = conn.execute("SELECT 1 FROM users WHERE google_id = ?", (google_id,)).fetchone()
        if not user:
            conn.close()
            return "Error: google_id not found"
        
        conn.execute("DELETE FROM matches WHERE title = ? AND google_id = ?", (title, google_id))
        conn.commit()
        conn.close()

    def get_matches(self, google_id):
        # 1. check if google_id exists
        # 2. serve based on user_id match    
        conn = sqlite3.connect(self.db_path)
        user = conn.execute("SELECT 1 FROM users WHERE google_id = ?", (google_id,)).fetchone()
        if not user:
            conn.close()
            return "Error: google_id not found"
        df = pd.read_sql_query("SELECT * FROM matches WHERE google_id = ?", conn, params=(google_id,))
        conn.close()
        return df.to_dict(orient='records')
    
    # [TESTING]
    def get_match_titles(self, google_id):
        return [m['title'] for m in self.get_matches(google_id) if m.get('title')]
        

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
    
    # --- Dev Funcs ---
    def print_schemas(self):
        conn = sqlite3.connect(self.db_path)
        for table in ['users', 'movies', 'matches', 'dislikes']:
            print(f"\n--- {table} ---")
            for row in conn.execute(f"PRAGMA table_info({table})"):
                print(f"  {row[1]} ({row[2]})")
        conn.close()

    def print_all_db_info(self):
        conn = sqlite3.connect(self.db_path)
        for table in ['users', 'movies', 'matches', 'dislikes']:
            print(f"\n--- {table} ---")
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            print(df)
        conn.close()

if __name__ == "__main__":
    app = MovieBackend()
    
    # Example usage:
    # app.add_match("Toy Story")
    # app.add_dislike("Jumanji")
    # print("Matches:", app.get_matches())
    # print("Dislikes:", app.get_dislikes())

    
    #print(app.get_dislike_titles())
    #print(app.get_match_titles())

    
    app.create_user("1234567890", "test@gmail.com", True, "John Doe", "https://photo.url")
    print(app.get_user_profile_info("1234567890"))

    app.delete_user("1234567890")
    app.print_all_db_info()
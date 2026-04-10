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
    
    def get_match_titles(self, google_id):
        return [m['title'] for m in self.get_matches(google_id) if m.get('title')]
        
    # --- Dislike Logic ---    
    def add_dislike(self, title, google_id):
        conn = sqlite3.connect(self.db_path)
        user = conn.execute("SELECT 1 FROM users WHERE google_id = ?", (google_id,)).fetchone()
        if not user:
            conn.close()
            return "Error: google_id not found"
        conn.execute("INSERT INTO dislikes SELECT *, ? FROM movies WHERE title = ? AND NOT EXISTS (SELECT 1 FROM dislikes WHERE title = ? AND google_id = ?)",
                    (google_id, title, title, google_id))
        conn.commit()
        conn.close()

    def remove_dislike(self, title, google_id):
        conn = sqlite3.connect(self.db_path)
        user = conn.execute("SELECT 1 FROM users WHERE google_id = ?", (google_id,)).fetchone()
        if not user:
            conn.close()
            return "Error: google_id not found"
        conn.execute("DELETE FROM dislikes WHERE title = ? AND google_id = ?", (title, google_id))
        conn.commit()
        conn.close()

    def get_dislikes(self, google_id):
        conn = sqlite3.connect(self.db_path)
        user = conn.execute("SELECT 1 FROM users WHERE google_id = ?", (google_id,)).fetchone()
        if not user:
            conn.close()
            return "Error: google_id not found"
        df = pd.read_sql_query("SELECT * FROM dislikes WHERE google_id = ?", conn, params=(google_id,))
        conn.close()
        return df.to_dict(orient='records')

    def get_dislike_titles(self, google_id):
        return [d['title'] for d in self.get_dislikes(google_id) if d.get('title')]
    
    # --- Algo Logic ---
    def get_rec(self, google_id):
        return self.recommender.serving_rec(self.get_match_titles(google_id), self.get_dislike_titles(google_id))
    
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

    def get_stats(self):
        """Returns the total counts for matches and dislikes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM matches")
        liked_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM dislikes")
        disliked_count = cursor.fetchone()[0]
        
        conn.close()
        return {"liked": liked_count, "disliked": disliked_count}

    def get_genre_stats(self):
        """Aggregates genre counts from liked content for the pie chart."""
        conn = sqlite3.connect(self.db_path)
        # We use pandas here because it handles the row-looping efficiently
        df = pd.read_sql_query("SELECT genres FROM matches", conn)
        conn.close()

        genre_counts = {}
        for row in df['genres'].dropna():
            # Split "Action, Adventure" into ["Action", "Adventure"]
            parts = [g.strip() for g in str(row).split(',') if g.strip()]
            for genre in parts:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        # Returns: {"Animation": 5, "Comedy": 3, ...}
        return genre_counts

if __name__ == "__main__":
    app = MovieBackend()
    
    # Example usage:
    # app.add_match("Toy Story")
    # app.add_dislike("Jumanji")
    # print("Matches:", app.get_matches())
    # print("Dislikes:", app.get_dislikes())

    
    #print(app.get_dislike_titles())
    #print(app.get_match_titles())

    print("-- create user -- ")
    app.create_user("1234567890", "test@gmail.com", True, "John Doe", "https://photo.url")
    print(app.get_user_profile_info("1234567890"))
    print()

    print("-- add match -- ")
    app.add_match("Toy Story", "1234567890")
    app.add_match("Jumanji", "1234567890")
    print(app.get_match_titles("1234567890"))
    print()

    print("-- add dislike -- ")
    app.add_dislike("Grumpier Old Men", "1234567890")
    print(app.get_dislike_titles("1234567890"))
    print()

    print("-- get rec -- ")
    print(app.get_rec("1234567890"))
    print()

    app.print_schemas()
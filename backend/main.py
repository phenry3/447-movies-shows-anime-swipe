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
        """Creates matches and dislikes tables with the same structure as movies."""
        conn = sqlite3.connect(self.db_path)
        # Create Matches table
        conn.execute("CREATE TABLE IF NOT EXISTS matches AS SELECT * FROM movies WHERE 1=0")
        # Create Dislikes table
        conn.execute("CREATE TABLE IF NOT EXISTS dislikes AS SELECT * FROM movies WHERE 1=0")
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
        """
            this needs to be modifiable by the front end via API call
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO matches SELECT * FROM movies WHERE title = ?", (title,))
        conn.commit()
        conn.close()

    def remove_match(self, title):
        """
            this needs to be modifiable by the front end via API call
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM matches WHERE title = ?", (title,))
        conn.commit()
        conn.close()

    def get_matches(self):
        """
            this needs to be modifiable by the front end via API call
        """
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM matches", conn)
        conn.close()
        return df.to_dict(orient='records')
    
    def get_match_titles(self):
        """
            this needs to be modifiable by the front end via API call
        """
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
    """
        this needs to be an API call!!!
        We need to add a put to modify the like in the database
    """
    def get_rec(self):
        return self.recommender.serving_rec(self.get_match_titles(), self.get_dislike_titles())

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

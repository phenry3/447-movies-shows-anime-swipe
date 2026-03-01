Backend setup steps so far, This assumes you have python3 already installed. Do this from the backend root

1. Create a virtual environment on your dev machine 
    - python3 -m (name_of_venv) venv #where name_of_venv is of your choosing
2. Activate your venv while sitting in the backend root
    - source name_of_venv/bin/activate

# If that worked your shell will gove from line 9 to line 10
castr@char:~/repos/447-movies-shows-anime-swipe/backend$ source 447app/bin/activate
(447app) castr@char:~/repos/447-movies-shows-anime-swipe/backend$ 

# Dependincies to install (run this once)
pip install -r requirements.txt

# DB stuff
you must have final_recommender_dataset.csv in your local backend folder
run the final_csv_to_db.py to turn it into a db if you have not build the db yet
run final_db_to_csv.py if you want to turn the db into a csv for using for the algo

# Algo stuff
currently in demo state
algo class can take in either title with get_recommendations_from_title or index of csv through get_recommendations_from_idx
csv_for_algo.csv must be in the backend directory to work

# Algo stuff
NOTE:
csv_for_algo.csv must be in the backend directory to work

ONLY entry point: serving_rec(liked_array)
- input: liked_array = list of liked movie titles (strings)
- output: one recommended movie title (string)

new media probability (else rec based on liked list):
- liked < 10: 50% new / 50% liked-based
- 10 <= liked < 20: 30% new / 70% liked-based
- liked >= 20: 15% new / 85% liked-based

when generating a rec (either from new media seed or a random liked title):
- computes cosine similarity on one-hot features (companies/genres/countries/language/keywords)
- takes top 10 most similar movies (excluding itself)
- returns ONE title chosen with weights [10,9,8,7,6,5,4,3,2,1]
  (rank1=18.18%, rank2=16.36%, rank3=14.55%, rank4=12.73%, rank5=10.91%,
   rank6=9.09%, rank7=7.27%, rank8=5.45%, rank9=3.64%, rank10=1.82%)

# Main Backend Logic (main.py)
This is the controller for the whole backend. It handles the 'matches' and 'dislikes' tables which have the same schema as the main movies table. 

Functions in MovieBackend class:
* **run_import()**: triggers the final_csv_to_db script
* **run_export()**: triggers the final_db_to_csv script
* **add_match(title) / add_dislike(title)**: pulls the movie from the main table and tosses it into the liked or disliked list
* **remove_match(title) / remove_dislike(title)**: deletes a movie from those lists if you change your mind
* **get_matches() / get_dislikes()**: returns everything in those tables as a list of dicts for the frontend to use
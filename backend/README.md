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

# Algo frontend info
the algo is integrated into the backend class stored in main.py
just call app.get_rec() to get a recommendation
this works if no content is in the liked list so always just call app.get_rec() for recs in ALL cases

example loop is just call algo function to get first piece of content -> user likes/dislikes -> call like/dislike backend functions -> call algo function to get next piece of content

example of algo use:
while True:
        user_input = ''
        rec = app.get_rec()

        while user_input != 'y' and user_input != 'n':
            user_input = input(f"Do you like this content? (y/n):\n{rec}\nEnter input: ")
            print()
        if user_input == 'y':
            app.add_match(rec)
        elif user_input == 'n':
            app.add_dislike(rec)

# Algo backend info
NOTE:
csv_for_algo.csv must be in the backend directory to work

ONLY entry point: serving_rec(liked_array)
- input: liked_array = list of liked movie titles (strings)
- output: one recommended movie title (string)

new media probability (else rec based on liked list):
NOTE: if a recomendation is going to be made that is already in the watchlist, new content is served instead
- liked == 0: 100% new / 0% liked-based (serve random/new content)
- 0 < liked < 8: 15% new / 85% liked-based
- 8 <= liked < 15: 10% new / 90% liked-based
- liked >= 15: 2% new / 98% liked-based

when generating a rec (either from new media seed or a random liked title):
- computes cosine similarity on one-hot features (companies/genres/countries/language/keywords)
- takes top pool_size most similar movies (excluding itself)
- returns ONE title chosen with weights per index created by a decay function in order
- runs retry logic if a collision is found on liked list or disliked list

# Main Backend Logic (main.py)
This is the controller for the whole backend. It handles the 'matches' and 'dislikes' tables which have the same schema as the main movies table. 

Functions in MovieBackend class:
* **run_import()**: triggers the final_csv_to_db script
* **run_export()**: triggers the final_db_to_csv script
* **add_match(title) / add_dislike(title)**: pulls the movie from the main table and tosses it into the liked or disliked list
* **remove_match(title) / remove_dislike(title)**: deletes a movie from those lists if you change your mind
* **get_matches() / get_dislikes()**: returns everything in those tables as a list of dicts for the frontend to use
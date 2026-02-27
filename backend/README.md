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
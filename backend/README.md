Back ene setup steps so far, This assumes you have python3 already installed. Do this from the backend root

1. Create a virtual environment on your dev machine 
    - python3 -m (name_of_venv) venv #where name_of_venv is of your choosing
2. Activate your venv while sitting in the backend root
    - source name_of_venv/bin/activate

# If that worked your shell will gove from line 9 to line 10
castr@char:~/repos/447-movies-shows-anime-swipe/backend$ source 447app/bin/activate
(447app) castr@char:~/repos/447-movies-shows-anime-swipe/backend$ 

# Dependincies to install (run this once)
pip install "fastapi[standard]"
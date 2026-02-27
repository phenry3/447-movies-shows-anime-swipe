import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self):
        # setting initial movie/feature tables
        self.movies = pd.read_csv("csv_for_algo.csv", low_memory=False)
        self.features = self.movies[['production_companies','genres', 'production_countries', 'original_language', 'keywords']].fillna('').astype(str).copy()

        # making everything one hot using count vectorizier + turning all nums not 0 to 1 and all 0s to 0
        # making it so each movie has a long string instead of individual cols
        df = self.features[['production_companies','genres', 'production_countries', 'original_language', 'keywords']].apply(lambda x: ' '.join(x), axis=1)

        cv = CountVectorizer(binary=True)
        self.movie_matrix = cv.fit_transform(df) # this is the final movie matrix

    # takes all companies from the company json and converts them to
    # a comma seperated string
    def company_parser(self, json_input):
        comma_sep_company_string = ""
        companies_arr = []
        
        json_list = ast.literal_eval(json_input)
            
        for dicts in json_list:
            companies_arr.append(dicts['name'])

        comma_sep_company_string = " ".join(companies_arr)
            
        return comma_sep_company_string
    
    # serving top 5 recommendations
    def get_recommendations_from_idx(self, index):
        scores = cosine_similarity(self.movie_matrix[index:index+1], self.movie_matrix)[0]
        sorted_indices = np.argsort(scores)
        top_5_indices = sorted_indices[-6:-1]
        
        recommended_titles = self.movies['title'].iloc[top_5_indices].tolist()

        return recommended_titles[::-1]
    
    def get_recommendations_from_name(self, title):
        if title not in self.movies['title'].values:
            return f"Error: '{title}' not found in the database."
        
        row_idx = np.where(self.movies['title'] == title)[0][0]
        scores = cosine_similarity(self.movie_matrix[row_idx : row_idx + 1], self.movie_matrix)[0]
        sorted_indices = np.argsort(scores)
        top_5_indices = sorted_indices[-6:-1]
        
        recommended_titles = self.movies['title'].iloc[top_5_indices].tolist()

        return recommended_titles[::-1]

movie_rec = MovieRecommender()

# DEMO: gets a few recommendations from index
for i in range(5):
    print(f"Recommendation for movie: {movie_rec.movies['title'].iloc[i]}:")
    print(f"{movie_rec.get_recommendations_from_idx(i)}\n")


# demo seperator
print("---------------------------------------------------\n")

# DEMO: gets recommendation based on title
title = "Toy Story"
print(f"Recommendation for movie: {title}:")
print(f"{movie_rec.get_recommendations_from_name(title)}\n")
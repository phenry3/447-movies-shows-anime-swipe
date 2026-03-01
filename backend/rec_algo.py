import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

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
    
    # serving a recommendation from index
    # chooses a random rec index with weight favoring in order -> index 0 is 10x more likely that index 10
    def get_recommendations_from_idx(self, index):
        scores = cosine_similarity(self.movie_matrix[index:index+1], self.movie_matrix)[0]
        sorted_indices = np.argsort(scores)
        top_5_indices = sorted_indices[-11:-1] # constructing list of top 10 most similar movies in order of similarity
        
        recommended_titles = self.movies['title'].iloc[top_5_indices].tolist()
        rec_idx = random.choices(range(10), weights=[10,9,8,7,6,5,4,3,2,1], k=1)[0] # chooses a random rec index

        return recommended_titles[::-1][rec_idx]
    
    # serving a recommendation from title
    # takes top 10 recs based on the title and gives an inverse log chance of returning content by order
    # chooses a random rec index with weight favoring in order -> index 0 is 10x more likely that index 10
    def get_recommendations_from_title(self, title):
        if title not in self.movies['title'].values:
            return f"Error: '{title}' not found in the database."
        
        row_idx = np.where(self.movies['title'] == title)[0][0]
        scores = cosine_similarity(self.movie_matrix[row_idx : row_idx + 1], self.movie_matrix)[0]
        sorted_indices = np.argsort(scores)
        top_5_indices = sorted_indices[-11:-1] # constructing list of top 10 most similar movies in order of similarity
        
        recommended_titles = self.movies['title'].iloc[top_5_indices].tolist()
        rec_idx = random.choices(range(10), weights=[10,9,8,7,6,5,4,3,2,1], k=1)[0] # chooses a random rec index

        return recommended_titles[::-1][rec_idx]
    
    # serving recommendation based on an array of liked content
    # if nothing in list (liked_size == 0), serve new/random content
    # 0 < liked < 8: 35% chance new content, 65% chance liked-based rec
    # 8 <= liked < 15: 20% chance new content, 80% chance liked-based rec
    # liked >= 15: 10% chance new content, 90% chance liked-based rec
    def serving_rec(self, liked_array, dislike_array):
        liked_size = len(liked_array)
        new_media_roll = random.randrange(100) + 1
        new_media = False
        liked_content_retry = 10
        max_new_content_retry = 10
        rec = ""

        # controls if new media is served based on spec
        if liked_size == 0:
            new_media = True
        elif liked_size < 8 and new_media_roll <= 35: # liked content < 4
            new_media = True
        elif liked_size < 15 and new_media_roll <= 20: # liked content < 8
            new_media = True
        elif liked_size >= 15 and new_media_roll <= 10: # liked content >= 8
            new_media = True
        
        # serving recommendation based on watchlist
        if new_media == False:
            eligible_content = False

            # looping for max 10 tries attempting to find content that can be recommended
            for attempts in range(liked_content_retry):
                i = random.randrange(liked_size)
                random_title = liked_array[i]
                rec = self.get_recommendations_from_title(random_title)

                # handling case where rec is in watchlist or dislike to prevent duplicate serving
                if rec not in liked_array and not rec in dislike_array:
                    eligible_content = True
                    break
                        
            # worst case just recommend random new content
            if eligible_content == False:
                new_media = True # serving random content -> unlikely new media will be dup anyways
            
        # serving new media
        # NOTE: no need to have a case for no eligible content as last piece of content will be served
        if new_media == True:
            eligible_content = False

            # looping for max 10 tries attempting to find content that can be recommended
            for attempts in range(max_new_content_retry):
                num_indexes = self.movie_matrix.shape[0]
                i = random.randrange(num_indexes)
                rec = self.get_recommendations_from_idx(i)

                # handling case where rec is in watchlist or dislike to prevent duplicate serving
                if rec not in liked_array and not rec in dislike_array:
                    eligible_content = True
                    break

        return rec

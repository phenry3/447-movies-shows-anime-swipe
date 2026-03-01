import pandas as pd
import numpy as np
import ast
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import hstack
import random

class MovieRecommender:
    def __init__(self):
        # setting initial movie/feature tables
        self.movies = pd.read_csv("csv_for_algo.csv", low_memory=False)
        self.features = self.movies[['production_companies','genres', 'production_countries', 'original_language', 'keywords']].fillna('').astype(str).copy()

        # making a vectorizer for each attribute
        count_genre = CountVectorizer(stop_words='english')
        count_language = CountVectorizer()
        count_country = CountVectorizer()
        tfidf_keyword = TfidfVectorizer(stop_words='english')
        tfidf_company = TfidfVectorizer(stop_words='english')

        # breaking each feature into its own matrix
        genre_matrix = count_genre.fit_transform(self.features['genres'])
        keyword_matrix = tfidf_keyword.fit_transform(self.features['keywords'])
        language_matrix = count_language.fit_transform(self.features['original_language'])
        country_matrix = count_country.fit_transform(self.features['production_countries'])
        company_matrix = tfidf_company.fit_transform(self.features['production_companies'])

        # making the weights for how much each attribute matrix matters
        weight_genre = 0.6
        weight_keyword = 0.4
        weight_language = 0.4 
        weight_country = 0.2
        weight_company = 0.1

        # multiplying each matrix by its specific weight
        weighted_genre = genre_matrix * weight_genre
        weighted_keyword = keyword_matrix * weight_keyword
        weighted_language = language_matrix * weight_language
        weighted_country = country_matrix * weight_country
        weighted_company = company_matrix * weight_company

        # creating the final movie matrix as a combination of the weighted attribute matrixs
        self.movie_matrix = hstack([weighted_genre, weighted_keyword, weighted_language, weighted_country, weighted_company])

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
    # chooses a random rec index with weight favoring in order
    def get_recommendations_from_idx(self, index):
        pool_size = 50
        
        scores = cosine_similarity(self.movie_matrix[index:index+1], self.movie_matrix)[0]
        sorted_indices = np.argsort(scores)
        top_50_indices = sorted_indices[-pool_size:-1] # constructing list pool_size most similar movies in order of similarity
        
        recommended_titles = self.movies['title'].iloc[top_50_indices].tolist()[::-1]

        dynamic_weights = [1.0 / ((i + 1) ** 0.5) for i in range(len(recommended_titles))]
        rec_title = random.choices(recommended_titles, weights=dynamic_weights, k=1)[0] # chooses a random rec index

        return rec_title
    
    # serving a recommendation from title
    # takes top 10 recs based on the title and gives an inverse log chance of returning content by order
    # chooses a random rec index with weight favoring in order -> index 0 is 10x more likely that index 10
    def get_recommendations_from_title(self, title):
        if title not in self.movies['title'].values:
            return f"Error: '{title}' not found in the database."
        pool_size = 50
        
        row_idx = np.where(self.movies['title'] == title)[0][0]
        scores = cosine_similarity(self.movie_matrix[row_idx : row_idx + 1], self.movie_matrix)[0]
        sorted_indices = np.argsort(scores)
        top_50_indices = sorted_indices[-pool_size:-1] # constructing list of pool_size most similar movies in order of similarity
        
        recommended_titles = self.movies['title'].iloc[top_50_indices].tolist()[::-1]
        
        dynamic_weights = [1.0 / ((i + 1) ** 0.5) for i in range(len(recommended_titles))]
        rec_title = random.choices(recommended_titles, weights=dynamic_weights, k=1)[0] # chooses a random rec index

        return rec_title
    
    # serving recommendation based on an array of liked content
    # GOAL -> recommend based on taste asap
    # if nothing in list (liked_size == 0), serve new/random content
    # 0 < liked < 8: 15% chance new content, 85% chance liked-based rec
    # 8 <= liked < 15: 10% chance new content, 90% chance liked-based rec
    # liked >= 15: 2% chance new content, 98% chance liked-based rec
    def serving_rec(self, liked_array, dislike_array):
        liked_size = len(liked_array)
        new_media_roll = random.randrange(100) + 1
        new_media = False
        liked_content_retry = 5
        max_new_content_retry = 5
        rec = ""

        # controls if new media is served based on spec
        if liked_size == 0:
            new_media = True
        elif liked_size < 8 and new_media_roll <= 15: # liked content < 8
            new_media = True
        elif liked_size < 15 and new_media_roll <= 10: # liked content < 15
            new_media = True
        elif liked_size >= 15 and new_media_roll <= 2: # liked content >= 15
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
            num_indexes = self.movie_matrix.shape[0]

            # looping for max 10 tries attempting to find content that can be recommended
            for attempts in range(max_new_content_retry):
                i = random.randrange(num_indexes)
                rec = self.get_recommendations_from_idx(i)

                # handling case where rec is in watchlist or dislike to prevent duplicate serving
                if rec not in liked_array and not rec in dislike_array:
                    eligible_content = True
                    break

        return rec

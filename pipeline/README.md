Data pipeline for merging movies, tv, and anime datasets.


# Data Pipeline

This script merges and cleans movie, TV, and anime datasets into a unified format for use in the recommendation system.

## Overview

The pipeline:

- Cleans and standardizes movie data (TMDB)
- Cleans and standardizes TV data (TMDB)
- Cleans and standardizes anime data
- Aligns all datasets to a common schema
- Generates a unique `uid` per record
- Exports a single unified CSV file for backend processing

## Expected Input Files

The following CSV files must be available locally before running the script:

- `movies_metadata.csv`
- `keywords.csv`
- `TMDB_tv_dataset_v3.csv`
- `AnimeList.csv`

Place these files in the same directory where the script is executed.

Raw datasets are not included in this repository.

## Output

The script generates:
- `data/processed/final_recommender_dataset.csv`
The output dataset contains the following fields:
- `id`
- `title`
- `description`
- `genres`
- `keywords`
- `production_companies`
- `production_countries`
- `original_language`
- `thumbnail_url`
- `content_type`
- `uid`


## Data Sources

The datasets used in this pipeline were obtained from public Kaggle datasets:

- TMDB Movies Metadata (includes `movies_metadata.csv` and `keywords.csv`)
- TMDB TV Dataset (`TMDB_tv_dataset_v3.csv`)
- MyAnimeList Dataset (`AnimeList.csv`)

import pandas as pd
import os
import ast


# -----------------------------
# Helpers
# -----------------------------
def safe_list_of_dicts(text):
    if pd.isna(text):
        return []
    if isinstance(text, list):
        return text
    if not isinstance(text, str):
        return []
    t = text.strip()
    if t == "" or t.lower() == "nan":
        return []
    try:
        val = ast.literal_eval(t)
        return val if isinstance(val, list) else []
    except Exception:
        return []


def extract_names(text):
    items = safe_list_of_dicts(text)
    names = []
    for x in items:
        if isinstance(x, dict) and x.get("name"):
            names.append(str(x["name"]))
    return ", ".join(names)


def clean_str_col(series_like):
    if series_like is None:
        return pd.Series([], dtype=str)
    return series_like.fillna("").astype(str).str.strip()


def must_exist(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    return path


# -----------------------------
# Main
# -----------------------------
def main():
    # Expect the input CSVs to be in the same folder where this script is run.
    movies_path = must_exist("movies_metadata.csv")
    keywords_path = must_exist("keywords.csv")
    tv_path = must_exist("TMDB_tv_dataset_v3.csv")
    anime_path = must_exist("AnimeList.csv")

    movies = pd.read_csv(movies_path, low_memory=False)
    keywords = pd.read_csv(keywords_path)
    tv = pd.read_csv(tv_path)
    anime = pd.read_csv(anime_path)

    # =============================
    # 1) MOVIES 
    # =============================
    movies_clean = movies.copy()

    movies_clean["id"] = pd.to_numeric(movies_clean["id"], errors="coerce")
    movies_clean = movies_clean.dropna(subset=["id"]).copy()
    movies_clean["id"] = movies_clean["id"].astype(int)

    keywords_df = keywords.copy()
    keywords_df["id"] = pd.to_numeric(keywords_df["id"], errors="coerce")
    keywords_df = keywords_df.dropna(subset=["id"]).copy()
    keywords_df["id"] = keywords_df["id"].astype(int)

    if "keywords" in keywords_df.columns:
        movies_clean = movies_clean.merge(keywords_df[["id", "keywords"]], on="id", how="left")
    else:
        movies_clean["keywords"] = ""

    movies_clean["title"] = clean_str_col(movies_clean.get("title"))
    movies_clean["description"] = clean_str_col(movies_clean.get("overview"))
    movies_clean["genres"] = movies_clean.get("genres", "").apply(extract_names)
    movies_clean["keywords"] = movies_clean.get("keywords", "").apply(extract_names)
    movies_clean["production_companies"] = movies_clean.get("production_companies", "").apply(extract_names)
    movies_clean["production_countries"] = movies_clean.get("production_countries", "").apply(extract_names)
    movies_clean["original_language"] = clean_str_col(movies_clean.get("original_language"))
    movies_clean["thumbnail_url"] = clean_str_col(movies_clean.get("poster_path"))
    movies_clean["content_type"] = "movie"

    # =============================
    # 2) TV 
    # =============================
    tv_clean = tv.copy()

    if "id" not in tv_clean.columns:
        raise KeyError("TV dataset missing 'id' column.")

    tv_clean["id"] = pd.to_numeric(tv_clean["id"], errors="coerce")
    tv_clean = tv_clean.dropna(subset=["id"]).copy()
    tv_clean["id"] = tv_clean["id"].astype(int)

    if "name" in tv_clean.columns and "title" not in tv_clean.columns:
        tv_clean = tv_clean.rename(columns={"name": "title"})
    if "overview" in tv_clean.columns and "description" not in tv_clean.columns:
        tv_clean = tv_clean.rename(columns={"overview": "description"})
    if "poster_path" in tv_clean.columns and "thumbnail_url" not in tv_clean.columns:
        tv_clean = tv_clean.rename(columns={"poster_path": "thumbnail_url"})

    tv_clean["title"] = clean_str_col(tv_clean.get("title"))
    tv_clean["description"] = clean_str_col(tv_clean.get("description"))
    tv_clean["genres"] = clean_str_col(tv_clean.get("genres"))

    tv_clean["keywords"] = tv_clean["keywords"].apply(extract_names) if "keywords" in tv_clean.columns else ""
    tv_clean["production_companies"] = tv_clean["production_companies"].apply(extract_names) if "production_companies" in tv_clean.columns else ""
    tv_clean["production_countries"] = tv_clean["production_countries"].apply(extract_names) if "production_countries" in tv_clean.columns else ""

    tv_clean["original_language"] = clean_str_col(tv_clean.get("original_language"))
    tv_clean["thumbnail_url"] = clean_str_col(tv_clean.get("thumbnail_url"))
    tv_clean["content_type"] = "tv"

    # =============================
    # 3) ANIME 
    # =============================
    anime_clean = anime.copy()

    if "anime_id" not in anime_clean.columns:
        raise KeyError("Anime dataset missing 'anime_id' column.")

    anime_clean["id"] = pd.to_numeric(anime_clean["anime_id"], errors="coerce")
    anime_clean = anime_clean.dropna(subset=["id"]).copy()
    anime_clean["id"] = anime_clean["id"].astype(int)

    if "background" in anime_clean.columns:
        anime_clean["description"] = clean_str_col(anime_clean["background"])
    elif "synopsis" in anime_clean.columns:
        anime_clean["description"] = clean_str_col(anime_clean["synopsis"])
    else:
        anime_clean["description"] = ""

    anime_clean["title"] = clean_str_col(anime_clean.get("title"))

    if "genre" in anime_clean.columns:
        anime_clean["genres"] = clean_str_col(anime_clean["genre"])
    elif "genres" in anime_clean.columns:
        anime_clean["genres"] = clean_str_col(anime_clean["genres"])
    else:
        anime_clean["genres"] = ""

    anime_clean["keywords"] = clean_str_col(anime_clean["tags"]) if "tags" in anime_clean.columns else ""
    anime_clean["production_companies"] = ""
    anime_clean["production_countries"] = ""
    anime_clean["original_language"] = "ja"

    if "image_url" in anime_clean.columns:
        anime_clean["thumbnail_url"] = clean_str_col(anime_clean["image_url"])
    elif "thumbnail_url" in anime_clean.columns:
        anime_clean["thumbnail_url"] = clean_str_col(anime_clean["thumbnail_url"])
    else:
        anime_clean["thumbnail_url"] = ""

    anime_clean["content_type"] = "anime"

    # =============================
    # 4) Final columns
    # =============================
    final_cols = [
        "id",
        "title",
        "description",
        "genres",
        "keywords",
        "production_companies",
        "production_countries",
        "original_language",
        "thumbnail_url",
        "content_type",
    ]

    movies_clean = movies_clean[final_cols]
    tv_clean = tv_clean[final_cols]
    anime_clean = anime_clean[final_cols]

    # =============================
    # 5) Combine + final cleanup
    # =============================
    all_content = pd.concat([movies_clean, tv_clean, anime_clean], ignore_index=True)

    for c in all_content.columns:
        all_content[c] = all_content[c].fillna("").astype(str).str.strip()

    all_content = all_content[all_content["title"] != ""].reset_index(drop=True)

    all_content["uid"] = all_content["content_type"] + "_" + all_content["id"].astype(str)

    # =============================
    # 6) Save
    # =============================
    output_csv = os.path.join("data", "processed", "final_recommender_dataset.csv")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    all_content.to_csv(output_csv, index=False)

    print("FINAL DATASET SHAPE:", all_content.shape)
    print("Saved:", os.path.abspath(output_csv))


if __name__ == "__main__":
    main()




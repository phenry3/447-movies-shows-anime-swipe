from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal, Any
import sqlite3



from main import MovieBackend  # imports the class from backend/main.py

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
backend = MovieBackend(db_path="movies.db")

MediaType = Literal["movie", "tv", "anime"]


# ---------- Request/Response schemas ----------
class MediaItem(BaseModel):
    title: str
    overview: str = ""
    genres: List[str] = []
    thumbnail_url: str = ""
    media_type: MediaType
    release_date: str = ""     # not in DB right now
    vote_average: float = 0.0  # not in DB right now


class FeedbackIn(BaseModel):
    google_id: str
    title: str
    action: Literal["like", "dislike"]

class UserIn(BaseModel):
    google_id: str
    email: str
    email_verified: bool
    name: str = ""
    picture: str = ""


#--------Helpers---------

def parse_genres(genres_val:Any) -> List[str]:
    if not genres_val :
        return []
    
    parts = str(genres_val).split(",")
    cleaned = []

    for g in parts:
        g.strip()
        if g:
            cleaned.append(g)

    return cleaned


def fetch_movie_by_title(title: str) -> dict:
    
    #Look up the full row in movies table (because recommender returns only a title).
    
    conn = sqlite3.connect(backend.db_path)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            "SELECT * FROM movies WHERE title = ? LIMIT 1",
            (title,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Title not found in movies: {title}")
        return dict(row)
    finally:
        conn.close()


def to_api_shape(row: dict) -> MediaItem:
    """
    Maps DB columns -> frontend JSON keys.
    DB: description, genres, thumbnail, content_type
    API: overview, genres(list), thumbnail_url, media_type
    """
    title = row.get("title")
    if not title:
        raise HTTPException(status_code=500, detail="Row missing title")

    media_type = row.get("content_type") or "movie"
    if media_type not in ("movie", "tv", "anime"):
        media_type = "movie"

    return MediaItem(
        title=str(title),
        overview=str(row.get("description") or ""),
        genres=parse_genres(row.get("genres")),
        thumbnail_url=str(row.get("thumbnail_url") or ""),
        media_type=media_type,  # type: ignore
        release_date="",
        vote_average=0.0,
    )


def one_recommendation(google_id : str) -> MediaItem:
    rec_title = backend.get_rec(google_id)  # confirmed: returns a string title
    if not isinstance(rec_title, str) or not rec_title.strip():
        raise HTTPException(status_code=404, detail="No recommendation available")

    row = fetch_movie_by_title(rec_title)
    return to_api_shape(row)


# Endpoints

@api.post("/api/users")
def create_user(user: UserIn):
    result = backend.create_user(
        user.google_id,
        user.email,
        user.email_verified,
        user.name,
        user.picture,
    )
    return {"status": result}

@api.get("/api/rec/{google_id}", response_model=MediaItem)
def get_rec(google_id: str) :
    return one_recommendation(google_id)

@api.post("/api/feedback", response_model=MediaItem)
def feedback(payload: FeedbackIn):
    title = payload.title.strip()
    google_id = payload.google_id.strip()

    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    
    if not google_id:
        raise HTTPException(status_code=400, detail="google_id is required")

    
    if payload.action == "like":
       result = backend.add_match(title, google_id)
    else:
       result = backend.add_dislike(title, google_id)
    
    if isinstance(result, str) and result.startswith("Error"):
        raise HTTPException(status_code=400, detail=result)
    return one_recommendation(google_id)


# To be used by the matches page
@api.get("/api/matches/{google_id}", response_model=List[MediaItem])
def matches(google_id: str):
    rows = backend.get_matches(google_id)

    if isinstance(rows, str) and rows.startswith("Error"):
        raise HTTPException(status_code=400, detail=rows)
    
    return [to_api_shape(r) for r in rows]

@api.get("/api/stats")
def get_counts():
    """Returns { "liked": 12, "disliked": 4 }"""
    return backend.get_stats()

@api.get("/api/stats/genres/{google_id}")
def get_genre_pie_data(google_id: str):
    """Returns { "GenreName": Count } for all liked items."""
    return backend.get_genre_stats(google_id)

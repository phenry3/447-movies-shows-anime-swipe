export type MediaItem = {
    media_type : "movie" | "tv" | "anime";
    title : string;
    overview : string;
    genres : string[];
    thumbnail_url: string;
    release_date : string; 
    vote_average : number;
}


export type FeedbackPaylaod ={
    google_id : string;
    title : string;
    action : "like" | "dislike";
};


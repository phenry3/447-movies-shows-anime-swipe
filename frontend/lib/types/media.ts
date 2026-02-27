export type MediaItem = {
    uid : string;
    media_type : "movie" | "tv" | "anime";
    title : string;
    overview : string;
    genres : string[];
    thumbnail_url: string;
    release_date : string; 
    vote_average : number;
}
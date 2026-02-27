import { MediaItem } from "../types/media";

export const mockMedia : MediaItem[] = [
   {
    uid: "movie_1",
    media_type: "movie",
    title : "Toy Story",
    overview : "bla bla bla",
    genres : ["Animation", "Comedy", "Family"],
    thumbnail_url : "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRw1ynxwA6p8jGMs5TD1Q6BFgn9fafEk-XQ3lrYQGQo0q4Ggo3a",
    release_date : "1995-11-22",
    vote_average : 8.3
   },
   {
    uid: "movie_2",
    media_type: "movie",
    title : "Jumanji",
    overview : "bla bla bla",
    genres : [ "Adventure" ,"Comedy", "Family"],
    thumbnail_url : "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcThKxlvl9t3vviDqi1q0ZCk2CVLWKPx-1_CjBDm3crbTriIfZpY",
    release_date : "1995-11-22",
    vote_average : 8.7
   },
   {
    uid: "anime_1",
    media_type: "anime",
    title : "Naruto",
    overview : "bla bla bla",
    genres : ["Animation", "Comedy", "Family", "Action", "Adventure"],
    thumbnail_url : "https://www.imdb.com/title/tt0409591/mediaviewer/rm651630848/?ref_=tt_ov_i",
    release_date : "1995-11-22",
    vote_average : 9.3
   },
   {
    uid: "anime_2",
    media_type: "anime",
    title : "Jujitsu Kaisen",
    overview : "bla bla bla",
    genres : ["Action", "Comedy"],
    thumbnail_url : "https://en.wikipedia.org/wiki/Jujutsu_Kaisen#/media/File:Jujutsu_kaisen.jpg",
    release_date : "1995-11-22",
    vote_average : 7.3
   },
   {
    uid: "tv_1",
    media_type: "tv",
    title : "Friends",
    overview : "bla bla bla",
    genres : [ "Comedy", "Family"],
    thumbnail_url : "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRSBPcppkFEt6S-ey_85LhiStjZbEXC5Ff5HEP0jfY82CxZCLTL",
    release_date : "1995-11-22",
    vote_average : 8.3
   },
   {
    uid: "tv_2",
    media_type: "tv",
    title : "The office",
    overview : "bla bla bla",
    genres : ["Comedy", "Family"],
    thumbnail_url : "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT1rLm86VJA7Tcf4ZjWQE6FrXCh9lvUu3RzeNIEDH2YqD3ta8BG",
    release_date : "1995-11-22",
    vote_average : 9.4
   }

]
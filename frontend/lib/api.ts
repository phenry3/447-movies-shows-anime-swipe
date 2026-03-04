import { MediaItem, FeedbackPaylaod } from "./types/media";

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function getRec() : Promise<MediaItem> {
    const res = await fetch(`${BASE_URL}/api/rec`, {cache:"no-store"});
    if (!res.ok) throw new Error(`getRec failed: ${res.status}`);
  return res.json();
}

export async function sendFeedback(payload: FeedbackPaylaod): Promise<MediaItem> {
    const res = await fetch(`${BASE_URL}/api/feedback`, 
                {method : "POST", 
                 headers: {"Content-Type": "application/json"}, 
                 body: JSON.stringify(payload),});

        if (!res.ok) throw new Error(`sendFeedback failed: ${res.status}`);
        return res.json();
}

export async function getMatches() : Promise<MediaItem[]>{
    const res = await fetch(`${BASE_URL}/api/matches`,{cache:"no-store"});
    if(!res.ok) throw new Error(`get Matches failed: ${res.status}`);
    return res.json();
}
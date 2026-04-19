import { MediaItem, FeedbackPaylaod, RemoveMatchPayload } from "./types/media";

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function createUser(payload: {
  google_id: string;
  email: string;
  email_verified: boolean;
  name: string;
  picture: string;
}){
    const res = await fetch (`${BASE_URL}/api/users`, {
        method : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`createUser failed: ${res.status}`);
    return res.json();
}

export async function getRec(google_id: string) : Promise<MediaItem> {
    const res = await fetch(`${BASE_URL}/api/rec/${google_id}`, {cache:"no-store"});
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

export async function getMatches(google_id : string) : Promise<MediaItem[]>{
    const res = await fetch(`${BASE_URL}/api/matches/${google_id}`,{cache:"no-store"});
    if(!res.ok) throw new Error(`get Matches failed: ${res.status}`);
    return res.json();
}

export async function removeMatch(payload: RemoveMatchPayload): Promise<void> {
    const res = await fetch(`${BASE_URL}/api/matches`, {
        method: "DELETE",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`removeMatch failed: ${res.status}`);
}

export async function searchMovies(query: string) {
  const res = await fetch(
    `http://127.0.0.1:8000/api/search?query=${encodeURIComponent(query)}&limit=10`
  );

  if (!res.ok) {
    throw new Error("Failed to search movies");
  }

  return res.json();
}

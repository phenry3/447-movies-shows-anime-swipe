"use client";

import { useEffect, useState } from "react";
import { MediaCard } from "@/components/MediaCard";
import { Heart,X } from "lucide-react";
import { getRec,sendFeedback} from "@/lib/api";
import { MediaItem } from "@/lib/types/media";
import {useSession} from "next-auth/react";

export default function DiscoveryPage() {
  const { data: session, status } = useSession();
  const [item, setItem] = useState<MediaItem | null>(null);
  const [loading, setLoading] = useState(true);

  
  async function loadRec(){

    if (!session?.user?.googleId) return;
    setLoading(true);
    try {
      const rec = await getRec(session.user.googleId);
      setItem(rec);
    }
    finally{
      setLoading(false);
    }
  }

  useEffect(() => {if (status === "authenticated" && session?.user?.googleId) {
      loadRec();
    }}, [status, session?.user?.googleId]);

  async function dislike() {
    if (!item || !session?.user?.googleId) return;
    const next = await sendFeedback({google_id: session.user.googleId, title: item.title, action: "dislike"});
    setItem(next);
  }

  async function like() {
    if (!item || !session?.user?.googleId) return;
    const next = await sendFeedback({google_id: session.user.googleId, title: item.title, action: "like"});
    setItem(next);
  }

  if (loading) return <div>Loading...</div>
  if (!item) {
    return (
      <main className="min-h-screen bg-black text-white p-6">
        No media found.
      </main>
    );
  }

  const iconClass = "h-9 w-9 text-white-500 transition-colors hover:text-white-800";

  return (
    <main className="min-h-screen bg-black text-white">
      <section className="mx-auto flex max-w-6xl flex-col items-center px-6">
        <div className="mt-5 w-full flex justify-center">
          <MediaCard item={item} />
        </div>

        <div className="mt-4 flex items-center gap-10">
          <button
            onClick={dislike}
            className="grid h-15 w-15 place-items-center rounded-full bg-red-600/90 text-3xl shadow-lg ring-1 ring-white/10"
            aria-label="Dislike"
          >
            <X className={iconClass}/>
          </button>

          <button
            onClick={like}
            className="grid h-15 w-15 place-items-center rounded-full bg-green-600/90 text-3xl shadow-lg ring-1 ring-white/10"
            aria-label="Like"
          >
            <Heart className={iconClass}/>
          </button>
        </div>
      </section>
    </main>
  );
}
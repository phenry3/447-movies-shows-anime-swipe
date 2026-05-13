"use client";

import { useEffect, useState } from "react";
import { MediaCard } from "@/components/MediaCard";
import { DetailsCard } from "@/components/DetailsCard";
import UndoButton from "@/components/UndoButton";
import { Heart, X } from "lucide-react";
import { getRec, sendFeedback, getLikedCount, undoFeedback } from "@/lib/api";
import { MediaItem } from "@/lib/types/media";
import { useSession } from "next-auth/react";

export default function DiscoveryPage() {
  const { data: session, status } = useSession();

  const [item, setItem] = useState<MediaItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [likedCount, setLikedCount] = useState<number | null>(null);
  const [canUndo, setCanUndo] = useState(false);
  const [undoing, setUndoing] = useState(false);

  useEffect(() => {
    async function loadCount() {
      if (!session?.user?.googleId) return;

      try {
        const count = await getLikedCount(session.user.googleId);
        setLikedCount(count);
      } catch (err) {
        console.error("Failed to load liked count:", err);
      }
    }

    if (status === "authenticated") {
      loadCount();
    }
  }, [status, session?.user?.googleId]);

  useEffect(() => {
    async function loadRec() {
      if (!session?.user?.googleId) return;
      if (likedCount === null || likedCount < 5) return;

      setLoading(true);
      try {
        const rec = await getRec(session.user.googleId);
        setItem(rec);
      } finally {
        setLoading(false);
      }
    }

    if (status === "authenticated") {
      loadRec();
    }
  }, [status, session?.user?.googleId, likedCount]);

  async function dislike() {
    if (!item || !session?.user?.googleId) return;
    const next = await sendFeedback({
      google_id: session.user.googleId,
      title: item.title,
      action: "dislike",
    });
    setItem(next);
    setCanUndo(true);
  }

  async function like() {
    if (!item || !session?.user?.googleId) return;
    const next = await sendFeedback({
      google_id: session.user.googleId,
      title: item.title,
      action: "like",
    });
    setItem(next);
    setCanUndo(true);
  }


  async function undo(){
    if (!canUndo || undoing) return;
    if (!session?.user?.googleId) return;
    setUndoing(true);
    try{
      const undon = await undoFeedback(session.user.googleId);
      setItem(undon);
      setCanUndo(false);
    }
    finally{
      setUndoing(false);
    }
    
  }

  if (likedCount !== null && likedCount < 5) {
    return (
      <main className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-semibold">
            Please search and select at least 5 movies
          </h1>
          <p className="mt-2 text-white/60">
            You’ve selected {likedCount} so far
          </p>
        </div>
      </main>
    );
  }

  if (loading || likedCount === null) {
    return <div className="text-white p-6">Loading...</div>;
  }

  if (!item) {
    return (
      <main className="min-h-screen bg-black text-white p-6">
        No media found.
      </main>
    );
  }

  const iconClass =
    "h-9 w-9 text-white-500 transition-colors hover:text-white-800";

  return (
    <main className="min-h-screen bg-black text-white">
      <section className="mx-auto flex max-w-6xl flex-col items-center px-6">
        <div className="mt-5 w-full flex justify-center">
          <MediaCard item={item} disableLink />
        </div>

        <div className="mt-4  flex items-center gap-10">
          <button
            onClick={dislike}
            className="grid h-15 w-15 place-items-center rounded-full bg-red-600/90 text-3xl shadow-lg ring-1 ring-white/10 cursor-pointer"
            aria-label="Dislike"
          >
            <X className={iconClass} />
          </button>

          <button
            onClick={like}
            className="grid h-15 w-15 place-items-center rounded-full bg-green-600/90 text-3xl shadow-lg ring-1 ring-white/10 cursor-pointer"
            aria-label="Like"
          >
            <Heart className={iconClass} />
          </button>
        </div>

        <UndoButton disabled={!canUndo} loading={undoing} onClick={undo} />

        <div className="mt-6 w-full mb-6">
          <DetailsCard item={item} />
        </div>
      </section>
    </main>
  );
}

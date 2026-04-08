"use client";

import { useEffect, useState } from "react";
import { MediaCard } from "@/components/MediaCard";
import { getMatches } from "@/lib/api";
import { MediaItem } from "@/lib/types/media";
import { useSession } from "next-auth/react";

export default function MatchesPage() {
  const { data: session, status } = useSession();
  const [matches, setMatches] = useState<MediaItem[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadMatches(googleId: string) {
    setLoading(true);
    try {
      const data = await getMatches(googleId);
      setMatches(data);
    } catch (err) {
      console.error("Failed to load matches:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (status === "authenticated" && session?.user?.googleId) {
      loadMatches(session.user.googleId);
      return;
    }

    if (status === "unauthenticated") {
      setLoading(false);
    }
  }, [status, session?.user?.googleId]);

  if (status === "loading" || loading) return <div className="min-h-screen p-6 text-white">Loading...</div>;
  if (matches.length === 0) return <div className="min-h-screen p-6 text-white">No matches yet.</div>;

  return (
    <main className="min-h-screen bg-black text-white p-6">
      <h1 className="text-2xl font-bold mb-6">Your Matches</h1>
      <div className="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {matches.map((item) => (
          <MediaCard key={item.title} item={item} />
        ))}
      </div>
    </main>
  );
}

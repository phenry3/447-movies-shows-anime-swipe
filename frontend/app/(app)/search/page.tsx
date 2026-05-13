"use client";

import { useEffect, useState } from "react";
import { SearchCard } from "@/components/SearchCard";
import { searchMovies, sendFeedback, getLikedTitles } from "@/lib/api";
import { MediaItem } from "@/lib/types/media";
import { useSession } from "next-auth/react";

export default function SearchPage() {
  const { data: session, status } = useSession();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MediaItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [likedTitles, setLikedTitles] = useState<Set<string>>(new Set());

  useEffect(() => {
    async function loadLikes() {
      if (!session?.user?.googleId) return;

      try {
        const liked = await getLikedTitles(session.user.googleId);
        setLikedTitles(new Set(liked));
      } catch (err) {
        console.error("Failed to load liked titles:", err);
      }
    }

    if (status === "authenticated") {
      loadLikes();
    }
  }, [status, session?.user?.googleId]);

  useEffect(() => {
    const delay = setTimeout(() => {
      if (!query.trim()) {
        setResults([]);
        return;
      }

      async function runSearch() {
        setLoading(true);
        try {
          const data = await searchMovies(query);
          setResults(data);
        } finally {
          setLoading(false);
        }
      }

      runSearch();
    }, 300);

    return () => clearTimeout(delay);
  }, [query]);

  async function handleLike(item: MediaItem) {
    if (!session?.user?.googleId) return;

    setLikedTitles((prev) => new Set(prev).add(item.title));

    try {
      await sendFeedback({
        google_id: session.user.googleId,
        title: item.title,
        action: "like",
      });
    } catch (err) {
      console.error("Failed to like item:", err);

      setLikedTitles((prev) => {
        const updated = new Set(prev);
        updated.delete(item.title);
        return updated;
      });
    }
  }

  return (
    <main className="min-h-screen bg-black text-white p-6">
      <section className="mx-auto max-w-4xl">

        {/* Search input */}
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search movies..."
          className="w-full rounded-lg bg-white/10 px-4 py-3 text-white outline-none ring-1 ring-white/10 focus:ring-white/30"
        />

        {/* Loading */}
        {loading && (
          <p className="mt-4 text-white/60">Searching...</p>
        )}

        {/* Results */}
        <div className="mt-6 flex flex-col gap-4">
          {results.map((item) => {
            const isLiked = likedTitles.has(item.title);

            return (
              <SearchCard
                key={`${item.title}-${item.release_date}`}
                item={item}
                onLike={handleLike}
                liked={isLiked}
              />
            );
          })}
        </div>

        {/* Empty state */}
        {!loading && query && results.length === 0 && (
          <p className="mt-6 text-white/50">
            No results found.
          </p>
        )}

      </section>
    </main>
  );
}
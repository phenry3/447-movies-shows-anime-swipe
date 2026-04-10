"use client";

import { useEffect, useState } from "react";
import { MediaCard } from "@/components/MediaCard";
import { searchMovies } from "@/lib/api";
import { MediaItem } from "@/lib/types/media";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MediaItem[]>([]);
  const [loading, setLoading] = useState(false);

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
    }, 300); // debounce

    return () => clearTimeout(delay);
  }, [query]);

  return (
    <main className="min-h-screen bg-black text-white p-6">
      <section className="mx-auto max-w-6xl">

        {/* Search input */}
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search movies..."
          className="w-full rounded-lg bg-white/10 px-4 py-3 text-white outline-none ring-1 ring-white/10 focus:ring-white/30"
        />

        {/* Loading state */}
        {loading && (
          <p className="mt-4 text-white/60">Searching...</p>
        )}

        {/* Results grid */}
        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {results.map((item) => (
            <MediaCard key={item.title} item={item} />
          ))}
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
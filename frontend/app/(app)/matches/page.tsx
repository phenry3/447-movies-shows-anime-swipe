"use client";

import { useEffect, useId, useState } from "react";
import { DetailsCard } from "@/components/DetailsCard";
import { MediaCard } from "@/components/MediaCard";
import { getMatches } from "@/lib/api";
import { MediaItem } from "@/lib/types/media";

export default function MatchesPage() {
  const [matches, setMatches] = useState<MediaItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedMatch, setSelectedMatch] = useState<MediaItem | null>(null);
  const detailsTitleId = useId();

  async function loadMatches() {
    setLoading(true);
    try {
      const data = await getMatches();
      setMatches(data);
    } catch (err) {
      console.error("Failed to load matches:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMatches();
  }, []);

  useEffect(() => {
    if (!selectedMatch) {
      return;
    }

    const originalOverflow = document.body.style.overflow;
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setSelectedMatch(null);
      }
    };

    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = originalOverflow;
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [selectedMatch]);

  if (loading) return <div className="min-h-screen p-6 text-white">Loading...</div>;
  if (matches.length === 0) return <div className="min-h-screen p-6 text-white">No matches yet.</div>;

  return (
    <main className="min-h-screen bg-black text-white p-6">
      <h1 className="text-2xl font-bold mb-6">Your Matches</h1>
      <div className="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {matches.map((item) => (
          <MediaCard
            key={item.title}
            item={item}
            onClick={() => setSelectedMatch(item)}
          />
        ))}
      </div>

      {selectedMatch ? (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 sm:p-6"
          onClick={() => setSelectedMatch(null)}
        >
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby={detailsTitleId}
            className="w-full max-w-5xl max-h-[calc(100vh-4rem)] overflow-y-auto"
            onClick={(event) => event.stopPropagation()}
          >
            <DetailsCard
              item={selectedMatch}
              titleId={detailsTitleId}
              onClose={() => setSelectedMatch(null)}
              opaque
            />
          </div>
        </div>
      ) : null}
    </main>
  );
}
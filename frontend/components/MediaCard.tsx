import Image from "next/image";
import Link from "next/link";
import type { MediaItem } from "@/lib/types/media";


export function MediaCard({ item }: { item: MediaItem }) {
  const href = `/media/${encodeURIComponent(item.title)}`;

  const imgSrc = item.thumbnail_url.startsWith("http")
  ? item.thumbnail_url
  : `https://image.tmdb.org/t/p/w500${item.thumbnail_url}`;

  return (
    <Link
      href={href}
      className="relative block w-full max-w-md overflow-hidden rounded-3xl bg-white/5 ring-1 ring-white/10"
    >
      {/* Poster */}
      <div className="relative h-[600px] w-full">
        <Image
          src={imgSrc}
          alt={item.title}
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-black/10" />
      </div>

      {/* Bottom overlay */}
      <div className="absolute bottom-0 w-full p-6">
        <div className="flex items-end justify-between gap-4">
          <h2 className="text-4xl font-bold leading-tight">{item.title}</h2>

          {typeof item.vote_average === "number" && (
            <span className="rounded-full bg-white/10 px-3 py-1 text-sm ring-1 ring-white/15">
              {item.vote_average.toFixed(1)}
            </span>
          )}
        </div>

        <p className="mt-1 text-sm text-white/70">
          {item.media_type.toUpperCase()}
          {item.release_date ? ` • ${item.release_date.slice(0, 4)}` : ""}
        </p>

        <div className="mt-3 flex flex-wrap gap-2">
          {(item.genres ?? []).slice(0, 3).map((g) => (
            <span
              key={g}
              className="rounded-full bg-white/10 px-3 py-1 text-xs ring-1 ring-white/15"
            >
              {g}
            </span>
          ))}
        </div>

        <p className="mt-4 text-sm italic text-white/85 line-clamp-2">
          “{item.overview}”
        </p>
      </div>
    </Link>
  );
}
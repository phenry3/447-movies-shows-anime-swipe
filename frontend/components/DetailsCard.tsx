import type { ReactNode } from "react";
import { CalendarDays, Film, Star, Tags, X } from "lucide-react";
import type { MediaItem } from "@/lib/types/media";

function DetailInfo({
  icon,
  label,
  value,
  opaque = false,
}: {
  icon: ReactNode;
  label: string;
  value: string;
  opaque?: boolean;
}) {
  return (
    <div
      className={`h-full min-h-[104px] rounded-2xl border border-white/10 p-4 ${
        opaque ? "bg-[#161616]" : "bg-white/[0.03]"
      }`}
    >
      <div className="flex h-full items-center gap-3">
        <div className="grid h-10 w-10 place-items-center rounded-2xl bg-white/5 text-white/75 ring-1 ring-white/10">
          {icon}
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-[11px] uppercase tracking-[0.22em] text-white/45">
            {label}
          </p>
          <p className="mt-1 line-clamp-2 break-words text-sm leading-6 font-medium text-white/90">
            {value}
          </p>
        </div>
      </div>
    </div>
  );
}

type DetailsCardProps = {
  item: MediaItem;
  onClose?: () => void;
  titleId?: string;
  opaque?: boolean;
};

export function DetailsCard({
  item,
  onClose,
  titleId,
  opaque = false,
}: DetailsCardProps) {
  const overview = item.overview?.trim() || "Unknown";
  const release = item.release_date?.trim() || "Unknown";
  const rating = String(item.vote_average);
  const genres = item.genres.length > 0 ? item.genres.join(", ") : "Unknown";

  return (
    <article
      className={`relative w-full overflow-hidden rounded-3xl border border-white/10 p-5 shadow-sm sm:p-7 ${
        opaque ? "bg-[#0d0d0d]" : "bg-white/[0.03]"
      }`}
    >
      {onClose ? (
        <button
          type="button"
          onClick={onClose}
          className="absolute top-5 right-5 grid h-11 w-11 place-items-center rounded-full bg-white/5 text-white/80 ring-1 ring-white/10 transition hover:bg-white/10 hover:text-white"
          aria-label={`Close details for ${item.title}`}
        >
          <X className="h-5 w-5" />
        </button>
      ) : null}

      <div
        className={`flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between ${
          onClose ? "pr-14 sm:pr-16" : ""
        }`}
      >
        <div className="max-w-2xl">
          <h2
            id={titleId}
            className="text-3xl font-semibold tracking-tight text-white sm:text-4xl"
          >
            {item.title}
          </h2>
          <p className="mt-4 text-sm leading-7 text-white/75 sm:text-[15px]">
            {overview}
          </p>
        </div>

        <div className="grid w-full gap-3 sm:auto-rows-fr sm:grid-cols-2 lg:w-[24rem] lg:flex-none lg:grid-cols-1">
          <DetailInfo
            icon={<Film className="h-4 w-4" />}
            label="Format"
            value={item.media_type.toUpperCase()}
            opaque={opaque}
          />
          <DetailInfo
            icon={<CalendarDays className="h-4 w-4" />}
            label="Release"
            value={release}
            opaque={opaque}
          />
          <DetailInfo
            icon={<Star className="h-4 w-4" />}
            label="Rating"
            value={rating}
            opaque={opaque}
          />
          <DetailInfo
            icon={<Tags className="h-4 w-4" />}
            label="Genres"
            value={genres}
            opaque={opaque}
          />
        </div>
      </div>
    </article>
  );
}

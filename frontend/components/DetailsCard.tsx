import type { ReactNode } from "react";
import { CalendarDays, Film, Star, Tags } from "lucide-react";
import type { MediaItem } from "@/lib/types/media";

function DetailInfo({
  icon,
  label,
  value,
}: {
  icon: ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="h-full min-h-[104px] rounded-2xl border border-white/10 bg-white/[0.03] p-4">
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

export function DetailsCard({ item }: { item: MediaItem }) {
  const overview = item.overview?.trim() || "Unknown";
  const release = item.release_date?.trim() || "Unknown";
  const rating = String(item.vote_average);
  const genres = item.genres.length > 0 ? item.genres.join(", ") : "Unknown";

  return (
    <article className="w-full overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] p-5 shadow-sm sm:p-7">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div className="max-w-2xl">
          <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
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
          />
          <DetailInfo
            icon={<CalendarDays className="h-4 w-4" />}
            label="Release"
            value={release}
          />
          <DetailInfo
            icon={<Star className="h-4 w-4" />}
            label="Rating"
            value={rating}
          />
          <DetailInfo
            icon={<Tags className="h-4 w-4" />}
            label="Genres"
            value={genres}
          />
        </div>
      </div>
    </article>
  );
}

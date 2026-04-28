import type { MediaItem } from "@/lib/types/media";

type SearchCardProps = {
  item: MediaItem;
  onLike?: (item: MediaItem) => void;
  liked?: boolean;
};

export function SearchCard({ item, onLike, liked }: SearchCardProps) {
  return (
    <div className="w-full rounded-xl bg-white/5 p-4 ring-1 ring-white/10 flex justify-between items-center">
      
      <div>
        <h3 className="text-lg font-semibold">{item.title}</h3>

        <p className="text-sm text-white/60">
          {item.media_type.toUpperCase()}
          {item.release_date ? ` • ${item.release_date.slice(0, 4)}` : ""}
        </p>
      </div>

      <button
        disabled={liked}
        onClick={() => onLike?.(item)}
        className={`rounded-full px-4 py-2 text-sm transition
          ${liked 
            ? "bg-gray-600 cursor-not-allowed" 
            : "bg-green-600 hover:bg-green-500"}`}
      >
        {liked ? "Liked" : "Like"}
      </button>
    </div>
  );
}
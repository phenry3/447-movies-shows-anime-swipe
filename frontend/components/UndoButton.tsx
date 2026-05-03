"use client";

import { Undo2 } from "lucide-react";

type UndoButtonProps = {
  disabled: boolean;
  loading?: boolean;
  onClick: () => void;
};

export default function UndoButton({
  disabled,
  loading = false,
  onClick,
}: UndoButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || loading}
      className="mt-4 inline-flex items-center gap-2 rounded-full bg-white/10 px-5 py-2.5 text-sm font-medium text-white shadow-lg ring-1 ring-white/15 transition hover:bg-white/15 disabled:cursor-not-allowed disabled:bg-white/5 disabled:text-white/35 disabled:ring-white/10"
      aria-label="Undo previous feedback"
    >
      <Undo2 className="h-4 w-4" />
      {loading ? "Undoing..." : "Undo"}
    </button>
  );
}

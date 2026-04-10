// components/StatsCard.tsx
"use client";

interface StatsCardProps {
  label: string;
  count: number;
  color?: string; // optional for different card colors
}

export function StatsCard({ label, count, color = "bg-blue-600" }: StatsCardProps) {
  return (
    <div className={`p-6 rounded-lg shadow-md ${color} text-white`}>
      <h2 className="text-lg font-semibold">{label}</h2>
      <p className="text-3xl font-bold mt-2">{count}</p>
    </div>
  );
}
"use client";

import { useEffect, useState } from "react";
import { StatsCard } from "@/components/StatsCard";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  ChartOptions,
  ChartData,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

interface Stats {
  liked: number;
  disliked: number;
}

interface GenreStats {
  [genre: string]: number;
}

export default function StatsPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [genres, setGenres] = useState<GenreStats>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const resStats = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/stats`,
          { cache: "no-store" }
        );
        if (!resStats.ok)
          throw new Error(`Failed to fetch stats: ${resStats.status}`);
        const dataStats = await resStats.json();
        setStats(dataStats);

        const resGenres = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/stats/genres`,
          { cache: "no-store" }
        );
        if (!resGenres.ok)
          throw new Error(`Failed to fetch genres: ${resGenres.status}`);
        const dataGenres: GenreStats = await resGenres.json();

        const sorted = Object.entries(dataGenres)
          .sort(([, a], [, b]) => b - a)
          .slice(0, 5); //change the 5 for more or less genres
        setGenres(Object.fromEntries(sorted));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
  }, []);

  if (loading) return <p className="p-6 text-white">Loading stats...</p>;
  if (!stats) return <p className="p-6 text-red-500">Failed to load stats</p>;

  const data: ChartData<"pie", number[], string> = {
    labels: Object.keys(genres),
    datasets: [
      {
        data: Object.values(genres),
        backgroundColor: ["#10B981", "#F59E0B", "#EF4444", "#3B82F6", "#8B5CF6"],
      },
    ],
  };

  const plugins = [
    {
      id: "sliceLabels",
      afterDraw: (chart: any) => {
        const { ctx, chartArea: { width, height }, data } = chart;
        ctx.save();
        const radius = chart._metasets[0].data[0].outerRadius;
        const centerX = width / 2;
        const centerY = height / 2;

        chart._metasets[0].data.forEach((arc: any, index: number) => {
          const midAngle = (arc.startAngle + arc.endAngle) / 2;
          const x = centerX + (radius / 2) * Math.cos(midAngle);
          const y = centerY + (radius / 2) * Math.sin(midAngle);

          const label = data.labels?.[index];
          if (typeof label === "string") {
            ctx.fillStyle = "#fff";
            ctx.font = "bold 14px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(label, x, y);
          }
        });
        ctx.restore();
      },
    },
  ];

  const options: ChartOptions<"pie"> = {
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true },
    },
  };

  return (
    <main className="min-h-screen bg-black p-6 text-white">
      <h1 className="text-2xl font-bold mb-6">Your Stats</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <StatsCard label="Liked Movies" count={stats.liked} color="bg-green-600" />
        <StatsCard label="Disliked Movies" count={stats.disliked} color="bg-red-600" />
      </div>

      {/* Pie Chart */}
      {Object.keys(genres).length > 0 && (
        <div className="max-w-md mx-auto">
          <Pie data={data} options={options} plugins={plugins} />
          <p className="text-center text-white mt-4 font-semibold">Your Top 5 Genres</p>
        </div>
      )}
    </main>
  );
}
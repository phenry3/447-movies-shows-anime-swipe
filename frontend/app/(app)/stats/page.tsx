"use client";

import { useEffect, useState } from "react";
import { StatsCard } from "@/components/StatsCard";
import { Pie } from "react-chartjs-2";
import { useSession } from "next-auth/react";  // phil change for stats to work
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
  const { data: session, status } = useSession();  // phill added for status to work
  const [stats, setStats] = useState<Stats | null>(null);
  const [genres, setGenres] = useState<GenreStats>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    // needed to add user authentication check, phil added
    if (status !== "authenticated" || !session?.user?.googleId) {
      if (status === "unauthenticated") setLoading(false);
      return;
    }

    const googleId = session.user.googleId;  // phil change 412

    async function fetchStats() {
      try {
        const resStats = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/stats/${googleId}`,
          { cache: "no-store" }
        );
        if (!resStats.ok)
          throw new Error(`Failed to fetch stats: ${resStats.status}`);

        const dataStats = await resStats.json();
        setStats(dataStats);

        const resGenres = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/stats/genres/${googleId}`,
          { cache: "no-store" }
        );
        if (!resGenres.ok)
          throw new Error(`Failed to fetch genres: ${resGenres.status}`);

        const dataGenres: GenreStats = await resGenres.json();

        //only does top 5
        const sorted = Object.entries(dataGenres)
          .sort(([, a], [, b]) => b - a)
          .slice(0, 5);

        setGenres(Object.fromEntries(sorted));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
  }, [status, session?.user?.googleId]); // user id dependency

  if (loading)
    return <p className="p-6 text-white">Loading stats...</p>;

  if (!stats)
    return <p className="p-6 text-red-500">Failed to load stats</p>;


  const safeGenres: Record<string, number> = { ...genres };

  const keys = Object.keys(safeGenres);
  const values = Object.values(safeGenres);

  if (keys.length === 1) {
    safeGenres["Other"] = Math.max(1, Math.floor(values[0] * 0.5));
  }

  const labels = Object.keys(safeGenres);
  const dataValues = Object.values(safeGenres);

  const data: ChartData<"pie", number[], string> = {
    labels,
    datasets: [
      {
        data: dataValues,
        backgroundColor: [
          "#10B981",
          "#F59E0B",
          "#EF4444",
          "#3B82F6",
          "#8B5CF6",
        ],
      },
    ],
  };

  const plugins = [
    {
      id: "sliceLabels",
      afterDraw: (chart: any) => {
        const meta = chart.getDatasetMeta(0);
        const labels = chart.data.labels;

        if (!meta?.data || !labels) return;

        const ctx = chart.ctx;

        meta.data.forEach((arc: any, index: number) => {
          const label = labels[index];
          if (!label) return;

          const midAngle = (arc.startAngle + arc.endAngle) / 2;

          const radius = arc.outerRadius * 0.65;
          const x = arc.x + radius * Math.cos(midAngle);
          const y = arc.y + radius * Math.sin(midAngle);

          ctx.save();
          ctx.fillStyle = "#fff";
          ctx.font = "bold 13px sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(String(label), x, y);
          ctx.restore();
        });
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
      <h1 className="mb-6 text-2xl font-bold">Your Stats</h1>

      {/* Stats Cards */}
      <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2">
        <StatsCard
          label="Liked Movies"
          count={stats.liked}
          color="bg-green-600"
        />
        <StatsCard
          label="Disliked Movies"
          count={stats.disliked}
          color="bg-red-600"
        />
      </div>

      {/* Pie Chart */}
      {labels.length > 0 && (
        <div className="mx-auto max-w-md">
          <Pie data={data} options={options} plugins={plugins} />

          <p className="mt-4 text-center font-semibold text-white">
            Your Top Genres
          </p>
        </div>
      )}
    </main>
  );
}

import Navigation from "@/components/Navigation";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-black text-white pt-20">
      <Navigation/>
      {children}
    </main>
  );
}
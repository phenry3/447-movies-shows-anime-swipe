"use client"

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import LoginButtons from "@/components/LoginButtons";

export default function Home() {

  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "authenticated") {
      router.replace("/discovery");
    }
  }, [status, router]);

  if (status === "loading") {
    return null;
  }

  if (session) {
    return null;
  }

  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center">
      <LoginButtons />
    </main>
  );
}
"use client"

import Navigation from "@/components/Navigation";
import {useSession} from "next-auth/react"
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { createUser } from "@/lib/api";


export default function AppLayout({ children }: { children: React.ReactNode }) {
  
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/");
    }
  }, [status, router]);

  useEffect(() => {
    async function syncUserToBackend() {
      if (
        status !== "authenticated" ||
        !session?.user?.email ||
        !session?.user?.googleId
      ) {
        return;
      }

      try {
        await createUser({
          google_id: session.user.googleId,
          email: session.user.email,
          email_verified: true,
          name: session.user.name ?? "",
          picture: session.user.image ?? "",
        });
      } catch (error) {
        console.error("Failed to create user in backend:", error);
      }
    }

    syncUserToBackend();
  }, [status, session]);

  if (status === "loading") {
    return null;
  }
  
  if (!session) {
    return null;
  }
  
  return (
    <main className="min-h-screen bg-black text-white pt-20">
      <Navigation/>
      {children}
    </main>
  );
}
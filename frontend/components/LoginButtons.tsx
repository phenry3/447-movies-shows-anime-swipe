"use client";
import { signIn} from "next-auth/react";

export default function LoginButtons() {
  return (
    <div className="flex flex-col gap-4 justify-center items-center">
      <h1 className="text-3xl font-semibold text-white">FilmFlicks</h1>
      <button
        onClick={() => signIn("google", { callbackUrl: "/discovery" })}
        className="rounded-full bg-white px-6 py-3 text-black font-medium cursor-pointer"
      >
        Sign in with Google
      </button>
    </div>
  );
}
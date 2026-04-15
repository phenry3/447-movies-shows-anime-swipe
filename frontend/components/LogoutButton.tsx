"use client"

import { signOut } from "next-auth/react"

type LogoutButtonProps = {
  className?: string;
};

export default function LoginButton({className = ""} : LogoutButtonProps){
    return (
        <button onClick={() => signOut({ callbackUrl: "/" })} className={className}>
            Sign Out
        </button>
    );
}
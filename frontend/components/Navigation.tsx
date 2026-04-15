"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Heart, Compass, Film, BarChart, Search} from "lucide-react";
import LogoutButton from "./LogoutButton"
{/**Helper function that takes inputs and gives one string that can be put into className */}
function cx(...classes: Array<string | false | undefined>) {
  return classes.filter(Boolean).join(" ");
}

export default function Navigation() {
  const pathname = usePathname();

  const isDiscovery = pathname === "/discovery";
  const isLiked = pathname === "/matches";
  const isStats = pathname === "/stats";
  const isSearch = pathname === "/search";

  const baseLink = "group flex items-center gap-2 rounded-full px-4 py-2 text-sm transition-colors";

  
  const activeLink = "bg-purple-500/45 ring-1 ring-purple-600/35";
  const inactiveLink = "bg-transparent";

  
  const iconClass = "h-6 w-6 text-purple-300 transition-colors group-hover:text-purple-200";
  const textClass = "text-purple-300 transition-colors group-hover:text-purple-200";

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/70 backdrop-blur">
      <div className="mx-auto flex max-w-[88rem] items-center justify-between px-6 py-5 ">
        <Link href="/discovery" className="group flex items-center gap-3">
          <Film className="h-10 w-10 text-purple-400 transition-colors group-hover:text-purple-300" />
          <span className="text-xl font-semibold text-white transition-colors group-hover:text-white">
            FilmFlicks
          </span>
        </Link>

        <nav className="flex items-center gap-3">
          <Link
            href="/discovery"
            className={cx(baseLink, isDiscovery ? activeLink : inactiveLink)}
          >
            <Compass className={iconClass} />
            <span className={textClass}>Discovery</span>
          </Link>

          <Link
            href="/matches"
            className={cx(baseLink, isLiked ? activeLink : inactiveLink)}
          >
            <Heart className={iconClass} />
            <span className={textClass}>Liked</span>
          </Link>

          <Link
            href="/stats"
            className={cx(baseLink, isStats ? activeLink : inactiveLink)}
          >
            <BarChart className={iconClass} />
            <span className={textClass}>Stats</span>
          </Link>

          <Link
            href="/search"
            className={cx(baseLink, isSearch ? activeLink : inactiveLink)}
          >
            <Search className={iconClass} />
            <span className={textClass}>Search</span>
          </Link>

          <LogoutButton
            className={cx(baseLink, inactiveLink, "text-purple-300 hover:text-purple-200")}
          />
            
          
        </nav>
      </div>
    </header>
  );
}

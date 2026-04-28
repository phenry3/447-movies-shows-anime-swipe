import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "image.tmdb.org", pathname: "/t/p/**" },
      { protocol: "https", hostname: "myanimelist.cdn-dena.com", pathname: "/images/**" },
      { protocol: "https", hostname: "myanimelist.net", pathname: "/images/**" },
    ],
  },
};

export default nextConfig;
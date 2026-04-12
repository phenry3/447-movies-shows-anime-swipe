import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "image.tmdb.org", pathname: "/t/p/**" },
      { protocol: "https", hostname: "myanimelist.cdn-dena.com", pathname: "/images/**" },
      
    ],
  },
};

export default nextConfig;
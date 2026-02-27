import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "encrypted-tbn3.gstatic.com" },
      // you might also need these depending on your mock urls:
      { protocol: "https", hostname: "encrypted-tbn0.gstatic.com" },
      { protocol: "https", hostname: "encrypted-tbn1.gstatic.com" },
      { protocol: "https", hostname: "encrypted-tbn2.gstatic.com" },
      { protocol: "https", hostname: "www.imdb.com" },
      { protocol: "https", hostname: "en.wikipedia.org" },
    ],
  },
};

export default nextConfig;

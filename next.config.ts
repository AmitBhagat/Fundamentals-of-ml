import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true, // Required for static export
  },
  // Only apply basePath in production (e.g., GitHub Pages deployment)
  // Local development will remain at the root '/'
  basePath: process.env.NODE_ENV === 'production' ? '/Fundamentals-of-ml' : undefined,
};

export default nextConfig;

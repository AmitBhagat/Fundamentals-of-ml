import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true, // Required for static export
  },
  // If your repo is "Math4ML", your URL is username.github.io/Math4ML/
  // basePath: '/Math4ML',
};

export default nextConfig;

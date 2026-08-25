/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Requis pour le build Docker : génère un serveur Node autonome
  // dans .next/standalone (utilisé par app/frontend/Dockerfile)
  output: "standalone",
};

module.exports = nextConfig;

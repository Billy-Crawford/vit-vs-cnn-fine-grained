/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Requis pour le build Docker : g├®n├¿re un serveur Node autonome
  // dans .next/standalone (utilis├® par app/frontend/Dockerfile)
  output: "standalone",
};

module.exports = nextConfig;

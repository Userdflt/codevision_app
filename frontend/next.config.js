/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  distDir: 'out',
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://code-vision-api-australia-southeast1-YOUR_PROJECT_ID.a.run.app',
  },
  // Remove rewrites for static export - API calls will go directly to Cloud Run
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
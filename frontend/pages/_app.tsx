// frontend/pages/_app.tsx
import { createBrowserClient } from '@supabase/ssr'
import type { SupabaseClient } from '@supabase/supabase-js'
import { createContext, useContext, useEffect, useState } from 'react'
import type { AppProps } from 'next/app'
import { useRouter } from 'next/router'
import '../styles/globals.css'
import { SupabaseContextType } from '../lib/types'

const SupabaseContext = createContext<SupabaseContextType | undefined>(undefined)

export function useSupabase(): SupabaseContextType {
  const context = useContext(SupabaseContext)
  if (!context) {
    throw new Error('useSupabase must be used within a SupabaseProvider')
  }
  return context
}

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter()
  const [supabase] = useState<SupabaseClient>(() =>
    createBrowserClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    )
  )

  // Prevent automatic session checking on reset-password page
  useEffect(() => {
    if (router.pathname === '/reset-password') {
      console.log('Skipping auto session check on reset-password page')
      return // Don't auto-check session on reset page
    }

    // Auto-check session for other pages
    const checkSession = async () => {
      try {
        console.log('Auto-checking session for page:', router.pathname)
        await supabase.auth.getSession()
      } catch (error) {
        console.warn('Session check failed:', error)
      }
    }

    checkSession()
  }, [router.pathname, supabase])

  return (
    <SupabaseContext.Provider value={{ supabase, session: null, user: null }}>
      <Component {...pageProps} />
    </SupabaseContext.Provider>
  )
}
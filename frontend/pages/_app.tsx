import { createBrowserClient } from '@supabase/ssr'
import type { SupabaseClient } from '@supabase/supabase-js'
import { createContext, useContext, useEffect, useState } from 'react'
import type { AppProps } from 'next/app'
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
  const [supabase] = useState<SupabaseClient>(() =>
    createBrowserClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    )
  )

  return (
    <SupabaseContext.Provider value={{ supabase, session: null, user: null }}>
      <Component {...pageProps} />
    </SupabaseContext.Provider>
  )
}
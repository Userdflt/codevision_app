import { ReactNode } from 'react'
import { User } from '@supabase/supabase-js'
import Header from './Header'

interface LayoutProps {
  children: ReactNode
  user?: User
  onSignOut: () => void
}

export default function Layout({ children, user, onSignOut }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onSignOut={onSignOut} />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}
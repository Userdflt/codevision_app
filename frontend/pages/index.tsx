import { useState, useEffect } from 'react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Head from 'next/head'
import Layout from '../components/Layout'
import ChatInterface from '../components/ChatInterface'
import AuthModal from '../components/AuthModal'

export default function Home() {
  const session = useSession()
  const supabase = useSupabaseClient()
  const [showAuthModal, setShowAuthModal] = useState(false)

  useEffect(() => {
    if (!session) {
      setShowAuthModal(true)
    }
  }, [session])

  const handleSignOut = async () => {
    await supabase.auth.signOut()
  }

  return (
    <>
      <Head>
        <title>Code Vision - AI Building Code Assistant</title>
        <meta name="description" content="AI-powered assistant for Australian building codes and regulations" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </Head>

      <Layout
        user={session?.user}
        onSignOut={handleSignOut}
      >
        {session ? (
          <ChatInterface userId={session.user.id} />
        ) : (
          <div className="flex items-center justify-center min-h-[50vh]">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Welcome to Code Vision
              </h2>
              <p className="text-gray-600 mb-8">
                Your AI-powered assistant for Australian building codes and regulations
              </p>
              <button
                onClick={() => setShowAuthModal(true)}
                className="bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
              >
                Sign In to Get Started
              </button>
            </div>
          </div>
        )}
      </Layout>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
      />
    </>
  )
}
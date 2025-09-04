import { useState, useEffect } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import { Session } from '@supabase/supabase-js'
import ChatInterface from '../components/ChatInterface'
import AuthModal from '../components/AuthModal'
import HeroSection from '../components/HeroSection'
import Features from '../components/features-2'
import ContentSection from '../components/content-1'
import Footer from '../components/footer'
import { useSupabase } from './_app'
import { Button } from '@/components/ui/button'

export default function Home() {
  const router = useRouter()
  const { supabase } = useSupabase()
  const [session, setSession] = useState<Session | null>(null)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [showChat, setShowChat] = useState(false)

  useEffect(() => {
    // Don't auto-check session if we're on auth-related routes
    if (router.pathname === '/reset-password' || router.pathname === '/confirm-email') {
      console.log('Skipping session check on auth route:', router.pathname)
      return
    }
  
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
    })
  
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
      if (session) {
        setShowChat(true)
      }
    })
  
    return () => subscription.unsubscribe()
  }, [supabase, router.pathname]) // Add router.pathname to dependencies

  const handleSignOut = async () => {
    await supabase.auth.signOut()
    setShowChat(false)
  }

  const handleGetStarted = () => {
    if (session) {
      setShowChat(true)
    } else {
      setShowAuthModal(true)
    }
  }

  if (showChat && session) {
    return (
      <>
        <Head>
          <title>Code Vision - AI Building Code Assistant</title>
          <meta name="description" content="AI-powered assistant for the New Zealand Building Code (NZBC) and regulations" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <div className="min-h-screen bg-background">
          {/* Chat Header */}
          <header className="bg-background border-b border-border shadow-sm">
            <div className="container mx-auto px-4">
              <div className="flex justify-between items-center h-16">
                <div className="flex items-center">
                  <h1 className="text-xl font-bold text-foreground">
                    Code Vision
                  </h1>
                  <span className="ml-2 text-sm text-muted-foreground">
                    AI Building Code Assistant
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <Button 
                    variant="outline" 
                    onClick={() => setShowChat(false)}
                  >
                    Back to Home
                  </Button>
                  <Button 
                    variant="destructive" 
                    onClick={handleSignOut}
                  >
                    Sign Out
                  </Button>
                </div>
              </div>
            </div>
          </header>

          {/* Chat Interface */}
          <main className="container mx-auto px-4 py-8">
            <ChatInterface userId={session.user.id} />
          </main>
        </div>
      </>
    )
  }

  return (
    <>
      <Head>
        <title>Code Vision - AI Building Code Assistant</title>
        <meta name="description" content="AI-powered assistant for the New Zealand Building Code (NZBC) and regulations" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </Head>

      <div className="min-h-screen bg-background">
        {/* Hero Section with custom CTA */}
        <HeroSection />
        
        {/* Custom CTA section replacing the hero buttons */}
        <section className="py-16 bg-muted/50">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-3xl font-bold text-foreground mb-4">
              Ready to streamline your NZ Building Code compliance?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Get instant answers to complex NZBC questions with our AI assistant — from fire protection to structure, durability, moisture, safety of users, services and facilities, and energy efficiency.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                onClick={handleGetStarted}
                className="text-lg px-8 py-3"
              >
                {session ? 'Open Chat Assistant' : 'Get Started'}
              </Button>
              {!session && (
                <Button 
                  variant="outline" 
                  size="lg" 
                  onClick={() => setShowAuthModal(true)}
                  className="text-lg px-8 py-3"
                >
                  Sign In
                </Button>
              )}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <Features />

        {/* Content Section */}
        <ContentSection />

        {/* Footer */}
        <Footer />
      </div>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
      />
    </>
  )
}
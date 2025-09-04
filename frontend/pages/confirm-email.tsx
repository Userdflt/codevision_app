// frontend/pages/confirm-email.tsx
import { useEffect, useState } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import { useSupabase } from './_app'
import { Button } from '@/components/ui/button'
import { LogoIcon } from '@/components/logo'

export default function ConfirmEmailPage() {
  const { supabase } = useSupabase()
  const router = useRouter()
  const [message, setMessage] = useState('')
  const [isConfirmed, setIsConfirmed] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!router.isReady) return

    console.log('Email confirmation page loaded')
    console.log('Full URL:', typeof window !== 'undefined' ? window.location.href : '')
    console.log('Router query:', router.query)
    console.log('Location hash:', typeof window !== 'undefined' ? window.location.hash : '')

    const processEmailConfirmation = async () => {
      try {
        // 1) Handle explicit error from URL params first
        const err = router.query.error as string | undefined
        const errDesc = router.query.error_description as string | undefined
        if (err) {
          console.log('Error from URL params:', err, errDesc)
          setMessage(decodeURIComponent(errDesc || 'Email confirmation failed.'))
          setIsConfirmed(false)
          setIsLoading(false)
          return
        }

        // 2) Handle hash-based tokens (Supabase default for email links)
        if (typeof window !== 'undefined' && window.location.hash) {
          const hash = window.location.hash.slice(1) // Remove #
          console.log('Processing hash:', hash)
          
          const hashParams = new URLSearchParams(hash)
          const access_token = hashParams.get('access_token')
          const refresh_token = hashParams.get('refresh_token')
          const type = hashParams.get('type')
          const error = hashParams.get('error')
          const errorDescription = hashParams.get('error_description')
          
          console.log('Hash params:', { 
            hasAccessToken: !!access_token, 
            hasRefreshToken: !!refresh_token, 
            type, 
            error 
          })
          
          // Handle errors in hash
          if (error) {
            console.log('Error in hash:', error, errorDescription)
            setMessage(decodeURIComponent(errorDescription || 'Email confirmation failed'))
            setIsConfirmed(false)
            setIsLoading(false)
            return
          }
          
          // Handle email confirmation tokens (type should be 'signup' for email confirmation)
          if (access_token && refresh_token && (type === 'signup' || type === 'email_change')) {
            console.log('Processing email confirmation with tokens')
            const { data, error: sessionError } = await supabase.auth.setSession({
              access_token,
              refresh_token
            })
            
            if (sessionError) {
              console.error('Session error:', sessionError)
              setMessage('Failed to confirm email. The link may be expired or invalid.')
              setIsConfirmed(false)
              setIsLoading(false)
              return
            }
            
            console.log('Email confirmed successfully:', data)
            setMessage('Your email has been confirmed successfully! You are now logged in.')
            setIsConfirmed(true)
            setIsLoading(false)
            
            // Optional: Auto-redirect to home after a few seconds
            setTimeout(() => {
              router.push('/')
            }, 3000)
            
            return
          }
        }

        // 3) Check if there's already a valid session (user might have already confirmed)
        const { data: { session }, error: sessionError } = await supabase.auth.getSession()
        console.log('Current session check:', { hasSession: !!session, error: sessionError })
        
        if (session?.user) {
          console.log('User already has valid session')
          setMessage('Your email is already confirmed and you are logged in!')
          setIsConfirmed(true)
          setIsLoading(false)
          return
        }

        // 4) No valid confirmation found
        console.log('No valid email confirmation found')
        setMessage('Invalid or expired confirmation link. Please check your email for a new confirmation link or try signing up again.')
        setIsConfirmed(false)
        setIsLoading(false)

      } catch (error: any) {
        console.error('Email confirmation error:', error)
        setMessage('An unexpected error occurred during email confirmation.')
        setIsConfirmed(false)
        setIsLoading(false)
      }
    }

    processEmailConfirmation()
  }, [router.isReady, router.query, supabase])

  const handleGoToLogin = () => {
    router.push('/')
  }

  return (
    <>
      <Head>
        <title>Confirm Email - CodeVision</title>
        <meta name="description" content="Confirm your email address" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <LogoIcon className="mx-auto h-12 w-auto" />
            <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
              Email Confirmation
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              {isLoading ? 'Processing your email confirmation...' : 'Confirm your account'}
            </p>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            {isLoading ? (
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-2 text-sm text-gray-600">Confirming your email...</p>
              </div>
            ) : (
              <div className="space-y-4">
                {message && (
                  <div className={`p-4 rounded-md ${
                    isConfirmed 
                      ? 'bg-green-50 border border-green-200' 
                      : 'bg-red-50 border border-red-200'
                  }`}>
                    <p className={`text-sm ${
                      isConfirmed ? 'text-green-700' : 'text-red-700'
                    }`}>
                      {message}
                    </p>
                  </div>
                )}

                {isConfirmed ? (
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <h3 className="mt-4 text-lg font-medium text-gray-900">
                        Email Confirmed!
                      </h3>
                      <p className="mt-2 text-sm text-gray-600">
                        You will be redirected to the home page automatically in a few seconds.
                      </p>
                    </div>
                    
                    <Button 
                      onClick={handleGoToLogin}
                      className="w-full"
                    >
                      Continue to CodeVision
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="w-16 h-16 mx-auto bg-red-100 rounded-full flex items-center justify-center">
                        <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <h3 className="mt-4 text-lg font-medium text-gray-900">
                        Confirmation Failed
                      </h3>
                    </div>
                    
                    <Button 
                      onClick={handleGoToLogin}
                      variant="outline"
                      className="w-full"
                    >
                      Go to Login
                    </Button>
                  </div>
                )}
              </div>
            )}
          </div>
          
          <div className="text-center">
            <Button 
              variant="link" 
              onClick={() => router.push('/')}
              className="text-sm"
            >
              ← Back to home
            </Button>
          </div>
        </div>
      </div>
    </>
  )
}
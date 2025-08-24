// frontend/pages/reset-password.tsx
import { FormEvent, useEffect, useState } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import { useSupabase } from './_app'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function ResetPasswordPage() {
  const { supabase } = useSupabase()
  const router = useRouter()
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [message, setMessage] = useState('')
  const [ready, setReady] = useState(false)

  useEffect(() => {
    if (!router.isReady) return

    console.log('Reset page loaded')
    console.log('Full URL:', typeof window !== 'undefined' ? window.location.href : '')
    console.log('Router query:', router.query)
    console.log('Location hash:', typeof window !== 'undefined' ? window.location.hash : '')

    const processAuth = async () => {
      try {
        // 1) Handle explicit error from URL params first
        const err = router.query.error as string | undefined
        const errDesc = router.query.error_description as string | undefined
        if (err) {
          console.log('Error from URL params:', err, errDesc)
          setMessage(decodeURIComponent(errDesc || 'Recovery link error.'))
          setReady(false)
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
            setMessage(decodeURIComponent(errorDescription || 'Authentication error'))
            setReady(false)
            return
          }
          
          // Handle recovery tokens
          if (access_token && refresh_token && type === 'recovery') {
            console.log('Setting session with recovery tokens')
            const { data, error: sessionError } = await supabase.auth.setSession({
              access_token,
              refresh_token
            })
            
            if (sessionError) {
              console.error('Session error:', sessionError)
              setMessage('Failed to authenticate. Please request a new reset link.')
              setReady(false)
              return
            }
            
            console.log('Session set successfully:', data)
            setReady(true)
            return
          }
        }

        // 3) Check if there's already a valid session
        const { data: { session }, error: sessionError } = await supabase.auth.getSession()
        console.log('Current session check:', { hasSession: !!session, error: sessionError })
        
        if (session?.user) {
          console.log('Found existing valid session')
          setReady(true)
          return
        }

        // 4) No valid authentication found
        console.log('No valid authentication found')
        setMessage('Invalid or expired reset link. Please request a new password reset.')
        setReady(false)

      } catch (error: any) {
        console.error('Auth processing error:', error)
        setMessage('Authentication failed. Please request a new reset link.')
        setReady(false)
      }
    }

    // Process authentication with a small delay to ensure hash is loaded
    const timer = setTimeout(processAuth, 100)
    return () => clearTimeout(timer)
  }, [router.isReady, router.query, supabase])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setMessage('')
    
    if (password.length < 6) {
      setMessage('Password must be at least 6 characters.')
      return
    }
    if (password !== confirm) {
      setMessage('Passwords do not match.')
      return
    }
    
    try {
      console.log('Attempting to update password')
      const { error } = await supabase.auth.updateUser({ password })
      
      if (error) {
        console.error('Password update error:', error)
        setMessage(error.message)
        return
      }
      
      console.log('Password updated successfully')
      setMessage('Password updated successfully! You can now sign in with your new password.')
      
      // Optionally redirect to home page after success
      setTimeout(() => {
        router.push('/')
      }, 2000)
      
    } catch (err: any) {
      console.error('Update password error:', err)
      setMessage('Failed to update password. Please try again.')
    }
  }

  return (
    <>
      <Head><title>Reset Password - Code Vision</title></Head>
      <div className="min-h-screen flex items-center justify-center p-6 bg-background">
        <div className="w-full max-w-sm space-y-4 border rounded-lg p-6 bg-card shadow-sm">
          <h1 className="text-xl font-semibold text-center">Reset your password</h1>
          
          {!ready ? (
            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                {message || 'Processing reset link...'}
              </p>
              {!message && (
                <div className="mt-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mx-auto"></div>
                </div>
              )}
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <p className="text-sm text-green-600 text-center mb-4">
                ✓ Reset link verified! Enter your new password below.
              </p>
              
              <div className="space-y-2">
                <Label htmlFor="password">New password</Label>
                <Input 
                  id="password" 
                  type="password" 
                  minLength={6} 
                  value={password} 
                  onChange={(e) => setPassword(e.target.value)} 
                  placeholder="Enter new password"
                  required 
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="confirm">Confirm new password</Label>
                <Input 
                  id="confirm" 
                  type="password" 
                  minLength={6} 
                  value={confirm} 
                  onChange={(e) => setConfirm(e.target.value)} 
                  placeholder="Confirm new password"
                  required 
                />
              </div>
              
              {message && (
                <p className={`text-sm text-center ${
                  message.includes('successfully') ? 'text-green-600' : 'text-red-600'
                }`}>
                  {message}
                </p>
              )}
              
              <Button type="submit" className="w-full">
                Update password
              </Button>
            </form>
          )}
          
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
import { useState, FormEvent } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { LogoIcon } from '@/components/logo'
import { useSupabase } from '../pages/_app'
import { AuthModalProps } from '../lib/types'

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')
  const { supabase } = useSupabase()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setMessage('')

    try {
      if (isSignUp) {
        const { error } = await supabase.auth.signUp({
          email,
          password,
        })
        if (error) throw error
        setMessage('Check your email for the confirmation link!')
      } else {
        const { error } = await supabase.auth.signInWithPassword({
          email,
          password,
        })
        if (error) throw error
        onClose()
      }
    } catch (error: any) {
      setMessage(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleGoogleSignIn = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: { redirectTo: window.location.origin }
      })
      if (error) throw error
    } catch (error: any) {
      setMessage(error.message)
    }
  }

  const handleForgotPassword = async () => {
    if (!email) {
      setMessage('Please enter your email to reset your password')
      return
    }
    
    setIsLoading(true)
    setMessage('Checking account...')
    
    try {
      const redirectTo = `${process.env.NEXT_PUBLIC_SITE_URL}/reset-password/`
      const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo })
      
      if (error) {
        // Check if it's because the user has no password (OAuth account)
        if (error.message.includes('User not found') || 
            error.message.includes('not found') ||
            error.message.includes('Invalid email')) {
          setMessage('This email might be associated with a Google account. Try signing in with Google instead, or check if you used a different email address.')
        } else if (error.message.includes('Email rate limit exceeded')) {
          setMessage('Too many reset attempts. Please wait a few minutes before trying again.')
        } else {
          setMessage(error.message)
        }
      } else {
        setMessage('Password reset email sent! Check your inbox and follow the link to reset your password.')
      }
    } catch (error: any) {
      console.error('Reset password error:', error)
      setMessage('If this email has a password, you should receive a reset link. If you signed up with Google, please use the "Continue with Google" button instead.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <div className="bg-card p-8 pb-6">
          <div className="text-center">
            <div className="mx-auto block w-fit">
              <LogoIcon />
            </div>
            <DialogHeader>
              <DialogTitle className="mb-1 mt-4 text-xl font-semibold">
                {isSignUp ? 'Create Account' : 'Sign In to Code Vision'}
              </DialogTitle>
            </DialogHeader>
            <p className="text-sm text-muted-foreground">
              {isSignUp ? 'Welcome! Create an account to get started' : 'Welcome back! Sign in to continue'}
            </p>
          </div>

          <div className="mt-6 space-y-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email" className="block text-sm">
                  Email
                </Label>
                <Input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password" className="text-sm">
                    Password
                  </Label>
                  {!isSignUp && (
                    <Button
                      type="button"
                      variant="link"
                      size="sm"
                      className="h-auto p-0 text-xs"
                      onClick={handleForgotPassword}
                      disabled={isLoading}
                    >
                      Forgot password?
                    </Button>
                  )}
                </div>
                <Input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={6}
                />
              </div>

              {message && (
                <div className={`text-sm ${message.includes('Check your email') ? 'text-green-600' : 'text-red-600'}`}>
                  {message}
                </div>
              )}

              <Button
                type="submit"
                disabled={isLoading}
                className="w-full"
              >
                {isLoading ? 'Loading...' : (isSignUp ? 'Sign Up' : 'Sign In')}
              </Button>
            </form>

            <div className="relative">
              <Separator />
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="bg-background px-2 text-sm text-muted-foreground">Or</span>
              </div>
            </div>

            <Button
              onClick={handleGoogleSignIn}
              variant="outline"
              className="w-full"
            >
              Continue with Google
            </Button>

            <div className="text-center">
              <Button
                onClick={() => setIsSignUp(!isSignUp)}
                variant="link"
                className="text-sm"
              >
                {isSignUp ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
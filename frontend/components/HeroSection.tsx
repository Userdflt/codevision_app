import React from 'react'
import { Button } from '@/components/ui/button'
import { LogoIcon } from './logo'

interface HeroSectionProps {
  onGetStarted?: () => void
}

export default function HeroSection({ onGetStarted }: HeroSectionProps) {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-background via-muted/20 to-background">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10" />
      <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent" />
      
      <div className="container relative mx-auto px-6 py-24 md:py-32">
        <div className="mx-auto max-w-4xl text-center">
          {/* Logo */}
          <div className="mb-8 flex justify-center">
            <div className="flex items-center gap-3">
              <LogoIcon />
              <span className="text-2xl font-bold text-foreground">Code Vision</span>
            </div>
          </div>
          
          {/* Main heading */}
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl md:text-7xl">
            <span className="block">AI-Powered</span>
            <span className="block bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              Building Code
            </span>
            <span className="block">Assistant</span>
          </h1>
          
          {/* Subtitle */}
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-muted-foreground md:text-xl">
            Get instant, accurate answers to complex Australian building code questions. 
            From fire safety requirements to structural specifications, our AI assistant 
            helps you navigate regulations with confidence.
          </p>
          
          {/* Features list */}
          <div className="mt-8 flex flex-wrap justify-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-primary" />
              Building Code of Australia (BCA)
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-primary" />
              Fire Safety Requirements
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-primary" />
              Structural Specifications
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-primary" />
              Accessibility Standards
            </div>
          </div>
          
          {/* CTA Button will be handled by parent component */}
        </div>
      </div>
    </section>
  )
}
import { SupabaseClient, User, Session } from '@supabase/supabase-js'

export interface SupabaseContextType {
  supabase: SupabaseClient
  session: Session | null
  user: User | null
}

export interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
}

export interface LayoutProps {
  children: React.ReactNode
  user?: User | null
  onSignOut?: () => void
}

export interface ChatInterfaceProps {
  userId: string
}

export interface MessageListProps {
  messages: Message[]
  isLoading: boolean
}

export interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  sources?: Source[]
}

export interface Source {
  title: string
  content: string
  url?: string
}

export interface SourceCardProps {
  source: Source
}
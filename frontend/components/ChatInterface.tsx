import { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { v4 as uuidv4 } from 'uuid'
import MessageList from './MessageList'
import { Message, sendChatMessage } from '../lib/api'

interface ChatInterfaceProps {
  userId: string
}

export default function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => uuidv4())
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: uuidv4(),
      content: input.trim(),
      role: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await sendChatMessage({
        content: userMessage.content,
        session_id: sessionId
      })

      const assistantMessage: Message = {
        id: uuidv4(),
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        sources: response.sources,
        agentUsed: response.agent_used
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      
      const errorMessage: Message = {
        id: uuidv4(),
        content: 'I apologize, but I encountered an error processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date(),
        isError: true
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [isLoading])

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-[600px] flex flex-col">
        {/* Chat Header */}
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Building Code Assistant
          </h2>
          <p className="text-sm text-gray-600">
            Ask questions about Australian building codes and regulations
          </p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} isLoading={isLoading} />
        </div>

        {/* Input Form */}
        <div className="p-4 border-t border-gray-200">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about building codes, regulations, or requirements..."
              className="flex-1 resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={2}
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              <PaperAirplaneIcon className="h-5 w-5" />
            </button>
          </form>
          
          {/* Tips */}
          <div className="mt-2 text-xs text-gray-500">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  )
}
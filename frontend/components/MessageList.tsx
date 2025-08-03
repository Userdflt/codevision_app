import { useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism'
import { Message } from '../lib/api'
import LoadingIndicator from './LoadingIndicator'
import SourceCard from './SourceCard'

interface MessageListProps {
  messages: Message[]
  isLoading: boolean
}

export default function MessageList({ messages, isLoading }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <p className="text-lg mb-2">Welcome to Code Vision!</p>
          <p className="text-sm">
            Ask me anything about Australian building codes and regulations.
          </p>
          <div className="mt-4 text-xs space-y-1">
            <p>Try asking:</p>
            <p className="italic">"What is the minimum R-value for Zone 3 walls?"</p>
            <p className="italic">"What are the fire egress requirements for Class 2 buildings?"</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${
            message.role === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`max-w-[80%] rounded-lg px-4 py-3 ${
              message.role === 'user'
                ? 'bg-primary-600 text-white'
                : message.isError
                ? 'bg-red-50 border border-red-200 text-red-700'
                : 'bg-gray-50 border border-gray-200 text-gray-900'
            }`}
          >
            {message.role === 'user' ? (
              <p className="whitespace-pre-wrap">{message.content}</p>
            ) : (
              <div>
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      code({ node, inline, className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || '')
                        return !inline && match ? (
                          <SyntaxHighlighter
                            style={oneDark}
                            language={match[1]}
                            PreTag="div"
                            className="rounded-md"
                            {...props}
                          >
                            {String(children).replace(/\n$/, '')}
                          </SyntaxHighlighter>
                        ) : (
                          <code className={className} {...props}>
                            {children}
                          </code>
                        )
                      },
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                </div>
                
                {/* Agent and Sources Info */}
                {message.agentUsed && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs text-gray-500 mb-2">
                      Answered by: {message.agentUsed.replace('_', ' ').toUpperCase()}
                    </p>
                  </div>
                )}
                
                {/* Sources */}
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs text-gray-600 mb-2 font-medium">
                      Sources:
                    </p>
                    <div className="space-y-2">
                      {message.sources.slice(0, 3).map((source, index) => (
                        <SourceCard key={index} source={source} />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {/* Timestamp */}
            <p className={`text-xs mt-2 ${
              message.role === 'user' ? 'text-primary-100' : 'text-gray-500'
            }`}>
              {message.timestamp.toLocaleTimeString()}
            </p>
          </div>
        </div>
      ))}
      
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-gray-50 border border-gray-200 rounded-lg px-4 py-3">
            <LoadingIndicator />
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  )
}
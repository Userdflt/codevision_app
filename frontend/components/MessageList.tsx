import { useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import SyntaxHighlighter from 'react-syntax-highlighter'
// Removed syntax highlighter styling for compatibility
import LoadingIndicator from './LoadingIndicator'
import SourceCard from './SourceCard'
import { MessageListProps } from '../lib/types'

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
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <div className="text-center">
          <p className="text-lg mb-2">Welcome to Code Vision!</p>
          <p className="text-sm">
            Ask me anything about New Zealand building codes and regulations.
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
            message.type === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`max-w-[80%] rounded-lg px-4 py-3 ${
              message.type === 'user'
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted border border-border text-muted-foreground'
            }`}
          >
            {message.type === 'user' ? (
              <p className="whitespace-pre-wrap">{message.content}</p>
            ) : (
              <div>
                <div className="prose prose-sm max-w-none dark:prose-invert">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      code({ node, inline, className, children, ...props }: any) {
                        const match = /language-(\w+)/.exec(className || '')
                        return !inline && match ? (
                          <SyntaxHighlighter
                            customStyle={{
                              backgroundColor: '#f6f8fa',
                              border: '1px solid #e1e4e8',
                              borderRadius: '6px',
                              padding: '16px'
                            }}
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
                
                {/* Sources */}
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-border">
                    <p className="text-xs text-muted-foreground mb-2 font-medium">
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
              message.type === 'user' ? 'text-primary-foreground/70' : 'text-muted-foreground'
            }`}>
              {message.timestamp.toLocaleTimeString()}
            </p>
          </div>
        </div>
      ))}
      
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-muted border border-border rounded-lg px-4 py-3">
            <LoadingIndicator />
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  )
}
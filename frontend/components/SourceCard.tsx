import { SourceCardProps } from '../lib/types'

export default function SourceCard({ source }: SourceCardProps) {
  return (
    <div className="bg-card border border-border rounded-md p-3 text-xs">
      <div className="flex justify-between items-start mb-2">
        <div className="font-medium text-card-foreground">
          {source.title || 'Building Code Reference'}
        </div>
      </div>
      
      <p className="text-muted-foreground mb-2 line-clamp-3">
        {source.content.substring(0, 150)}
        {source.content.length > 150 && '...'}
      </p>
      
      <div className="flex justify-between text-muted-foreground">
        {source.url && (
          <a 
            href={source.url} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="text-primary hover:underline"
          >
            View Source
          </a>
        )}
      </div>
    </div>
  )
}
interface Source {
  content: string
  similarity_score: number
  metadata: {
    source?: string
    clause_type?: string
    section?: string
    page_number?: number
    document_id?: string
  }
}

interface SourceCardProps {
  source: Source
}

export default function SourceCard({ source }: SourceCardProps) {
  const { metadata } = source

  return (
    <div className="bg-white border border-gray-200 rounded-md p-3 text-xs">
      <div className="flex justify-between items-start mb-2">
        <div className="font-medium text-gray-900">
          {metadata.section || metadata.clause_type || 'Building Code Reference'}
        </div>
        <div className="text-gray-500">
          {Math.round(source.similarity_score * 100)}% match
        </div>
      </div>
      
      <p className="text-gray-700 mb-2 line-clamp-3">
        {source.content.substring(0, 150)}
        {source.content.length > 150 && '...'}
      </p>
      
      <div className="flex justify-between text-gray-500">
        {metadata.source && (
          <span>{metadata.source}</span>
        )}
        {metadata.page_number && (
          <span>Page {metadata.page_number}</span>
        )}
      </div>
    </div>
  )
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Message {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
  sources?: Source[]
  agentUsed?: string
  isError?: boolean
}

export interface Source {
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

export interface ChatRequest {
  content: string
  session_id?: string
}

export interface ChatResponse {
  response: string
  session_id: string
  sources: Source[]
  agent_used?: string
}

export async function sendChatMessage(
  request: ChatRequest,
  accessToken?: string
): Promise<ChatResponse> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }

  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
    method: 'POST',
    headers,
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
  }

  return response.json()
}

export async function endChatSession(
  sessionId: string,
  accessToken?: string
): Promise<void> {
  const headers: HeadersInit = {}

  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/chat/session/${sessionId}`, {
    method: 'DELETE',
    headers,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
  }
}

export async function getHealthStatus(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/health`)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return response.json()
}
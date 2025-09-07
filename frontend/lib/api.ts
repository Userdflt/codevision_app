const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000' // Fallback just in case for dev purposes.

export interface ChatRequest {
  message: string
  session_id?: string
  userId?: string
}

export interface ChatResponse {
  response: string
  session_id: string
  sources?: Array<{
    title: string
    content: string
    url?: string
  }>
}

export interface HealthResponse {
  status: string
  timestamp: string
}

export async function sendChatMessage(request: ChatRequest, accessToken?: string): Promise<ChatResponse> {
  const headers: Record<string, string> = {
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

export async function endChatSession(sessionId: string, accessToken?: string): Promise<void> {
  const headers: Record<string, string> = {}

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

export async function getHealthStatus(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/health`)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return response.json()
}
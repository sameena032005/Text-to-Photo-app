import axios from 'axios'

const STORAGE_KEY = 'ai-photo-api-url'

export function getApiBaseUrl() {
  return localStorage.getItem(STORAGE_KEY) || import.meta.env.VITE_API_URL || 'http://localhost:8000'
}

export function setApiBaseUrl(url) {
  localStorage.setItem(STORAGE_KEY, url.replace(/\/$/, ''))
}

function createClient() {
  return axios.create({
    baseURL: getApiBaseUrl(),
    timeout: 120000,
    headers: { 'Content-Type': 'application/json' },
  })
}

/**
 * POST /generate
 * @param {{ prompt: string, style: string, ratio: string, quality?: string }} payload
 * @returns {Promise<{ image_url: string }>}
 */
export async function generateImage(payload) {
  const client = createClient()
  const { data } = await client.post('/generate', payload)
  return data
}

export async function healthCheck() {
  const client = createClient()
  try {
    const { data } = await client.get('/health')
    return data
  } catch {
    return { status: 'unknown' }
  }
}

export async function getJobStatus(jobId) {
  const client = createClient()
  const { data } = await client.get(`/api/status/${jobId}`)
  return data
}

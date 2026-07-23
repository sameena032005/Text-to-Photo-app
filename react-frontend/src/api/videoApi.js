import axios from 'axios'

const STORAGE_KEY = 'ai-video-api-url'

export function getApiBaseUrl() {
  return localStorage.getItem(STORAGE_KEY) || import.meta.env.VITE_API_URL || 'http://localhost:8000'
}

export function setApiBaseUrl(url) {
  localStorage.setItem(STORAGE_KEY, url.replace(/\/$/, ''))
}

function createClient() {
  return axios.create({
    baseURL: getApiBaseUrl(),
    timeout: 300000,
    headers: { 'Content-Type': 'application/json' },
  })
}

/**
 * POST /generate
 * @param {{ prompt: string, style: string, duration: number, ratio: string, quality?: string }} payload
 * @returns {Promise<{ video_url: string }>}
 */
export async function generateVideo(payload) {
  const client = createClient()
  const { data } = await client.post('/generate', payload)
  return data
}

export async function healthCheck() {
  const client = createClient()
  const { data } = await client.get('/health').catch(() => ({ status: 'unknown' }))
  return data
}

export async function getJobStatus(jobId) {
  const client = createClient()
  const { data } = await client.get(`/api/status/${jobId}`)
  return data
}


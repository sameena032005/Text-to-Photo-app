import { useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

async function pollJobStatus(jobId, onStatus) {
  while (true) {
    await new Promise((r) => setTimeout(r, 2000))
    const { data } = await axios.get(`${API_BASE}/status/${jobId}`)
    if (onStatus) onStatus(data.message || 'Processing...')
    if (data.status === 'done') {
      return data.videoUrl || data.video_url
    }
    if (data.status === 'error') {
      throw new Error(data.message || 'Generation failed on server.')
    }
  }
}

export default function App() {
  const [prompt, setPrompt] = useState('')
  const [videoUrl, setVideoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [statusMsg, setStatusMsg] = useState('')
  const [error, setError] = useState('')

  const generateVideo = async () => {
    if (!prompt.trim()) { setError('Please enter a prompt first.'); return }
    setLoading(true)
    setError('')
    setVideoUrl('')
    setStatusMsg('Sending request...')

    try {
      const res = await axios.post(`${API_BASE}/generate`, {
        prompt, style: 'Cinematic', duration: 10, ratio: '16:9'
      })
      console.log('Initial response:', res.data)

      let finalUrl = null

      if (res.data.video_url) {
        // ✅ ComfyUI / FastAPI backend: returns video_url directly
        const raw = res.data.video_url
        finalUrl = raw.startsWith('http') ? raw : `${API_BASE}${raw}`
        setStatusMsg('Video ready!')
      } else if (res.data.jobId || res.data.job_id) {
        // ✅ Flask backend: returns jobId — poll until done
        const jobId = res.data.jobId || res.data.job_id
        setStatusMsg('Job started, processing...')
        finalUrl = await pollJobStatus(jobId, setStatusMsg)
        if (finalUrl && !finalUrl.startsWith('http')) {
          finalUrl = `${API_BASE}${finalUrl}`
        }
      } else if (res.data.error) {
        throw new Error(res.data.error)
      } else {
        throw new Error('Unexpected response from server. Check backend logs.')
      }

      if (!finalUrl) throw new Error('Server returned no video URL.')
      setVideoUrl(finalUrl)
      setStatusMsg('')
    } catch (err) {
      const msg = err.response?.data?.error || err.response?.data?.message || err.message || 'Unknown error'
      setError(msg)
      setStatusMsg('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold mb-8">🎬 AI Text to Video</h1>

        <div className="bg-gray-800/50 rounded-2xl p-8 mb-8">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your video... e.g. 'a sunset over the ocean'"
            disabled={loading}
            className="w-full h-32 bg-gray-900 border border-gray-600 rounded-lg p-4 text-white placeholder-gray-500 focus:border-purple-500 focus:outline-none resize-none"
          />

          <button
            onClick={generateVideo}
            disabled={loading}
            className="mt-6 w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 py-3 rounded-lg font-semibold transition-all"
          >
            {loading ? '⏳ Generating...' : '✨ Generate Video'}
          </button>
        </div>

        {/* Status message while generating */}
        {loading && statusMsg && (
          <div className="bg-blue-900/30 border border-blue-700 rounded-lg p-4 mb-6 text-blue-200 flex items-center gap-3">
            <span className="animate-spin text-xl">⚙️</span>
            <span>{statusMsg}</span>
          </div>
        )}

        {/* Error display */}
        {error && (
          <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-6 text-red-200">
            ❌ {error}
          </div>
        )}

        {/* Result display */}
        {videoUrl && (
          <div className="bg-gray-800/50 rounded-2xl overflow-hidden">
            <div className="aspect-video bg-black flex items-center justify-center">
              {/\.(png|jpg|jpeg|gif|webp)(\?|$)/i.test(videoUrl) ? (
                <img
                  src={videoUrl}
                  alt="AI Generated"
                  className="w-full h-full object-contain"
                  onError={() => setError('Failed to load the generated image. The file may not exist yet.')}
                />
              ) : (
                <video
                  src={videoUrl}
                  controls
                  autoPlay
                  playsInline
                  className="w-full h-full object-contain"
                  onError={() => setError('Failed to load the generated video. The file may not exist yet.')}
                />
              )}
            </div>
            <div className="p-4 flex gap-4">
              <button
                onClick={() => { setVideoUrl(''); setError(''); }}
                className="flex-1 bg-gray-700 hover:bg-gray-600 py-2 rounded font-semibold transition-colors"
              >
                Clear
              </button>
              <button
                onClick={generateVideo}
                disabled={loading}
                className="flex-1 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 py-2 rounded font-semibold transition-colors"
              >
                Regenerate
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
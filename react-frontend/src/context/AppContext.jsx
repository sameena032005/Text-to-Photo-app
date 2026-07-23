import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { generateImage as apiGenerate, getJobStatus } from '../api/photoApi'

const AppContext = createContext(null)

const HISTORY_KEY = 'ai-photo-history'
const SETTINGS_KEY = 'ai-photo-settings'

const defaultSettings = {
  theme: 'dark',
  defaultStyle: 'Cinematic',
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
}

function loadSettings() {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    return raw ? { ...defaultSettings, ...JSON.parse(raw) } : defaultSettings
  } catch {
    return defaultSettings
  }
}

function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function applyUrlApiOverride() {
  try {
    const api = new URLSearchParams(window.location.search).get('api')
    if (api) {
      const saved = loadSettings()
      const next = { ...saved, apiUrl: api.replace(/\/$/, '') }
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(next))
      localStorage.setItem('ai-photo-api-url', next.apiUrl)
      return next
    }
  } catch {
    /* ignore */
  }
  return null
}

export function AppProvider({ children }) {
  const urlSettings = applyUrlApiOverride()
  const [settings, setSettings] = useState(urlSettings || loadSettings)
  const [history, setHistory] = useState(loadHistory)
  const [activeSection, setActiveSection] = useState('home')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const [prompt, setPrompt] = useState('a beautiful mountain landscape at sunset')
  const [style, setStyle] = useState(settings.defaultStyle)
  const [ratio, setRatio] = useState('1:1')
  const [quality, setQuality] = useState('High')

  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [imageUrl, setImageUrl] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    document.documentElement.classList.toggle('light', settings.theme === 'light')
    document.documentElement.classList.toggle('dark', settings.theme === 'dark')
  }, [settings.theme])

  useEffect(() => {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
    localStorage.setItem('ai-photo-api-url', settings.apiUrl.replace(/\/$/, ''))
  }, [settings])

  useEffect(() => {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history))
  }, [history])

  const addToHistory = useCallback((entry) => {
    setHistory((prev) => [entry, ...prev].slice(0, 50))
  }, [])

  const generate = useCallback(async () => {
    if (!prompt.trim() || isGenerating) return

    setIsGenerating(true)
    setError(null)
    setImageUrl(null)
    setProgress(0)

    const progressInterval = setInterval(() => {
      setProgress((p) => Math.min(p + Math.random() * 12, 90))
    }, 600)

    try {
      const payload = {
        prompt: prompt.trim(),
        style,
        ratio,
        quality: quality.toLowerCase(),
      }

      const result = await apiGenerate(payload)
      let finalUrl = null

      if (result.image_url || result.video_url) {
        const raw = result.image_url || result.video_url
        finalUrl = raw.startsWith('/') ? `${settings.apiUrl.replace(/\/$/, '')}${raw}` : raw
      } else if (result.jobId || result.job_id) {
        const jobId = result.jobId || result.job_id
        let jobDone = false
        while (!jobDone) {
          await new Promise((resolve) => setTimeout(resolve, 2000))
          const jobData = await getJobStatus(jobId)
          if (jobData.status === 'done') {
            finalUrl = jobData.imageUrl || jobData.image_url || jobData.videoUrl || jobData.video_url
            jobDone = true
          } else if (jobData.status === 'error') {
            throw new Error(jobData.message || 'Generation failed on backend.')
          }
        }
      } else {
        throw new Error('Invalid backend response: missing image_url or jobId.')
      }

      setProgress(100)
      setImageUrl(finalUrl)

      addToHistory({
        id: Date.now().toString() + Math.random().toString(36),
        prompt: prompt.trim(),
        style,
        ratio,
        quality,
        imageUrl: finalUrl,
        thumbnail: finalUrl,
        createdAt: new Date().toISOString(),
      })
    } catch (err) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.detail ||
        err.message ||
        'Failed to generate image. Please check your backend connection.'
      setError(message)
    } finally {
      clearInterval(progressInterval)
      setIsGenerating(false)
    }
  }, [prompt, style, ratio, quality, isGenerating, addToHistory, settings.apiUrl])

  const retry = useCallback(() => {
    setError(null)
    generate()
  }, [generate])

  const openHistoryItem = useCallback((item) => {
    setPrompt(item.prompt)
    setStyle(item.style || settings.defaultStyle)
    setRatio(item.ratio || '1:1')
    setQuality(item.quality || 'High')
    setImageUrl(item.imageUrl)
    setActiveSection('generate')
    setError(null)
  }, [settings])

  const updateSettings = useCallback((partial) => {
    setSettings((s) => {
      const next = { ...s, ...partial }
      if (partial.defaultStyle != null) setStyle(partial.defaultStyle)
      return next
    })
  }, [])

  const toggleTheme = useCallback(() => {
    setSettings((s) => ({ ...s, theme: s.theme === 'dark' ? 'light' : 'dark' }))
  }, [])

  const value = useMemo(
    () => ({
      settings,
      updateSettings,
      toggleTheme,
      history,
      activeSection,
      setActiveSection,
      sidebarOpen,
      setSidebarOpen,
      prompt,
      setPrompt,
      style,
      setStyle,
      ratio,
      setRatio,
      quality,
      setQuality,
      isGenerating,
      progress,
      imageUrl,
      setImageUrl,
      // keep videoUrl alias so VideoPlayer still works
      videoUrl: imageUrl,
      setVideoUrl: setImageUrl,
      error,
      setError,
      generate,
      retry,
      openHistoryItem,
    }),
    [
      settings,
      updateSettings,
      toggleTheme,
      history,
      activeSection,
      sidebarOpen,
      prompt,
      style,
      ratio,
      quality,
      isGenerating,
      progress,
      imageUrl,
      error,
      generate,
      retry,
      openHistoryItem,
    ],
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}

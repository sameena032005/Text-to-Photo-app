import { motion } from 'framer-motion'
import { Download, RefreshCw, Share2 } from 'lucide-react'
import { useState } from 'react'
import { useApp } from '../context/AppContext'

/** Detect if running inside the Flutter WebView shell */
function isFlutter() {
  return typeof window !== 'undefined' &&
    (typeof window.FlutterDownload !== 'undefined' ||
     typeof window.FlutterShare !== 'undefined')
}

export default function VideoPlayer() {
  const { videoUrl, generate, isGenerating, prompt, settings } = useApp()
  const isDark = settings.theme === 'dark'
  const [toast, setToast] = useState('')

  if (!videoUrl) return null

  const isVideo = /\.(mp4|webm|mov)(\?|$)/i.test(videoUrl)
  const ext = isVideo ? 'mp4' : 'png'
  const fileName = `ai-photo-${Date.now()}.${ext}`

  function showToast(msg) {
    setToast(msg)
    setTimeout(() => setToast(''), 3000)
  }

  // ── Download ────────────────────────────────────────────────────────────────
  async function handleDownload() {
    if (isFlutter()) {
      // Hand off to Flutter — saves to Pictures/AIPhotoGenerator on device
      window.FlutterDownload.postMessage(videoUrl)
      return
    }

    // Web fallback: fetch as blob so browser triggers Save dialog
    try {
      const resp = await fetch(videoUrl)
      const blob = await resp.blob()
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href     = url
      a.download = fileName
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
      showToast('Download started!')
    } catch {
      // Fallback to direct link if CORS blocks fetch
      const a    = document.createElement('a')
      a.href     = videoUrl
      a.download = fileName
      a.target   = '_blank'
      a.click()
    }
  }

  // ── Share ───────────────────────────────────────────────────────────────────
  async function handleShare() {
    if (isFlutter()) {
      // Hand off to Flutter — opens native Android share sheet with ALL apps
      window.FlutterShare.postMessage(videoUrl)
      return
    }

    // Web: use Web Share API (mobile browsers) or clipboard fallback
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AI Generated Photo',
          text: `Check out this AI photo I created: "${prompt}"`,
          url: videoUrl,
        })
      } catch {
        /* user cancelled */
      }
    } else {
      try {
        await navigator.clipboard.writeText(videoUrl)
        showToast('Image URL copied to clipboard!')
      } catch {
        showToast('Share not supported in this browser.')
      }
    }
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      className={`overflow-hidden rounded-2xl shadow-2xl ${
        isDark ? 'bg-ai-card shadow-black/40' : 'bg-white shadow-gray-200/80'
      }`}
    >
      {/* Image / Video */}
      <div className="relative w-full bg-black" style={{ minHeight: '300px' }}>
        {isVideo ? (
          <video
            src={videoUrl}
            controls
            autoPlay
            playsInline
            className="h-full w-full object-contain"
          >
            <track kind="captions" />
          </video>
        ) : (
          <img
            src={videoUrl}
            alt="AI Generated Photo"
            className="mx-auto block max-h-[600px] w-full object-contain"
          />
        )}
      </div>

      {/* Toast notification */}
      {toast && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="mx-4 mt-3 rounded-xl bg-violet-600/20 border border-violet-500/30 px-4 py-2.5 text-sm text-violet-300 text-center"
        >
          {toast}
        </motion.div>
      )}

      {/* Action buttons */}
      <div className="flex flex-wrap gap-3 p-4 sm:p-6">
        <ActionButton
          icon={Download}
          label="Download"
          onClick={handleDownload}
          isDark={isDark}
        />
        <ActionButton
          icon={Share2}
          label="Share"
          onClick={handleShare}
          isDark={isDark}
        />
        <ActionButton
          icon={RefreshCw}
          label="Regenerate"
          onClick={generate}
          disabled={isGenerating}
          primary
        />
      </div>
    </motion.section>
  )
}

function ActionButton({ icon: Icon, label, onClick, disabled, primary, isDark }) {
  return (
    <motion.button
      type="button"
      whileHover={{ scale: disabled ? 1 : 1.03 }}
      whileTap={{ scale: disabled ? 1 : 0.97 }}
      onClick={onClick}
      disabled={disabled}
      className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition disabled:opacity-50 ${
        primary
          ? 'gradient-btn text-white shadow-md'
          : isDark
            ? 'border border-ai-border bg-ai-surface text-white hover:bg-ai-card'
            : 'border border-gray-200 bg-gray-50 text-gray-800 hover:bg-gray-100'
      }`}
    >
      <Icon className="h-4 w-4" />
      {label}
    </motion.button>
  )
}

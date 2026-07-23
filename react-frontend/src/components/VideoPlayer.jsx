import { motion } from 'framer-motion'
import { Download, RefreshCw, Share2 } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function VideoPlayer() {
  const { videoUrl, generate, isGenerating, prompt, settings } = useApp()
  const isDark = settings.theme === 'dark'

  if (!videoUrl) return null

  const isVideo = /\.(mp4|webm|mov)(\?|$)/i.test(videoUrl)
  const ext = isVideo ? 'mp4' : 'png'

  const handleDownload = () => {
    const a = document.createElement('a')
    a.href = videoUrl
    a.download = `ai-photo-${Date.now()}.${ext}`
    a.target = '_blank'
    a.rel = 'noopener noreferrer'
    a.click()
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({ title: 'AI Generated Photo', text: prompt, url: videoUrl })
      } catch {
        /* user cancelled */
      }
    } else {
      await navigator.clipboard.writeText(videoUrl)
      alert('Image URL copied to clipboard!')
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

      <div className="flex flex-wrap gap-3 p-4 sm:p-6">
        <ActionButton icon={Download} label="Download" onClick={handleDownload} isDark={isDark} />
        <ActionButton icon={Share2} label="Share" onClick={handleShare} isDark={isDark} />
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

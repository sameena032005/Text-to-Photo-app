import { motion } from 'framer-motion'
import { AlertCircle, RotateCcw } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function ErrorBanner() {
  const { error, retry, setError, settings } = useApp()
  const isDark = settings.theme === 'dark'

  if (!error) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex flex-col gap-4 rounded-2xl border p-5 sm:flex-row sm:items-center sm:justify-between ${
        isDark
          ? 'border-red-500/30 bg-red-500/10'
          : 'border-red-200 bg-red-50'
      }`}
      role="alert"
    >
      <div className="flex gap-3">
        <AlertCircle className="h-5 w-5 shrink-0 text-red-400" />
        <div>
          <p className={`font-medium ${isDark ? 'text-red-200' : 'text-red-800'}`}>
            Generation failed
          </p>
          <p className={`mt-1 text-sm ${isDark ? 'text-red-300/80' : 'text-red-700'}`}>
            {error}
          </p>
        </div>
      </div>
      <div className="flex gap-2">
        <motion.button
          type="button"
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          onClick={retry}
          className="inline-flex items-center gap-2 rounded-xl bg-red-500 px-4 py-2 text-sm font-medium text-white hover:bg-red-600"
        >
          <RotateCcw className="h-4 w-4" />
          Retry
        </motion.button>
        <button
          type="button"
          onClick={() => setError(null)}
          className={`rounded-xl px-4 py-2 text-sm font-medium ${
            isDark ? 'text-ai-muted hover:text-white' : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Dismiss
        </button>
      </div>
    </motion.div>
  )
}

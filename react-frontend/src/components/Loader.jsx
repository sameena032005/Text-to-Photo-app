import { motion } from 'framer-motion'
import { ImageIcon } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function Loader() {
  const { isGenerating, progress, settings } = useApp()
  const isDark = settings.theme === 'dark'

  if (!isGenerating) return null

  const remaining = Math.max(0, Math.round(15 * (1 - progress / 100)))

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0 }}
      className={`glass-card rounded-2xl p-6 sm:p-8 ${isDark ? '' : 'bg-white'}`}
    >
      <div className="flex flex-col items-center text-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          className="gradient-btn mb-6 flex h-16 w-16 items-center justify-center rounded-2xl shadow-lg"
        >
          <ImageIcon className="h-8 w-8 text-white" />
        </motion.div>

        <h3 className={`mb-2 text-xl font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
          Creating your photo...
        </h3>
        <p className={`mb-6 text-sm ${isDark ? 'text-ai-muted' : 'text-gray-500'}`}>
          {remaining > 0 ? `About ${remaining}s remaining` : 'Almost done...'}
        </p>

        <div className="w-full max-w-md">
          <div className={`mb-2 h-2 overflow-hidden rounded-full ${isDark ? 'bg-ai-border' : 'bg-gray-200'}`}>
            <motion.div
              className="gradient-btn h-full rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ ease: 'easeOut' }}
            />
          </div>
          <p className={`text-right text-xs ${isDark ? 'text-ai-muted' : 'text-gray-500'}`}>
            {Math.round(progress)}%
          </p>
        </div>

        <div className="mt-6 flex gap-1.5">
          {[0, 1, 2].map((i) => (
            <motion.span
              key={i}
              className="h-2 w-2 rounded-full bg-violet-500"
              animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1.2, 0.8] }}
              transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  )
}

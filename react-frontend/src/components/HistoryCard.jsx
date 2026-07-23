import { motion } from 'framer-motion'
import { ExternalLink, ImageIcon } from 'lucide-react'
import { useApp } from '../context/AppContext'

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return iso
  }
}

export default function HistoryCard({ item, index = 0 }) {
  const { openHistoryItem, settings } = useApp()
  const isDark = settings.theme === 'dark'

  const thumbUrl = item.imageUrl || item.videoUrl || item.thumbnail

  return (
    <motion.article
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      whileHover={{ y: -4 }}
      className={`glass-card flex flex-col overflow-hidden rounded-2xl sm:flex-row ${isDark ? '' : 'bg-white'}`}
    >
      {/* Thumbnail */}
      <div className="relative aspect-square w-full shrink-0 bg-black sm:w-40 md:w-48">
        {thumbUrl ? (
          <img
            src={thumbUrl}
            alt={item.prompt}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center">
            <ImageIcon className={`h-10 w-10 ${isDark ? 'text-ai-muted' : 'text-gray-400'}`} />
          </div>
        )}
      </div>

      <div className="flex flex-1 flex-col justify-between gap-3 p-4 sm:p-5">
        <div>
          <p className={`line-clamp-2 text-sm font-medium leading-relaxed ${isDark ? 'text-white' : 'text-gray-900'}`}>
            {item.prompt}
          </p>
          <p className={`mt-2 text-xs ${isDark ? 'text-ai-muted' : 'text-gray-500'}`}>
            {formatDate(item.createdAt)}
            {item.style && ` · ${item.style}`}
            {item.ratio && ` · ${item.ratio}`}
          </p>
        </div>

        <motion.button
          type="button"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => openHistoryItem(item)}
          className={`inline-flex w-fit items-center gap-2 rounded-xl px-4 py-2 text-sm font-medium ${
            isDark
              ? 'bg-ai-card text-violet-300 hover:bg-ai-border'
              : 'bg-violet-50 text-violet-700 hover:bg-violet-100'
          }`}
        >
          <ExternalLink className="h-4 w-4" />
          Open
        </motion.button>
      </div>
    </motion.article>
  )
}

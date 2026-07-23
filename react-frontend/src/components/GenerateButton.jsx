import { motion } from 'framer-motion'
import { ImageIcon, Loader2 } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function GenerateButton({ className = '' }) {
  const { generate, isGenerating, prompt } = useApp()
  const disabled = isGenerating || !prompt.trim()

  return (
    <motion.button
      type="button"
      onClick={generate}
      disabled={disabled}
      whileHover={disabled ? {} : { scale: 1.02, y: -2 }}
      whileTap={disabled ? {} : { scale: 0.98 }}
      className={`gradient-btn flex w-full items-center justify-center gap-3 rounded-2xl px-8 py-4 text-lg font-semibold text-white shadow-xl shadow-indigo-500/30 transition disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-none ${className}`}
    >
      {isGenerating ? (
        <>
          <Loader2 className="h-6 w-6 animate-spin" />
          Generating photo...
        </>
      ) : (
        <>
          <ImageIcon className="h-6 w-6" />
          Generate Photo
        </>
      )}
    </motion.button>
  )
}

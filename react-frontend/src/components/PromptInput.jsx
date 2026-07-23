import { motion } from 'framer-motion'
import { Wand2 } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function PromptInput({ large = false }) {
  const { prompt, setPrompt, isGenerating, settings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.15 }}
      className="w-full"
    >
      <label
        htmlFor="prompt"
        className={`mb-2 flex items-center gap-2 text-sm font-medium ${
          isDark ? 'text-ai-muted' : 'text-gray-600'
        }`}
      >
        <Wand2 className="h-4 w-4 text-violet-400" />
        Your prompt
      </label>
      <textarea
        id="prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        disabled={isGenerating}
        rows={large ? 4 : 3}
        placeholder="Example: A futuristic city at sunset, cinematic lighting, ultra realistic"
        className={`w-full resize-none rounded-2xl border px-5 py-4 text-base transition-all outline-none focus:ring-2 focus:ring-violet-500/40 ${
          large ? 'min-h-[140px] text-lg sm:min-h-[160px]' : 'min-h-[100px]'
        } ${
          isDark
            ? 'border-ai-border bg-ai-card text-white placeholder:text-ai-muted/70'
            : 'border-gray-200 bg-white text-gray-900 placeholder:text-gray-400'
        } disabled:cursor-not-allowed disabled:opacity-60`}
      />
      <p className={`mt-2 text-xs ${isDark ? 'text-ai-muted' : 'text-gray-500'}`}>
        {prompt.length} characters
      </p>
    </motion.div>
  )
}

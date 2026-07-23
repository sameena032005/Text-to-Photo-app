import { AnimatePresence, motion } from 'framer-motion'
import { History, ImageIcon } from 'lucide-react'
import ErrorBanner from '../components/ErrorBanner'
import GenerateButton from '../components/GenerateButton'
import HistoryCard from '../components/HistoryCard'
import Loader from '../components/Loader'
import PromptInput from '../components/PromptInput'
import StyleSelector from '../components/StyleSelector'
import VideoPlayer from '../components/VideoPlayer'
import { useApp } from '../context/AppContext'
import Settings from './Settings'

function HeroSection() {
  const { settings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative mb-10 text-center"
    >
      <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/2 top-0 h-64 w-96 -translate-x-1/2 rounded-full bg-violet-600/20 blur-[100px]" />
        <div className="absolute right-0 top-20 h-48 w-48 rounded-full bg-blue-600/15 blur-[80px]" />
      </div>

      <motion.h1
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className={`font-display text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl lg:text-6xl ${
          isDark ? 'text-white' : 'text-gray-900'
        }`}
      >
        Generate Stunning{' '}
        <span className="gradient-text">AI Photos</span> from Text
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className={`mx-auto mt-4 max-w-2xl text-base sm:text-lg ${
          isDark ? 'text-ai-muted' : 'text-gray-600'
        }`}
      >
        Turn your imagination into stunning photos using AI — just describe what you want
      </motion.p>
    </motion.section>
  )
}

function GeneratePanel() {
  const { settings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="space-y-6"
    >
      <div className={`glass-card rounded-2xl p-5 sm:p-8 ${isDark ? '' : 'bg-white'}`}>
        <PromptInput large />
      </div>

      <div className={`glass-card space-y-6 rounded-2xl p-5 sm:p-8 ${isDark ? '' : 'bg-white'}`}>
        <h2 className={`font-display text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
          Generation options
        </h2>
        <StyleSelector />
      </div>

      <ErrorBanner />

      <GenerateButton />

      <AnimatePresence mode="wait">
        <Loader key="loader" />
      </AnimatePresence>

      <VideoPlayer />
    </motion.div>
  )
}

function HistorySection() {
  const { history, settings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <motion.section
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div className="flex items-center gap-3">
        <History className="h-6 w-6 text-violet-400" />
        <h2 className={`font-display text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
          Generation history
        </h2>
      </div>

      {history.length === 0 ? (
        <div className={`rounded-2xl border border-dashed p-12 text-center ${
          isDark ? 'border-ai-border text-ai-muted' : 'border-gray-200 text-gray-500'
        }`}>
          <ImageIcon className="mx-auto mb-3 h-10 w-10 opacity-30" />
          <p>No photos yet. Generate your first AI photo above.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {history.map((item, i) => (
            <HistoryCard key={item.id} item={item} index={i} />
          ))}
        </div>
      )}
    </motion.section>
  )
}

export default function Home() {
  const { activeSection, setActiveSection, settings } = useApp()
  const isDark = settings.theme === 'dark'
  const bg = isDark ? 'bg-ai-black text-white' : 'bg-gray-50 text-gray-900'

  return (
    <div className={`min-h-full ${bg}`}>
      <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 sm:py-12 lg:max-w-5xl">
        {activeSection === 'home' && (
          <>
            <HeroSection />
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className={`mb-10 rounded-2xl border p-8 text-center ${
                isDark ? 'border-ai-border bg-ai-surface/50' : 'border-gray-200 bg-white'
              }`}
            >
              <div className="mb-4 flex justify-center">
                <div className="gradient-btn flex h-14 w-14 items-center justify-center rounded-2xl shadow-lg shadow-indigo-500/20">
                  <ImageIcon className="h-7 w-7 text-white" />
                </div>
              </div>
              <h2 className={`mb-2 font-display text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Your AI Photo Studio
              </h2>
              <p className={`mb-6 ${isDark ? 'text-ai-muted' : 'text-gray-600'}`}>
                Describe any scene, style, or concept and watch AI bring it to life as a stunning photo.
              </p>
              <motion.button
                type="button"
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => setActiveSection('generate')}
                className="gradient-btn rounded-xl px-8 py-3 font-semibold text-white shadow-lg"
              >
                Start generating
              </motion.button>
            </motion.div>

            {/* Feature highlights */}
            <div className="grid gap-4 sm:grid-cols-3">
              {[
                { emoji: '✨', title: 'Any Style', desc: 'Cinematic, Anime, Realistic, Oil Painting and more' },
                { emoji: '⚡', title: 'Fast Generation', desc: 'High-quality images ready in seconds' },
                { emoji: '🎨', title: 'Full Control', desc: 'Choose aspect ratio, quality, and style' },
              ].map((f) => (
                <div
                  key={f.title}
                  className={`rounded-2xl border p-5 ${
                    isDark ? 'border-ai-border bg-ai-surface/30' : 'border-gray-200 bg-white'
                  }`}
                >
                  <div className="mb-2 text-2xl">{f.emoji}</div>
                  <h3 className={`mb-1 font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>{f.title}</h3>
                  <p className={`text-sm ${isDark ? 'text-ai-muted' : 'text-gray-500'}`}>{f.desc}</p>
                </div>
              ))}
            </div>
          </>
        )}

        {activeSection === 'generate' && (
          <>
            <HeroSection />
            <GeneratePanel />
          </>
        )}

        {activeSection === 'history' && <HistorySection />}
        {activeSection === 'settings' && <Settings />}
      </div>
    </div>
  )
}

import { AnimatePresence, motion } from 'framer-motion'
import {
  History,
  Home,
  ImageIcon,
  Settings,
  Sparkles,
  X,
} from 'lucide-react'
import { useApp } from '../context/AppContext'
import { NAV_ITEMS } from '../utils/constants'

const iconMap = {
  home: Home,
  sparkles: Sparkles,
  history: History,
  settings: Settings,
}

export default function Sidebar() {
  const { settings, activeSection, setActiveSection, sidebarOpen, setSidebarOpen } =
    useApp()
  const isDark = settings.theme === 'dark'

  const nav = (
    <nav className="flex flex-1 flex-col gap-1 p-4">
      {NAV_ITEMS.map((item) => {
        const Icon = iconMap[item.icon]
        const active = activeSection === item.id
        return (
          <motion.button
            key={item.id}
            type="button"
            whileHover={{ x: 4 }}
            onClick={() => {
              setActiveSection(item.id)
              setSidebarOpen(false)
            }}
            className={`flex items-center gap-3 rounded-xl px-4 py-3 text-left text-sm font-medium transition-all ${
              active
                ? 'gradient-btn text-white shadow-lg shadow-indigo-500/25'
                : isDark
                  ? 'text-ai-muted hover:bg-ai-card hover:text-white'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            }`}
          >
            <Icon className="h-5 w-5 shrink-0" />
            {item.label}
          </motion.button>
        )
      })}
    </nav>
  )

  return (
    <>
      {/* Desktop sidebar */}
      <aside
        className={`hidden w-64 shrink-0 flex-col border-r lg:flex ${
          isDark ? 'border-ai-border bg-ai-surface' : 'border-gray-200 bg-white'
        }`}
      >
        <div className="flex items-center gap-2 border-b border-inherit px-5 py-5">
          <div className="gradient-btn flex h-8 w-8 items-center justify-center rounded-lg">
            <ImageIcon className="h-4 w-4 text-white" />
          </div>
          <span className={`font-display font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
            AI Photos
          </span>
        </div>
        {nav}
      </aside>

      {/* Mobile drawer */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm lg:hidden"
              onClick={() => setSidebarOpen(false)}
            />
            <motion.aside
              initial={{ x: -280 }}
              animate={{ x: 0 }}
              exit={{ x: -280 }}
              transition={{ type: 'spring', damping: 28, stiffness: 320 }}
              className={`fixed inset-y-0 left-0 z-50 flex w-72 flex-col shadow-2xl lg:hidden ${
                isDark ? 'bg-ai-surface' : 'bg-white'
              }`}
            >
              <div className="flex items-center justify-between border-b border-inherit px-4 py-4">
                <span className={`font-display font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  Menu
                </span>
                <button
                  type="button"
                  onClick={() => setSidebarOpen(false)}
                  className={`rounded-lg p-2 ${isDark ? 'text-ai-muted hover:bg-ai-card' : 'text-gray-500'}`}
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              {nav}
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  )
}

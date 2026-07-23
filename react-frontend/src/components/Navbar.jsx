import { motion } from 'framer-motion'
import { ImageIcon, LogOut, Menu, Moon, Sun, User } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useApp } from '../context/AppContext'

export default function Navbar() {
  const { settings, toggleTheme, setSidebarOpen } = useApp()
  const { user, logout } = useAuth()
  const isDark = settings.theme === 'dark'
  const [dropdownOpen, setDropdownOpen] = useState(false)

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className={`sticky top-0 z-40 border-b ${
        isDark
          ? 'border-ai-border/60 bg-ai-black/80 backdrop-blur-xl'
          : 'border-gray-200 bg-white/80 backdrop-blur-xl'
      }`}
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">

        {/* Left: hamburger + logo */}
        <div className="flex items-center gap-3">
          {user && (
            <button
              type="button"
              onClick={() => setSidebarOpen(true)}
              className={`rounded-lg p-2 lg:hidden ${
                isDark ? 'text-ai-muted hover:bg-ai-card' : 'text-gray-600 hover:bg-gray-100'
              }`}
              aria-label="Open menu"
            >
              <Menu className="h-5 w-5" />
            </button>
          )}

          <div className="flex items-center gap-2.5">
            <div className="gradient-btn flex h-9 w-9 items-center justify-center rounded-xl shadow-lg shadow-indigo-500/20">
              <ImageIcon className="h-5 w-5 text-white" />
            </div>
            <span
              className={`font-display text-lg font-semibold tracking-tight sm:text-xl ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}
            >
              AI Photo Generator
            </span>
          </div>
        </div>

        {/* Right: theme + auth */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Theme toggle */}
          <motion.button
            type="button"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleTheme}
            className={`rounded-xl p-2.5 transition-colors ${
              isDark
                ? 'bg-ai-card text-ai-muted hover:text-white'
                : 'bg-gray-100 text-gray-600 hover:text-gray-900'
            }`}
            aria-label="Toggle theme"
          >
            {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </motion.button>

          {user ? (
            /* Logged-in: user avatar + dropdown */
            <div className="relative">
              <motion.button
                type="button"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setDropdownOpen((v) => !v)}
                className={`flex h-10 items-center gap-2 rounded-full border px-3 ${
                  isDark
                    ? 'border-ai-border bg-ai-card text-white'
                    : 'border-gray-200 bg-gray-50 text-gray-900'
                }`}
                aria-label="User menu"
              >
                <div className="gradient-btn flex h-6 w-6 items-center justify-center rounded-full">
                  <User className="h-3.5 w-3.5 text-white" />
                </div>
                <span className="hidden text-sm font-medium sm:block max-w-[120px] truncate">
                  {user.name}
                </span>
              </motion.button>

              {dropdownOpen && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setDropdownOpen(false)}
                  />
                  <motion.div
                    initial={{ opacity: 0, y: -8, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0 }}
                    className={`absolute right-0 z-20 mt-2 w-52 rounded-2xl border p-2 shadow-xl ${
                      isDark
                        ? 'border-ai-border bg-ai-surface'
                        : 'border-gray-200 bg-white'
                    }`}
                  >
                    <div className={`px-3 py-2 border-b mb-1 ${isDark ? 'border-ai-border' : 'border-gray-100'}`}>
                      <p className={`text-sm font-medium truncate ${isDark ? 'text-white' : 'text-gray-900'}`}>
                        {user.name}
                      </p>
                      <p className="text-xs text-ai-muted truncate">{user.email}</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => { setDropdownOpen(false); logout() }}
                      className={`flex w-full items-center gap-2.5 rounded-xl px-3 py-2.5 text-sm transition-colors ${
                        isDark
                          ? 'text-ai-muted hover:bg-ai-card hover:text-red-400'
                          : 'text-gray-600 hover:bg-gray-100 hover:text-red-500'
                      }`}
                    >
                      <LogOut className="h-4 w-4" />
                      Sign out
                    </button>
                  </motion.div>
                </>
              )}
            </div>
          ) : (
            /* Logged-out: Login + Signup buttons */
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className={`rounded-xl px-4 py-2 text-sm font-medium transition-colors ${
                  isDark
                    ? 'text-ai-muted hover:bg-ai-card hover:text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Sign in
              </Link>
              <Link
                to="/signup"
                className="gradient-btn rounded-xl px-4 py-2 text-sm font-semibold text-white shadow-md shadow-indigo-500/20 transition hover:opacity-90"
              >
                Sign up
              </Link>
            </div>
          )}
        </div>
      </div>
    </motion.header>
  )
}

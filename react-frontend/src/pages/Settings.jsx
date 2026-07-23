import { motion } from 'framer-motion'
import { Globe, Palette, Sliders } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { IMAGE_STYLES } from '../utils/constants'

export default function Settings() {
  const { settings, updateSettings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="mx-auto max-w-2xl"
    >
      <h1 className={`mb-2 font-display text-3xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
        Settings
      </h1>
      <p className={`mb-8 ${isDark ? 'text-ai-muted' : 'text-gray-600'}`}>
        Customize your generation defaults and backend connection.
      </p>

      <div className="space-y-6">
        <SettingCard title="Appearance" icon={Palette} isDark={isDark}>
          <label className={`mb-2 block text-sm ${isDark ? 'text-ai-muted' : 'text-gray-600'}`}>
            Theme
          </label>
          <div className="flex gap-2">
            {['dark', 'light'].map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => updateSettings({ theme: t })}
                className={`rounded-xl px-4 py-2.5 text-sm font-medium capitalize ${
                  settings.theme === t
                    ? 'gradient-btn text-white'
                    : isDark
                      ? 'border border-ai-border bg-ai-card text-ai-muted'
                      : 'border border-gray-200 bg-white text-gray-600'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </SettingCard>

        <SettingCard title="Generation Defaults" icon={Sliders} isDark={isDark}>
          <div>
            <label className={`mb-2 block text-sm ${isDark ? 'text-ai-muted' : 'text-gray-600'}`}>
              Default style
            </label>
            <select
              value={settings.defaultStyle}
              onChange={(e) => updateSettings({ defaultStyle: e.target.value })}
              className={`w-full rounded-xl border px-4 py-2.5 text-sm ${
                isDark
                  ? 'border-ai-border bg-ai-card text-white'
                  : 'border-gray-200 bg-white'
              }`}
            >
              {IMAGE_STYLES.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
        </SettingCard>

        <SettingCard title="Backend API" icon={Globe} isDark={isDark}>
          <label className={`mb-2 block text-sm ${isDark ? 'text-ai-muted' : 'text-gray-600'}`}>
            API URL
          </label>
          <input
            type="url"
            value={settings.apiUrl}
            onChange={(e) => updateSettings({ apiUrl: e.target.value })}
            placeholder="http://localhost:8000"
            className={`w-full rounded-xl border px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-violet-500/40 ${
              isDark
                ? 'border-ai-border bg-ai-card text-white'
                : 'border-gray-200 bg-white'
            }`}
          />
          <p className={`mt-2 text-xs ${isDark ? 'text-ai-muted' : 'text-gray-500'}`}>
            POST requests will be sent to{' '}
            <code className="text-violet-400">{settings.apiUrl}/generate</code>
          </p>
        </SettingCard>
      </div>
    </motion.div>
  )
}

function SettingCard({ title, icon: Icon, children, isDark }) {
  return (
    <div className={`glass-card rounded-2xl p-6 ${isDark ? '' : 'bg-white'}`}>
      <div className="mb-4 flex items-center gap-2">
        <Icon className="h-5 w-5 text-violet-400" />
        <h2 className={`font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>{title}</h2>
      </div>
      {children}
    </div>
  )
}

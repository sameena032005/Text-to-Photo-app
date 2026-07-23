import { Clock } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { DURATIONS } from '../utils/constants'

export default function DurationSelector() {
  const { duration, setDuration, isGenerating, settings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <div className="flex flex-col gap-2">
      <span
        className={`flex items-center gap-2 text-xs font-medium uppercase tracking-wider ${
          isDark ? 'text-ai-muted' : 'text-gray-500'
        }`}
      >
        <Clock className="h-3.5 w-3.5" />
        Duration
      </span>
      <div className="flex flex-wrap gap-2">
        {DURATIONS.map((d) => {
          const active = duration === d.value
          return (
            <button
              key={d.value}
              type="button"
              disabled={isGenerating}
              onClick={() => setDuration(d.value)}
              className={`rounded-xl px-4 py-2.5 text-sm font-medium transition-all disabled:opacity-60 ${
                active
                  ? 'gradient-btn text-white shadow-md shadow-indigo-500/25'
                  : isDark
                    ? 'border border-ai-border bg-ai-card text-ai-muted hover:text-white'
                    : 'border border-gray-200 bg-white text-gray-600 hover:border-violet-300'
              }`}
            >
              {d.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}

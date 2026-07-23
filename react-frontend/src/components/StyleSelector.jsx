import { Palette } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { ASPECT_RATIOS, IMAGE_STYLES, QUALITIES } from '../utils/constants'

function SelectField({ label, icon: Icon, value, onChange, options, disabled, isDark }) {
  return (
    <div className="flex flex-col gap-2">
      <label
        className={`flex items-center gap-2 text-xs font-medium uppercase tracking-wider ${
          isDark ? 'text-ai-muted' : 'text-gray-500'
        }`}
      >
        {Icon && <Icon className="h-3.5 w-3.5" />}
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className={`rounded-xl border px-4 py-2.5 text-sm font-medium outline-none transition focus:ring-2 focus:ring-violet-500/40 ${
          isDark
            ? 'border-ai-border bg-ai-card text-white'
            : 'border-gray-200 bg-white text-gray-900'
        } disabled:opacity-60`}
      >
        {options.map((opt) => (
          <option key={typeof opt === 'object' ? opt.value : opt} value={typeof opt === 'object' ? opt.value : opt}>
            {typeof opt === 'object' ? opt.label : opt}
          </option>
        ))}
      </select>
    </div>
  )
}

export default function StyleSelector() {
  const { style, setStyle, ratio, setRatio, quality, setQuality, isGenerating, settings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <SelectField
        label="Art style"
        icon={Palette}
        value={style}
        onChange={setStyle}
        options={IMAGE_STYLES}
        disabled={isGenerating}
        isDark={isDark}
      />
      <SelectField
        label="Aspect ratio"
        value={ratio}
        onChange={setRatio}
        options={ASPECT_RATIOS}
        disabled={isGenerating}
        isDark={isDark}
      />
      <SelectField
        label="Quality"
        value={quality}
        onChange={setQuality}
        options={QUALITIES}
        disabled={isGenerating}
        isDark={isDark}
      />
    </div>
  )
}

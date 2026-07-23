import { useApp } from '../context/AppContext'

const links = [
  { label: 'About', href: '#about' },
  { label: 'Privacy', href: '#privacy' },
  { label: 'Contact', href: '#contact' },
]

export default function Footer() {
  const { settings } = useApp()
  const isDark = settings.theme === 'dark'

  return (
    <footer
      className={`mt-auto border-t px-4 py-8 sm:px-6 ${
        isDark ? 'border-ai-border bg-ai-black' : 'border-gray-200 bg-gray-50'
      }`}
    >
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 sm:flex-row">
        <p className={`text-sm ${isDark ? 'text-ai-muted' : 'text-gray-500'}`}>
          © {new Date().getFullYear()} AI Photo Generator. Powered by ComfyUI.
        </p>
        <nav className="flex gap-6">
          {links.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className={`text-sm font-medium transition hover:text-violet-400 ${
                isDark ? 'text-ai-muted' : 'text-gray-600'
              }`}
            >
              {link.label}
            </a>
          ))}
        </nav>
      </div>
    </footer>
  )
}

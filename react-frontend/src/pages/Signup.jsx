import { motion } from 'framer-motion'
import { Eye, EyeOff, ImageIcon, Lock, Mail, User } from 'lucide-react'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Signup() {
  const { signup, authLoading, authError, clearAuthError } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({ name: '', email: '', password: '', confirmPassword: '' })
  const [errors, setErrors] = useState({})
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  function validate() {
    const e = {}
    if (!form.name.trim()) e.name = 'Full name is required.'
    else if (form.name.trim().length < 2) e.name = 'Name must be at least 2 characters.'

    if (!form.email.trim()) e.email = 'Email is required.'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Enter a valid email.'

    if (!form.password) e.password = 'Password is required.'
    else if (form.password.length < 6) e.password = 'Password must be at least 6 characters.'

    if (!form.confirmPassword) e.confirmPassword = 'Please confirm your password.'
    else if (form.password !== form.confirmPassword) e.confirmPassword = 'Passwords do not match.'

    return e
  }

  function handleChange(e) {
    const { name, value } = e.target
    setForm((f) => ({ ...f, [name]: value }))
    setErrors((errs) => ({ ...errs, [name]: undefined }))
    clearAuthError()
  }

  async function handleSubmit(e) {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length) { setErrors(errs); return }
    const result = await signup({ name: form.name, email: form.email, password: form.password })
    if (result.success) navigate('/')
  }

  // Password strength indicator
  function getStrength(pwd) {
    if (!pwd) return 0
    let score = 0
    if (pwd.length >= 6) score++
    if (pwd.length >= 10) score++
    if (/[A-Z]/.test(pwd)) score++
    if (/[0-9]/.test(pwd)) score++
    if (/[^A-Za-z0-9]/.test(pwd)) score++
    return score
  }
  const strength = getStrength(form.password)
  const strengthLabel = ['', 'Weak', 'Fair', 'Good', 'Strong', 'Very strong'][strength]
  const strengthColor = ['', 'bg-red-500', 'bg-orange-400', 'bg-yellow-400', 'bg-green-400', 'bg-emerald-400'][strength]

  return (
    <div className="min-h-screen bg-ai-black flex items-center justify-center px-4 py-10">
      {/* Background glow */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-1/3 top-1/4 h-72 w-72 rounded-full bg-violet-600/20 blur-[120px]" />
        <div className="absolute right-1/4 bottom-1/4 h-56 w-56 rounded-full bg-blue-600/15 blur-[100px]" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="mb-8 flex flex-col items-center gap-3">
          <div className="gradient-btn flex h-14 w-14 items-center justify-center rounded-2xl shadow-lg shadow-indigo-500/30">
            <ImageIcon className="h-7 w-7 text-white" />
          </div>
          <h1 className="font-display text-2xl font-bold text-white">Create your account</h1>
          <p className="text-sm text-ai-muted">Start generating stunning AI photos</p>
        </div>

        {/* Card */}
        <div className="glass-card rounded-2xl p-8">
          <form onSubmit={handleSubmit} noValidate className="space-y-5">

            {/* Server error */}
            {authError && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400"
              >
                {authError}
              </motion.div>
            )}

            {/* Full name */}
            <div>
              <label className="mb-1.5 block text-sm font-medium text-ai-muted">Full name</label>
              <div className="relative">
                <User className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ai-muted" />
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  placeholder="Jane Smith"
                  autoComplete="name"
                  className={`w-full rounded-xl border bg-ai-card py-3 pl-10 pr-4 text-sm text-white placeholder-ai-muted outline-none transition focus:ring-2 focus:ring-violet-500/40 ${
                    errors.name ? 'border-red-500/60' : 'border-ai-border'
                  }`}
                />
              </div>
              {errors.name && <p className="mt-1 text-xs text-red-400">{errors.name}</p>}
            </div>

            {/* Email */}
            <div>
              <label className="mb-1.5 block text-sm font-medium text-ai-muted">Email address</label>
              <div className="relative">
                <Mail className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ai-muted" />
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                  autoComplete="email"
                  className={`w-full rounded-xl border bg-ai-card py-3 pl-10 pr-4 text-sm text-white placeholder-ai-muted outline-none transition focus:ring-2 focus:ring-violet-500/40 ${
                    errors.email ? 'border-red-500/60' : 'border-ai-border'
                  }`}
                />
              </div>
              {errors.email && <p className="mt-1 text-xs text-red-400">{errors.email}</p>}
            </div>

            {/* Password */}
            <div>
              <label className="mb-1.5 block text-sm font-medium text-ai-muted">Password</label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ai-muted" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  autoComplete="new-password"
                  className={`w-full rounded-xl border bg-ai-card py-3 pl-10 pr-11 text-sm text-white placeholder-ai-muted outline-none transition focus:ring-2 focus:ring-violet-500/40 ${
                    errors.password ? 'border-red-500/60' : 'border-ai-border'
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-ai-muted hover:text-white transition-colors"
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.password && <p className="mt-1 text-xs text-red-400">{errors.password}</p>}

              {/* Strength bar */}
              {form.password && (
                <div className="mt-2">
                  <div className="flex gap-1 mb-1">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <div
                        key={i}
                        className={`h-1 flex-1 rounded-full transition-all ${
                          i <= strength ? strengthColor : 'bg-ai-border'
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-ai-muted">{strengthLabel}</p>
                </div>
              )}
            </div>

            {/* Confirm password */}
            <div>
              <label className="mb-1.5 block text-sm font-medium text-ai-muted">Confirm password</label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ai-muted" />
                <input
                  type={showConfirm ? 'text' : 'password'}
                  name="confirmPassword"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  placeholder="••••••••"
                  autoComplete="new-password"
                  className={`w-full rounded-xl border bg-ai-card py-3 pl-10 pr-11 text-sm text-white placeholder-ai-muted outline-none transition focus:ring-2 focus:ring-violet-500/40 ${
                    errors.confirmPassword ? 'border-red-500/60' : 'border-ai-border'
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirm((v) => !v)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-ai-muted hover:text-white transition-colors"
                  aria-label={showConfirm ? 'Hide password' : 'Show password'}
                >
                  {showConfirm ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-xs text-red-400">{errors.confirmPassword}</p>
              )}
            </div>

            {/* Submit */}
            <motion.button
              type="submit"
              disabled={authLoading}
              whileHover={{ scale: authLoading ? 1 : 1.02 }}
              whileTap={{ scale: authLoading ? 1 : 0.98 }}
              className="gradient-btn mt-2 w-full rounded-xl py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition disabled:opacity-60"
            >
              {authLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                  Creating account...
                </span>
              ) : (
                'Create account'
              )}
            </motion.button>
          </form>
        </div>

        {/* Footer link */}
        <p className="mt-6 text-center text-sm text-ai-muted">
          Already have an account?{' '}
          <Link
            to="/login"
            className="font-medium text-violet-400 hover:text-violet-300 transition-colors"
          >
            Sign in
          </Link>
        </p>
      </motion.div>
    </div>
  )
}

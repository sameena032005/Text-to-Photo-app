import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { loginUser, registerUser } from '../api/authApi'

const AuthContext = createContext(null)

const AUTH_KEY = 'ai-photo-auth'

function loadAuth() {
  try {
    const raw = localStorage.getItem(AUTH_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(loadAuth)
  const [authLoading, setAuthLoading] = useState(false)
  const [authError, setAuthError] = useState(null)

  useEffect(() => {
    if (user) {
      localStorage.setItem(AUTH_KEY, JSON.stringify(user))
    } else {
      localStorage.removeItem(AUTH_KEY)
    }
  }, [user])

  const login = useCallback(async ({ email, password }) => {
    setAuthLoading(true)
    setAuthError(null)
    try {
      const userData = await loginUser({ email, password })
      setUser(userData)
      return { success: true }
    } catch (err) {
      const msg = err.message || 'Login failed. Please try again.'
      setAuthError(msg)
      return { success: false, error: msg }
    } finally {
      setAuthLoading(false)
    }
  }, [])

  const signup = useCallback(async ({ name, email, password }) => {
    setAuthLoading(true)
    setAuthError(null)
    try {
      const userData = await registerUser({ name, email, password })
      setUser(userData)
      return { success: true }
    } catch (err) {
      const msg = err.message || 'Signup failed. Please try again.'
      setAuthError(msg)
      return { success: false, error: msg }
    } finally {
      setAuthLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    setUser(null)
    setAuthError(null)
  }, [])

  const clearAuthError = useCallback(() => setAuthError(null), [])

  const value = useMemo(
    () => ({ user, authLoading, authError, login, signup, logout, clearAuthError }),
    [user, authLoading, authError, login, signup, logout, clearAuthError]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

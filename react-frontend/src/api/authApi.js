// Mock auth API — replace with real backend calls when ready

const USERS_KEY = 'ai-photo-users'

function getUsers() {
  try {
    return JSON.parse(localStorage.getItem(USERS_KEY) || '[]')
  } catch {
    return []
  }
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users))
}

/**
 * Simulate login — checks stored users by email + password
 */
export async function loginUser({ email, password }) {
  await new Promise((r) => setTimeout(r, 800)) // simulate network delay

  const users = getUsers()
  const user = users.find(
    (u) => u.email.toLowerCase() === email.toLowerCase() && u.password === password
  )

  if (!user) {
    throw new Error('Invalid email or password.')
  }

  const { password: _pw, ...safeUser } = user
  return { ...safeUser, token: btoa(`${user.email}:${Date.now()}`) }
}

/**
 * Simulate signup — creates a new user entry
 */
export async function registerUser({ name, email, password }) {
  await new Promise((r) => setTimeout(r, 800))

  const users = getUsers()
  const exists = users.some((u) => u.email.toLowerCase() === email.toLowerCase())

  if (exists) {
    throw new Error('An account with this email already exists.')
  }

  const newUser = {
    id: Date.now().toString(),
    name: name.trim(),
    email: email.toLowerCase().trim(),
    password, // in production, this would be hashed server-side
    createdAt: new Date().toISOString(),
  }

  saveUsers([...users, newUser])

  const { password: _pw, ...safeUser } = newUser
  return { ...safeUser, token: btoa(`${newUser.email}:${Date.now()}`) }
}

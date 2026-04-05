// services/questService.js
const nuxtApp = useNuxtApp()
const BASE_URL = 'https://questly-production-75dc.up.railway.app'
//const BASE_URL = import.meta.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
console.log('API BASE URL:', BASE_URL)

// Token helpers

function getToken() {
  return localStorage.getItem('questly_token')
}

function setToken(token) {
  localStorage.setItem('questly_token', token)
}

function clearToken() {
  localStorage.removeItem('questly_token')
  localStorage.removeItem('questly_player')
}

function setPlayer(player) {
  localStorage.setItem('questly_player', JSON.stringify(player))
}

function getPlayer() {
  const p = localStorage.getItem('questly_player')
  return p ? JSON.parse(p) : null
}

// Base fetch wrapper

async function api(path, options = {}) {
  const token = getToken()
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  }

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers,
    })

    if (res.status === 204) return null

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.detail || `Request failed: ${res.status}`)
    }

    return data

  } catch (err) {
    // Native fetch errors (no internet, timeout, DNS failure etc.)
    if (err.message === 'Failed to fetch' || err instanceof TypeError) {
      throw new Error('Unable to connect. Please check your internet connection.')
    }
    throw err  // re-throw API errors as normal
  }
}

// Auth

const auth = {
  async register(name, email, password) {
    const data = await api('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    })
    setToken(data.access_token)
    setPlayer(data.player)
    return data
  },

  async login(email, password) {
    const data = await api('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    setToken(data.access_token)
    setPlayer(data.player)
    return data
  },

  logout() {
    clearToken()
  },

  isLoggedIn() {
    return !!getToken()
  },

  currentPlayer() {
    return getPlayer()
  },

  async me() {
    return api('/auth/me')
  },
}

// Player

const players = {
  async getProfile() {
    return api('/players/me')
  },

  async updateProfile(payload) {
    // payload: { name?, bio?, avatar_url? }
    return api('/players/me', {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },

  async getStats() {
    return api('/players/me/stats')
  },

  async getAchievements() {
    return api('/players/me/achievements')
  },
}

// Quests

const quests = {
  async list(status = null) {
    const query = status ? `?status=${status}` : ''
    return api(`/quests/${query}`)
  },

  async get(id) {
    return api(`/quests/${id}`)
  },

  async create(payload) {
    // payload: { name, description?, due_date?, difficulty, priority }
    return api('/quests/', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async update(id, payload) {
    // payload: any subset of quest fields
    return api(`/quests/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },

  async delete(id) {
    return api(`/quests/${id}`, { method: 'DELETE' })
  },

  async start(id) {
    return api(`/quests/${id}/start`, { method: 'POST' })
  },

  async complete(id) {
    // Returns: { quest, xp_gained, new_xp, leveled_up, new_level, achievements_unlocked }
    return api(`/quests/${id}/complete`, { method: 'POST' })
  },

  async abandon(id) {
    return api(`/quests/${id}/abandon`, { method: 'POST' })
  },
}

// Achievements

const achievements = {
  async listAll() {
    return api('/achievements/')
  },
}

// Progression

const progression = {
  async get() {
    // Returns: { level, current_xp, xp_to_next_level, progress_percent, ... }
    return api('/progression/')
  },
}

// Export

export default {
  auth,
  players,
  quests,
  achievements,
  progression,
  getToken,
  getPlayer,
}
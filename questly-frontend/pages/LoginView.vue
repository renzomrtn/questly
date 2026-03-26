<template>
  <div class="auth-page">
    <NuxtLink to="/" class="auth-page_back">< Back</NuxtLink>

    <div class="auth-page_header">
      <div class="auth-page_label">QUESTLY</div>
      <h1>Sign In</h1>
      <p>Continue your adventure</p>
    </div>

    <form class="auth-form" @submit.prevent="submit">
      <div class="field">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="you@example.com"
          required
          autocomplete="email"
        />
      </div>
      <div class="field">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="••••••••"
          required
          autocomplete="current-password"
        />
      </div>

      <p v-if="error" class="auth-form_error">{{ error }}</p>

      <button type="submit" class="btn-submit" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>
    </form>

    <p class="auth-page_switch">
      No account? <NuxtLink to="/RegisterView">Create one</NuxtLink>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/questService'

const email    = ref('')
const password = ref('')
const loading  = ref(false)
const error    = ref(null)

async function submit() {
  loading.value = true
  error.value = null
  try {
    await api.auth.login(email.value, password.value)
    await navigateTo('/QuestsView')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  background: #0a0a14;
}

.auth-page_back {
  font-size: 13px;
  color: #5a5a7a;
  text-decoration: none;
  margin-bottom: 2.5rem;
  display: inline-block;
}

.auth-page_back:hover {
  color: #fff;
}

.auth-page_label {
  font-size: 10px;
  font-weight: 600;
  color: #3d2fff;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.auth-page_header {
  margin-bottom: 2rem;
}

.auth-page_header h1 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 4px;
}

.auth-page_header p {
  font-size: 13px;
  color: #5a5a7a;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-size: 11px;
  font-weight: 600;
  color: #8888aa;
}

.field input {
  background: #111128;
  border: 1px solid #2a2a42;
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 14px;
  color: #fff;
  outline: none;
  transition: border-color 0.2s;
}

.field input:focus {
  border-color: #3d2fff;
}

.auth-form_error {
  font-size: 12px;
  color: #ef4444;
  background: #1f0a0a;
  border: 1px solid #3f1a1a;
  border-radius: 8px;
  padding: 8px 12px;
  margin: 0;
}

.btn-submit {
  background: #3d2fff;
  border: none;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  padding: 13px;
  border-radius: 14px;
  cursor: pointer;
  margin-top: 6px;
  transition: opacity 0.2s;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-page_switch {
  font-size: 13px;
  color: #5a5a7a;
  text-align: center;
  margin-top: 1.5rem;
}

.auth-page_switch a {
  color: #3d2fff;
  font-weight: 600;
  text-decoration: none;
}
</style>
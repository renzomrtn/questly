<template>
    <div class="auth-page">
        <NuxtLink to="/" class="auth-page_back">< Back</NuxtLink>

        <div class="auth-page_header">
            <h1>Create Account</h1>
            <p>Your adventure begins here</p>
        </div>

        <form class="auth-form" @submit.prevent="submit">
            <div class="field">
                <label for="name">Name</label>
                <input id="name" type="text" v-model="name" placeholder="Hero Name" required />
            </div>
            <div class="field">
                <label for="email">Email</label>
                <input id="email" type="email" v-model="email" placeholder="you@example.com" required />
            </div>
            <div class="field">
                <label for="password">Password</label>
                <input id="password" type="password" v-model="password" placeholder="Min 8 characters" required
                    minlength="8" />
            </div>

            <p v-if="error" class="auth-form_error">{{ error }}</p>
            <p v-if="success" class="auth-form_success">{{ success }}</p>

            <button type="submit" class="btn-submit" :disabled="loading">
                {{ loading ? 'Creating account...' : 'Create Account' }}
            </button>
        </form>

        <p class="auth-page_switch">
            Already have an account? <NuxtLink to="/LoginView">Sign in</NuxtLink>
        </p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import questService from '@/services/questService'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

async function submit() {
    error.value = ''
    success.value = ''
    loading.value = true

    try {
        await questService.auth.register(name.value, email.value, password.value)
        success.value = 'Account created! Redirecting...'
        setTimeout(() => router.push('/'), 1200)
    } catch (err) {
        error.value = err.message || 'Registration failed. Please try again.'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.auth-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 1.5rem;
    gap: 1.5rem;
}

.auth-page_back {
    align-self: flex-start;
    font-size: 13px;
    color: #5a5a7a;
    text-decoration: none;
}

.auth-page_header {
    text-align: center;
}

.auth-page_header h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #fff;
}

.auth-page_header p {
    font-size: 13px;
    color: #5a5a7a;
    margin-top: 4px;
}

.auth-form {
    background: #111128;
    border: 1px solid #1e1e38;
    border-radius: 18px;
    padding: 1.5rem;
    width: 100%;
    max-width: 320px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.field label {
    font-size: 12px;
    font-weight: 600;
    color: #8888aa;
}

.field input {
    background: #0d0d1a;
    border: 1px solid #2a2a42;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 14px;
    color: #fff;
    outline: none;
}

.field input:focus {
    border-color: #3d2fff;
}

.auth-form_error {
    font-size: 12px;
    color: #ef4444;
    background: #1f0a0a;
    padding: 8px 12px;
    border-radius: 8px;
}

.auth-form_success {
    font-size: 12px;
    color: #22c55e;
    background: #0a2318;
    padding: 8px 12px;
    border-radius: 8px;
}

.btn-submit {
    background: #3d2fff;
    color: #fff;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
}

.btn-submit:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.auth-page_switch {
    font-size: 13px;
    color: #5a5a7a;
}

.auth-page_switch a {
    color: #3d2fff;
    text-decoration: none;
    font-weight: 600;
}
</style>

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  ssr: false,                    // ← SPA mode for Capacitor
  css: [
    'assets/global.css',
    '~/node_modules/@mdi/font/css/materialdesignicons.css'
  ],
  nitro: {
    prerender: {
      crawlLinks: true
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  }
})
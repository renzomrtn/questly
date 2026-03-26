export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const token = localStorage.getItem('questly_token')
    if (!token && to.path !== '/LoginView') {
      return navigateTo('/LoginView')
    }
  }
})
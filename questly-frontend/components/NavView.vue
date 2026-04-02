<template>
    <section class="bottom-nav">
        <NuxtLink to="/DashboardView" class="nav-item" :class="{ active: route.path === '/DashboardView' }">
            <i class="mdi mdi-view-dashboard-outline"></i>
        </NuxtLink>

        <NuxtLink to="/QuestsView" class="nav-item" :class="{ active: route.path === '/QuestsView' }">
            <i class="mdi mdi-format-list-bulleted"></i>
        </NuxtLink>

        <NuxtLink to="/ProfileView" class="nav-item" :class="{ active: route.path === '/ProfileView' }">
            <i class="mdi mdi-account-badge-outline"></i>
        </NuxtLink>

        <NuxtLink to="/SettingsView" class="nav-item" :class="{ active: route.path === '/SettingsView' }">
            <i class="mdi mdi-cog"></i>
        </NuxtLink>
    </section>
</template>

<script setup>
const route = useRoute()
</script>

<style scoped>
.bottom-nav {
    width: 80%;
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 14px;
    padding: 10px 18px;
    border: 1px solid #2d2d55;
    border-radius: 99px;
    background: #0d0d1a;
    justify-content: space-between;
}

.nav-item {
    color: #b6adad;
    font-size: 24px;
    text-decoration: none;
    transition: 0.2s ease;
}

.nav-item {
    padding: 3px 5px;
}

.nav-item.active {
    color: rgb(255, 255, 255);
    background-color: rgba(106, 176, 255, 0.5);
    border-radius: 12px;
}

.nav-item:hover {
    color: #fff;
}
</style>
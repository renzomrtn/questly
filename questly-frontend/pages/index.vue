<template>
    <div class="welcome">
        <div class="welcome_logo">
            <p class="welcome_tagline">Finish quests, earn EXP</p>
            <h1 class="welcome_title">Welcome to <span>Questly</span></h1>
            <p class="welcome_sub">Where your quests await</p>
        </div>

        <div class="welcome_card">
            <NuxtLink to="/LoginView" class="btn btn_primary">
                Sign In
            </NuxtLink>
            <NuxtLink to="/RegisterView" class="btn btn_secondary">
                Sign Up
            </NuxtLink>
        </div>

        <p class="welcome_desc">
            Questly turns your daily tasks into quests. Complete them, earn XP, level up, and unlock achievements.
        </p>
    </div>
</template>

<script setup>
</script>

<style scoped>
.welcome {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 1.5rem;
    gap: 2rem;
}

.welcome_logo {
    text-align: center;
}

.welcome_logomark {
    width: 64px;
    height: 64px;
    background: #1a0e3a;
    border: 2px solid #3d2fff;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    color: #3d2fff;
}

.welcome_tagline {
    font-size: 11px;
    color: #5a5a7a;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.welcome_title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
}

.welcome_title span {
    color: #3d2fff;
}

.welcome_sub {
    font-size: 13px;
    color: #5a5a7a;
    margin-top: 4px;
}

.welcome_card {
    background: #111128;
    border: 1px solid #1e1e38;
    border-radius: 18px;
    padding: 1.5rem;
    width: 100%;
    max-width: 320px;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 0.75rem;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: opacity 0.15s;
}

.btn_primary {
    background: #3d2fff;
    color: #fff;
}

.btn_secondary {
    background: transparent;
    border: 1.5px solid #2a2a42;
    color: #8888aa;
}

.btn:active {
    opacity: 0.8;
}

.welcome_desc {
    font-size: 12px;
    color: #3a3a5a;
    text-align: center;
    line-height: 1.7;
    max-width: 280px;
}
</style>

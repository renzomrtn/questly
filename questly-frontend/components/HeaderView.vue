<template>
    <section class="header">
        <h1>Quest<span>ly</span></h1>
        <div class="wrapper">
            <div class="energy-bar">
                <i class="mdi mdi-lightning-bolt energy-icon"></i>
                <div class="bar-track">
                    <div class="bar-fill" :style="{ width: energyPercent + '%' }"></div>
                </div>
                <span class="energy-text">{{ stats?.current_energy ?? 0 }}/{{ stats?.max_energy ?? 100 }}</span>
            </div>
            <div class="streak-badge">
                <i class="mdi mdi-fire"></i>
                {{ stats?.streak_days ?? 0 }}d
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import questService from '@/services/questService'

const stats = ref(null)

const energyPercent = computed(() => {
    if (!stats.value) return 0
    return Math.round((stats.value.current_energy / stats.value.max_energy) * 100)
})



onMounted(async () => {
    try {
        stats.value = await questService.players.getStats()
    } catch (err) {
        console.error('Header: failed to load stats', err)
    }
})
</script>

<style scoped>
.header {
    width: 80%;
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    color: #fff;
    justify-content: space-between;
    align-items: center;
    padding: 10px 18px;
    border: 1px solid #2d2d55;
    border-radius: 99px;
    background: #0d0d1a;
    gap: 8px;
}

h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 25px;
    font-weight: 700;
    margin: 0;
    white-space: nowrap;
    flex-shrink: 0;
}

h1 span {
    color: #3d2fff;
}

.wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}

/* Energy bar */
.energy-bar {
    display: flex;
    align-items: center;
    gap: 4px;
    background: #1f1f3d;
    border-radius: 99px;
    padding: 4px 8px 4px 6px;
}

.energy-icon {
    font-size: 13px;
    color: #3d2fff;
    line-height: 1;
}

.bar-track {
    width: 52px;
    height: 5px;
    background: #2a2a45;
    border-radius: 99px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: #3d2fff;
    border-radius: 99px;
    transition: width 0.4s ease;
}

.energy-text {
    font-size: 10px;
    font-weight: 600;
    color: #8888aa;
    white-space: nowrap;
}

/* Streak badge */
.streak-badge {
    display: flex;
    align-items: center;
    gap: 3px;
    background: #2a1500;
    color: #f59e0b;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    border-radius: 99px;
    white-space: nowrap;
}

.streak-badge .mdi {
    font-size: 13px;
}


</style>
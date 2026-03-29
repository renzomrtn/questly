<template>
    <HeaderView />
    <div class="dashboard">
        <div class="dashboard_hero">
            <div class="dashboard_label">DASHBOARD</div>
            <h1>Welcome back, {{ profile?.name ?? '...' }}!</h1>
            <p>Here's your current activity</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-card_icon stat-card_icon_red">
                    <i class="mdi mdi-format-list-group"></i>
                </div>
                <div class="stat-card_num">{{ activeQuests }}</div>
                <div class="stat-card_lbl">Active Quests</div>
            </div>

            <div class="stat-card">
                <div class="stat-card_icon stat-card_icon_green">
                    <i class="mdi mdi-check"></i>
                </div>
                <div class="stat-card_num">{{ stats?.quests_completed ?? 0 }}</div>
                <div class="stat-card_lbl">Completed</div>
            </div>

            <div class="stat-card">
                <div class="stat-card_icon stat-card_icon_yellow">
                    <i class="mdi mdi-clock-time-five-outline"></i>
                </div>
                <div class="stat-card_num">{{ inProgressQuests }}</div>
                <div class="stat-card_lbl">On Going</div>
            </div>

            <div class="stat-card">
                <div class="stat-card_icon stat-card_icon_amber">
                    <i class="mdi mdi-trophy-outline"></i>
                </div>
                <div class="stat-card_num">{{ achievements.length }}</div>
                <div class="stat-card_lbl">Achievements</div>
            </div>

            <div class="stat-card">
                <div class="stat-card_icon stat-card_icon_blue">
                    <i class="mdi mdi-lightning-bolt"></i>
                </div>
                <div class="stat-card_num">{{ stats?.current_energy ?? 0 }}</div>
                <div class="stat-card_lbl">Energy Left</div>
            </div>

            <div class="stat-card">
                <div class="stat-card_icon stat-card_icon_purple">
                    <i class="mdi mdi-fire"></i>
                </div>
                <div class="stat-card_num">{{ stats?.streak_days ?? 0 }}</div>
                <div class="stat-card_lbl">Day Streak</div>
            </div>
        </div>

        <!-- Level progress card -->
        <div class="level-card">
            <div class="level-card_row">
                <span class="level-card_title">Experience Progress</span>
                <span class="level-card_badge">Lv. {{ stats?.level ?? 1 }}</span>
            </div>
            <div class="level-card_bar">
                <div class="level-card_fill" :style="{ width: xpPercent + '%' }"></div>
            </div>
            <div class="level-card_foot">
                <span>{{ stats?.current_xp ?? 0 }} / {{ xpTotal }} XP</span>
                <span>{{ stats?.xp_to_next_level ?? 0 }} XP to Lv. {{ (stats?.level ?? 1) + 1 }}</span>
            </div>
        </div>
    </div>
    <NavView />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import questService from '@/services/questService'

definePageMeta({ middleware: 'auth' })

const profile = ref(null)
const stats = ref(null)
const achievements = ref([])
const allQuests = ref([])

// Filter quests by status client-side
const activeQuests = computed(() =>
    allQuests.value.filter(q => q.status === 'pending').length
)

const inProgressQuests = computed(() =>
    allQuests.value.filter(q => q.status === 'in_progress').length
)

// XP bar
const xpTotal = computed(() => {
    if (!stats.value) return 0
    return stats.value.current_xp + stats.value.xp_to_next_level
})

const xpPercent = computed(() => {
    if (!stats.value || !xpTotal.value) return 0
    return Math.min(100, Math.round((stats.value.current_xp / xpTotal.value) * 100))
})

onMounted(async () => {
    try {
        const [profileData, statsData, achievementsData, questsData] = await Promise.all([
            questService.players.getProfile(),
            questService.players.getStats(),
            questService.players.getAchievements(),
            questService.quests.list(),
        ])
        profile.value = profileData ?? null
        stats.value = statsData ?? null
        achievements.value = achievementsData ?? []
        allQuests.value = questsData ?? []
    } catch (err) {
        console.error('Failed to load dashboard:', err)
    }
})
</script>

<style scoped>
.dashboard {
    padding-top: 50px;
    padding-bottom: 80px;
}

.dashboard_hero {
    padding: 16px 16px 10px;
}

.dashboard_label {
    font-size: 10px;
    font-weight: 600;
    color: #3d2fff;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.dashboard_hero h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
}

.dashboard_hero p {
    font-size: 12px;
    color: #5a5a7a;
    margin-top: 2px;
}

.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    padding: 0 14px 12px;
}

.stat-card {
    background: #1f1f3d;
    border: 1px solid #1e1e38;
    border-radius: 14px;
    padding: 14px;
}

.stat-card_icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}

.stat-card_icon svg {
    width: 18px;
    height: 18px;
}

.stat-card_icon_blue {
    background: #0e2050;
    color: #4f8fff;
}

.stat-card_icon_yellow {
    background: #3d470d;
    color: #c2c522;
}

.stat-card_icon_red {
    background: #470d36;
    color: #ff08b5;
}

.stat-card_icon_green {
    background: #103827;
    color: #22c55e;
}

.stat-card_icon_amber {
    background: #382101;
    color: #f59e0b;
}

.stat-card_icon_purple {
    background: #22134d;
    color: #a855f7;
}

.stat-card_num {
    font-family: 'Rajdhani', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #fff;
    line-height: 1;
}

.stat-card_lbl {
    font-size: 11px;
    color: #bfbfcc;
    margin-top: 3px;
}

.level-card {
    margin: 0 14px 12px;
    background: #111128;
    border: 1px solid #2a1a5e;
    border-radius: 14px;
    padding: 14px;
}

.level-card_row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.level-card_title {
    font-size: 12px;
    font-weight: 600;
    color: #d0d0e8;
}

.level-card_badge {
    background: #1a0e3a;
    border: 1px solid #3d2fff;
    border-radius: 8px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
    color: #7c5cfc;
}

.level-card_bar {
    height: 8px;
    background: #1a1a2e;
    border-radius: 4px;
    overflow: hidden;
}

.level-card_fill {
    height: 100%;
    background: #3d2fff;
    border-radius: 4px;
    transition: width 0.4s ease;
}

.level-card_foot {
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
    font-size: 10px;
    color: #3a3a5a;
}
</style>

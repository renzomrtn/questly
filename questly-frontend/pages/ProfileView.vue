<template>
    <HeaderView />
    <div class="profile">
        <div class="profile-page_header">
            <div class="profile-page_label">PLAYER</div>
            <h1>Profile</h1>
            <p>Your Profile Information and Statistics</p>
        </div>

        <div class="profile-page_toolbar">
            <button class="btn-new" @click="">Edit Profile</button>
        </div>

        <div v-if="loading" class="loading-state">Loading...</div>

        <template v-else>
            <div class="profile-wrapper">
                <div class="profile-grid">
                    <div class="profile-card">
                        <div class="profile-card-left">
                            <img v-if="profile?.avatar_url" :src="profile.avatar_url" class="avatar-img" alt="avatar" />
                            <i v-else class="mdi mdi-account"></i>
                        </div>
                        <div class="profile-card-right">
                            <div class="stat-card_num">{{ profile?.name }}</div>
                            <div class="stat-card_lbl">{{ profile?.email }}</div>
                            <div class="stat-card_lbl lvl">Level {{ profile?.level }}</div>
                            <div v-if="profile?.bio" class="stat-card_lbl bio">{{ profile.bio }}</div>
                        </div>
                    </div>
                </div>

                <div class="quest-grid">
                    <div class="quest-card">
                        <div class="stat-card_num">{{ stats?.quests_completed ?? 0 }}</div>
                        <div class="stat-card_lbl">Tasks Completed</div>
                    </div>
                    <div class="quest-card">
                        <div class="stat-card_num">{{ achievements.length }}</div>
                        <div class="stat-card_lbl">Achievements</div>
                    </div>
                    <div class="quest-card">
                        <div class="stat-card_num">{{ stats?.streak_days ?? 0 }}</div>
                        <div class="stat-card_lbl">Highest Streak</div>
                    </div>
                </div>

                <div class="experience-grid">
                    <div class="experience-card">
                        <div class="sidebyside">
                            <div class="stat-card_lbl">Experience Progress</div>
                            <div class="stat-card_lbl">{{ stats?.current_xp ?? 0 }} / {{ xpTotal }} XP</div>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
                        </div>
                        <div class="stat-card_lbl">{{ stats?.xp_to_next_level ?? 0 }} XP until Level {{ (stats?.level ?? 0) + 1 }}</div>
                    </div>
                </div>
            </div>

            <div class="achievements-wrapper">
                <div class="achievements_header">
                    <div class="achivements_label">ACHIEVEMENTS</div>
                </div>

                <div v-if="achievements.length === 0" class="stat-card_lbl" style="padding: 0 16px;">
                    No achievements yet. Complete quests to earn some!
                </div>

                <div
                    v-for="item in achievements"
                    :key="item.id"
                    class="achievement-card"
                >
                    <div class="ach-icon">
                        <i :class="`mdi mdi-${item.achievement?.icon ?? 'trophy'}`"></i>
                    </div>
                    <div class="ach-info">
                        <div class="ach-name">{{ item.achievement?.name }}</div>
                        <div class="ach-lbl">{{ item.achievement?.description }}</div>
                    </div>
                </div>
            </div>
        </template>
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
const loading = ref(true)

// Total XP cap for the progress bar denominator
const xpTotal = computed(() => {
    if (!stats.value) return 0
    return stats.value.current_xp + stats.value.xp_to_next_level
})

const progressPercent = computed(() => {
    if (!xpTotal.value) return 0
    return Math.min(100, Math.round((stats.value.current_xp / xpTotal.value) * 100))
})

onMounted(async () => {
    try {
        // Fire all three in parallel
        const [profileData, statsData, achievementsData] = await Promise.all([
            questService.players.getProfile(),
            questService.players.getStats(),
            questService.players.getAchievements(),
        ])
        profile.value = profileData
        stats.value = statsData
        achievements.value = achievementsData
    } catch (err) {
        console.error('Failed to load profile:', err)
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.profile {
    padding-bottom: 80px;
    color: #bfbfcc;
}

.loading-state {
    padding: 32px 16px;
    text-align: center;
    color: #5a5a7a;
    font-size: 13px;
}

.profile-page_header,
.achievements_header {
    padding: 16px 16px 8px;
}

.profile-page_label,
.achivements_label {
    font-size: 10px;
    font-weight: 600;
    color: #3d2fff;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.profile-page_header h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
}

.profile-page_header p {
    font-size: 11px;
    color: #5a5a7a;
    margin-top: 1px;
}

.profile-page_toolbar {
    padding: 16px 8px;
    display: flex;
    justify-content: right;
}

.btn-new {
    background: #3d2fff;
    border: none;
    color: #fff;
    font-size: 12px;
    font-weight: 600;
    padding: 7px 16px;
    border-radius: 20px;
    cursor: pointer;
}
.quest-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    padding: 0 14px 12px;
}

.profile-grid,
.experience-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
    padding: 0 14px 12px;
}

.profile-card,
.experience-card,
.quest-card {
    background: #1f1f3d;
    border-radius: 14px;
    padding: 14px;
    display: flex;
    font-size: small;
}

.quest-card {
    text-align: center;
}

.lvl {
    color: #858588;
}

.quest-card,
.experience-card {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.sidebyside {
    display: flex;
    justify-content: space-between;
}

.profile-card-left {
    width: 30%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.profile-card-right {
    width: 70%;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.profile-card-left,
.profile-card-right {
    border: #1f1f3d 1px solid;
}

.avatar-img {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    object-fit: cover;
}

.bio {
    margin-top: 4px;
    font-style: italic;
    color: #5a5a7a;
}

/* XP progress bar */
.progress {
    background: #2e2e55;
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
    margin: 4px 0;
}

.progress-bar {
    height: 100%;
    background: #3d2fff;
    border-radius: 99px;
    transition: width 0.4s ease;
}

/* Achievement cards */
.achievement-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #1f1f3d;
    border-radius: 14px;
    padding: 12px 14px;
    margin: 0 14px 10px;
}

.ach-icon {
    font-size: 22px;
    color: #3d2fff;
    min-width: 28px;
    text-align: center;
}

.ach-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.ach-name {
    font-size: 13px;
    font-weight: 600;
    color: #fff;
}

.ach-lbl {
    font-size: 11px;
    color: #5a5a7a;
}
</style>
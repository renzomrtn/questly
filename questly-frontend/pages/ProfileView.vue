<template>
    <HeaderView />
    <div class="profile">
        <div class="profile-page_header">
            <div class="profile-page_label">PLAYER</div>
            <div class="page_label_container">
                <div class="page_label_left">
                    <h1>Profile</h1>
                    <p>Your Profile Information and Statistics</p>
                </div>
                <div class="page_label_right">
                    <button class="btn-logout" @click="logout" title="Logout">
                        <i class="mdi mdi-logout"></i> Logout
                    </button>
                </div>
            </div>
        </div>
        <div class="profile-page_toolbar">
            <button class="btn-new" @click="openEdit">Edit Profile</button>
        </div>
        <div v-if="loading" class="loading-state">Loading...</div>

        <template v-else>
            <div class="profile-wrapper">
                <div class="profile-grid">
                    <div class="profile-card">
                        <div class="profile-card-left">
                            <img v-if="profile?.avatar_url" :src="profile.avatar_url" class="avatar-img" alt="avatar" />
                            <img v-else class="adventurer-avatar" :src="avatarImage" alt="default-avatar" />
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
                        <div class="stat-card_lbl">{{ stats?.xp_to_next_level ?? 0 }} XP until Level {{ (stats?.level ??
                            0) + 1 }}</div>
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

                <div v-for="item in achievements" :key="item.id" class="achievement-card">
                    <div class="ach-icon">
                        {{ item.achievement?.icon ?? '🏆' }}
                    </div>
                    <div class="ach-info">
                        <div class="ach-name">{{ item.achievement?.name }}</div>
                        <div class="ach-lbl">{{ item.achievement?.description }}</div>
                    </div>
                </div>
            </div>
        </template>
    </div>
    <!-- Edit Profile Modal -->
    <Teleport to="body">
        <div v-if="showEdit" class="modal-overlay" @click.self="showEdit = false">
            <div class="modal">
                <h2>Edit Profile</h2>
                <form @submit.prevent="saveProfile">
                    <div class="field">
                        <label>Display Name</label>
                        <input v-model="editForm.name" type="text" placeholder="Your name" required />
                    </div>
                    <div class="field">
                        <label>Bio (optional)</label>
                        <textarea v-model="editForm.bio" placeholder="Tell us about yourself..." rows="2"></textarea>
                    </div>
                    <div class="field">
                        <label>Choose Avatar</label>
                        <div class="avatar-picker">
                            <button v-for="src in PRESET_AVATARS" :key="src" type="button" class="avatar-option"
                                :class="{ 'avatar-option--selected': editForm.avatar_url === src }"
                                @click="editForm.avatar_url = src">
                                <img :src="src" :alt="src" />
                            </button>
                        </div>
                    </div>
                    <div v-if="editError" class="form-error">{{ editError }}</div>
                    <div class="modal_actions">
                        <button type="button" class="btn-cancel" @click="showEdit = false">Cancel</button>
                        <button type="submit" class="btn-submit" :disabled="saving">
                            {{ saving ? 'Saving...' : 'Save Changes' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </Teleport>
    <NavView />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import questService from '@/services/questService'
import { useRouter } from 'vue-router'
import avatarImage from '../public/avatars/chat_warrior.png'

const router = useRouter()

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

function logout() {
    questService.auth.logout()
    router.push('/LoginView')
}

// ── Edit Profile ──────────────────────────────────────────────────────────────
const showEdit = ref(false)
const saving = ref(false)
const editError = ref(null)

const editForm = ref({
    name: '',
    bio: '',
    avatar_url: '',
})

// ── Avatar presets ─────────────────────────────────────────────────────────
const PRESET_AVATARS = [
    '/avatars/chat_warrior.png',
    '/avatars/chat_mage.png',
    '/avatars/chat_assassin.png',
    '/avatars/chat_archer.png',
    '/avatars/chat_tank.png',
    '/avatars/chat_healer.png'
]

function openEdit() {
    editForm.value = {
        name: profile.value?.name ?? '',
        bio: profile.value?.bio ?? '',
        avatar_url: profile.value?.avatar_url ?? PRESET_AVATARS[0],
    }
    editError.value = null
    showEdit.value = true
}

async function saveProfile() {
    saving.value = true
    editError.value = null
    try {
        const payload = { ...editForm.value }
        if (!payload.bio) delete payload.bio
        // avatar_url is always set from the picker, so keep it

        const updated = await questService.players.updateProfile(payload)
        profile.value = updated
        showEdit.value = false
    } catch (err) {
        editError.value = err.message
    } finally {
        saving.value = false
    }
}
</script>

<style scoped>
.profile {
    padding-top: 50px;
    padding-bottom: 80px;
    color: #bfbfcc;
}

.page_label_container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Logout */
.btn-logout {
    background: #f84e4e;
    border: 1px solid #2a2a42;
    color: white;
    height: 28px;
    border-radius: 8px;
    display: flex;
    gap: 5px;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex-shrink: 0;
    transition: color 0.2s, border-color 0.2s;
}

.btn-logout .mdi {
    font-size: 14px;
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

.profile-card {
    display: flex;
    gap: 10px;
}

.adventurer-avatar, .avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
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

/* Modal */
.modal-overlay {
    width: 100%;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: flex-end;
    z-index: 100;
}

.modal {
    background: #111128;
    border: 1px solid #2a2a42;
    border-radius: 24px 24px 0 0;
    padding: 1.5rem;
    width: 100%;
}

.modal h2 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 1rem;
}

.field {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 10px;
}

.field label {
    font-size: 11px;
    font-weight: 600;
    color: #8888aa;
}

.field input,
.field textarea {
    background: #0d0d1a;
    border: 1px solid #2a2a42;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 13px;
    color: #fff;
    outline: none;
}

.field input:focus,
.field textarea:focus {
    border-color: #3d2fff;
}

.form-error {
    font-size: 12px;
    color: #ef4444;
    margin-bottom: 8px;
}

.modal_actions {
    display: flex;
    gap: 8px;
    margin-top: 1rem;
}

.btn-cancel {
    flex: 1;
    background: #1a1a2e;
    border: none;
    color: #8888aa;
    font-size: 13px;
    font-weight: 600;
    padding: 11px;
    border-radius: 12px;
    cursor: pointer;
}

.btn-submit {
    flex: 2;
    background: #3d2fff;
    border: none;
    color: #fff;
    font-size: 13px;
    font-weight: 600;
    padding: 11px;
    border-radius: 12px;
    cursor: pointer;
}

.btn-submit:disabled {
    opacity: 0.6;
}

.avatar-picker {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 4px;
}

.avatar-option {
    background: #0d0d1a;
    border: 2px solid #2a2a42;
    border-radius: 10px;
    padding: 6px;
    cursor: pointer;
    transition: border-color 0.15s;
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar-option img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}

.avatar-option--selected {
    border-color: #3d2fff;
    background: #1a1040;
}

.avatar-option:hover:not(.avatar-option--selected) {
    border-color: #5a5a7a;
}
</style>
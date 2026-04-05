<template>
    <HeaderView />
    <div class="quests-page">
        <div class="quests-page_header">
            <div class="quests-page_label">QUESTS</div>
            <h1>Quest Board</h1>
            <p>Manage and track your quests</p>
        </div>

        <div class="quests-page_toolbar">
            <button class="btn-new" @click="showCreate = true">+ New Quest</button>
        </div>

        <!Filter tabs -->
        <div class="filter-tabs">
            <button v-for="tab in tabs" :key="tab.value" class="filter-tab"
                :class="{ 'filter-tab--active': activeTab === tab.value }" @click="activeTab = tab.value">
                {{ tab.label }}
            </button>
        </div>

        <!States -->
        <div v-if="loading" class="quests-page_loading">Loading quests...</div>
        <div v-else-if="error" class="quests-page_error">{{ error }}</div>

        <!Quest list -->
        <div v-else class="quest-list">
            <div v-for="quest in filteredQuests" :key="quest.id" class="quest-item" @click="openDetails(quest)">
                <div class="quest-item_info">
                    <div class="quest-item_name">{{ quest.name }}</div>
                    <div class="quest-item_tags">
                        <span class="tag" :class="`tag--${quest.status}`">{{ formatStatus(quest.status) }}</span>
                        <span class="tag" :class="`tag--${quest.priority}`">{{ quest.priority }}</span>
                    </div>
                </div>
                <div class="quest-item_xp">
                    <span>+{{ quest.xp_reward }} XP</span>
                </div>
                <span v-if="isOverdue(quest)" class="overdue-badge">Overdue</span>
            </div>

            <div v-if="filteredQuests.length === 0" class="quests-page_empty">
                No quests here. <button class="link-btn" @click="showCreate = true">Create one!</button>
            </div>
        </div>

        <!XP / level-up toast -->
        <Transition name="toast">
            <div v-if="toast" class="toast" :class="{ 'toast--levelup': toast.leveledUp }">
                <span v-if="toast.leveledUp">🎉 Level up! You're now level {{ toast.newLevel }}</span>
                <span v-else>+{{ toast.xpGained }} XP earned!</span>
                <span v-if="toast.achievements.length" class="toast_achievements">
                    🏆 {{ toast.achievements.join(', ') }}
                </span>
            </div>
        </Transition>
    </div>

    <!Create Quest Modal -->
    <Teleport to="body">
        <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
            <div class="modal">
                <h2>New Quest</h2>
                <form @submit.prevent="createQuest">
                    <div class="field">
                        <label>Title</label>
                        <input v-model="newQuest.name" type="text" placeholder="What's your quest?" required />
                    </div>
                    <div class="field">
                        <label>Description (optional)</label>
                        <textarea v-model="newQuest.description" placeholder="Details..." rows="2"></textarea>
                    </div>
                    <div class="field-row">
                        <div class="field">
                            <label>Difficulty</label>
                            <select v-model="newQuest.difficulty">
                                <option value="easy">Easy (10 XP)</option>
                                <option value="medium">Medium (50 XP)</option>
                                <option value="hard">Hard (100 XP)</option>
                                <option value="legendary">Legendary (250 XP)</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>Priority</label>
                            <select v-model="newQuest.priority">
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>
                    </div>
                    <div class="field">
                        <label>Due Date (optional)</label>
                        <input v-model="newQuest.due_date" type="date" :min="today" />
                    </div>
                    <div v-if="createError" class="form-error">{{ createError }}</div>
                    <div class="modal_actions">
                        <button type="button" class="btn-cancel" @click="showCreate = false">Cancel</button>
                        <button type="submit" class="btn-submit" :disabled="creating">
                            {{ creating ? 'Creating...' : 'Create Quest' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </Teleport>
    <Teleport to="body">
        <div v-if="showDetails" class="modal-overlay" @click.self="showDetails = false">
            <div class="modal">
                <h2>{{ selectedQuest.name }}</h2>
                <p v-if="selectedQuest.description" class="detail-desc">{{ selectedQuest.description }}</p>
                <p v-if="selectedQuest.due_date" class="detail-due">{{ selectedQuest.due_date }}</p>

                <div class="detail-row">
                    <span class="tag" :class="`tag--${selectedQuest.status}`">{{ formatStatus(selectedQuest.status) }}</span>
                    <span class="tag" :class="`tag--${selectedQuest.priority}`">{{ selectedQuest.priority }}</span>
                </div>

                <div class="detail-row">
                    <div class="quest-item_xp" style="margin-top: 10px; width: fit-content;">
                        <span>+{{ selectedQuest.xp_reward }} XP</span>
                    </div>
                    <div class="quest-item_energy" style="margin-top: 10px; width: fit-content;">
                        <span>-{{ selectedQuest.energy_cost }} Energy</span>
                    </div>
                </div>
                

                <div class="modal_actions" style="margin-top: 1.5rem;">
                    <button class="btn-cancel" @click="showDetails = false">Close</button>
                    <button
                        v-if="selectedQuest.status === 'pending'"
                        class="btn-submit"
                        @click="startQuest(selectedQuest.id); showDetails = false">
                        Start Quest
                    </button>
                    <button
                        v-if="selectedQuest.status === 'in_progress'"
                        class="btn-submit"
                        @click="completeQuest(selectedQuest.id); showDetails = false">
                        Complete Quest
                    </button>
                </div>
            </div>
        </div>
    </Teleport>
    <NavView />
    <ModalAlert :visible="modalVisible" :title="modalTitle" :message="modalMessage" :type="modalType"
        @close="modalVisible = false" />
</template>

<script setup>
definePageMeta({ middleware: 'auth' })
import { ref, computed, onMounted } from 'vue'
import api from '@/services/questService'

// Tabs

const tabs = [
    { label: 'All', value: 'all' },
    { label: 'Pending', value: 'pending' },
    { label: 'In Progress', value: 'in_progress' },
    { label: 'Completed', value: 'completed' },
]

const activeTab = ref('pending')

// State

const quests = ref([])
const loading = ref(false)
const error = ref(null)
const actionLoading = ref(null)   // holds the quest id currently being acted on
const toast = ref(null)
let toastTimer = null

// Tasks
const showDetails = ref(false)
const selectedQuest = ref(null)

function openDetails(quest) {
    selectedQuest.value = quest
    showDetails.value = true
}

// Fetch quests from backend

async function fetchQuests() {
    loading.value = true
    error.value = null
    try {
        quests.value = await api.quests.list()
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

onMounted(fetchQuests)

// Filter

const filteredQuests = computed(() => {
    if (activeTab.value === 'all') return quests.value
    return quests.value.filter(q => q.status === activeTab.value)
})

// Helpers

function formatStatus(status) {
    const map = {
        pending: 'Pending',
        in_progress: 'In Progress',
        completed: 'Completed',
        failed: 'Failed',
        abandoned: 'Abandoned',
    }
    return map[status] ?? status
}

function showToast(data) {
    clearTimeout(toastTimer)
    toast.value = data
    toastTimer = setTimeout(() => { toast.value = null }, 3500)
}

// Actions

async function startQuest(id) {
    actionLoading.value = id
    try {
        const updated = await api.quests.start(id)
        const idx = quests.value.findIndex(q => q.id === id)
        if (idx !== -1) quests.value[idx] = updated
    } catch (err) {
        showModal('Cannot Start Quest', err.message, 'error')
    } finally {
        actionLoading.value = null
    }
}

async function completeQuest(id) {
    actionLoading.value = id
    try {
        const result = await api.quests.complete(id)
        // result: { quest, xp_gained, leveled_up, new_level, achievements_unlocked }

        const idx = quests.value.findIndex(q => q.id === id)
        if (idx !== -1) quests.value[idx] = result.quest

        showToast({
            xpGained: result.xp_gained,
            leveledUp: result.leveled_up,
            newLevel: result.new_level,
            achievements: result.achievements_unlocked,
        })
    } catch (err) {
        showModal(err.message)
    } finally {
        actionLoading.value = null
    }
}

// Create quest

const showCreate = ref(false)
const creating = ref(false)
const createError = ref(null)

const newQuest = ref({
    name: '',
    description: '',
    difficulty: 'easy',
    priority: 'medium',
    due_date: '',
})

const today = new Date().toISOString().split('T')[0]

async function createQuest() {
    creating.value = true
    createError.value = null
    try {
        const payload = { ...newQuest.value }
        if (!payload.due_date) delete payload.due_date
        if (!payload.description) delete payload.description

        const created = await api.quests.create(payload)
        quests.value.unshift(created)   // add to top of list

        newQuest.value = { name: '', description: '', difficulty: 'easy', priority: 'medium', due_date: '' }
        showCreate.value = false
    } catch (err) {
        createError.value = err.message
    } finally {
        creating.value = false
    }
}

function isOverdue(quest) {
    if (!quest.due_date || quest.status === 'completed') return false
    return new Date(quest.due_date) < new Date()
}

const modalVisible = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')
const modalType = ref('info')

function showModal(title, message, type = 'info') {
    modalTitle.value = title
    modalMessage.value = message
    modalType.value = type
    modalVisible.value = true
}
</script>

<style scoped>
.quests-page {
    padding-top: 50px;
    padding-bottom: 80px;
}

.quests-page_header {
    padding: 16px 16px 8px;
}

.quests-page_label {
    font-size: 10px;
    font-weight: 600;
    color: #3d2fff;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.quests-page_header h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
}

.quests-page_header p {
    font-size: 11px;
    color: #5a5a7a;
    margin-top: 1px;
}

.quests-page_toolbar {
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

.filter-tabs {
    display: flex;
    padding: 0 14px;
    gap: 6px;
    margin-bottom: 10px;
    overflow-x: auto;
}

.filter-tab {
    font-size: 12px;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 20px;
    border: none;
    background: transparent;
    color: #5a5a7a;
    cursor: pointer;
    white-space: nowrap;
}

.filter-tab--active {
    background: #1a1a2e;
    color: #fff;
}

.quests-page_loading,
.quests-page_error,
.quests-page_empty {
    text-align: center;
    padding: 2rem;
    color: #5a5a7a;
    font-size: 13px;
}

.quests-page_error {
    color: #ef4444;
}

.link-btn {
    background: none;
    border: none;
    color: #3d2fff;
    font-size: 13px;
    cursor: pointer;
    font-weight: 600;
}

.quest-list {
    padding: 0 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.quest-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 12px;
    background: #111128;
    border: 1px solid #1e1e38;
    border-radius: 12px;
}

.quest-item_info {
    flex: 1;
    min-width: 0;
}

.quest-item_name {
    font-size: 13px;
    font-weight: 500;
    color: #d0d0e8;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.quest-item_tags {
    display: flex;
    gap: 4px;
    margin-top: 4px;
    flex-wrap: wrap;
}

.tag {
    font-size: 10px;
    padding: 1px 7px;
    border-radius: 10px;
    font-weight: 500;
    text-transform: capitalize;
}

.tag--completed {
    background: #0a2318;
    color: #22c55e;
}

.tag--in_progress {
    background: #1f1200;
    color: #f59e0b;
}

.tag--pending {
    background: #151520;
    color: #70708d;
}

.tag--failed {
    background: #1f0a0a;
    color: #ef4444;
}

.tag--abandoned {
    background: #1a1a1a;
    color: #888;
}

.tag--high {
    background: #1f0a0a;
    color: #ef4444;
}

.tag--medium {
    background: #1a1a00;
    color: #eab308;
}

.tag--low {
    background: #0a1a0a;
    color: #4ade80;
}

.quest-item_xp, .quest-item_energy {
    background: #1a0e3a;
    border: 1px solid #2d1f5a;
    border-radius: 8px;
    padding: 4px 8px;
    display: flex;
    align-items: center;
    gap: 3px;
    flex-shrink: 0;
}

.quest-item_xp span {
    font-size: 11px;
    font-weight: 700;
    color: #a78bfa;
}

.quest-item_energy {
    font-size: 11px;
    font-weight: 700;
    color: #6739f1;
}

.overdue-badge {
    background: #1a0e3a;
    color: rgb(228, 8, 8);
    font-size: 11px;
    padding: 4px 8px;
    border: 1px solid #2d1f5a;
    border-radius: 8px;
}

/* Toast */
.toast {
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    background: #1a0e3a;
    border: 1px solid #2d1f5a;
    color: #a78bfa;
    font-size: 13px;
    font-weight: 600;
    padding: 10px 20px;
    border-radius: 20px;
    z-index: 200;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
}

.toast--levelup {
    background: #1a2e0e;
    border-color: #2d5a1f;
    color: #22c55e;
}

.toast_achievements {
    font-size: 11px;
    color: #f59e0b;
}

.toast-enter-active,
.toast-leave-active {
    transition: opacity 0.3s, transform 0.3s;
}

.toast-enter-from,
.toast-leave-to {
    opacity: 0;
    transform: translateX(-50%) translateY(10px);
}

/* Modal */
.modal-overlay {
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
.field textarea,
.field select {
    background: #0d0d1a;
    border: 1px solid #2a2a42;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 13px;
    color: #fff;
    outline: none;
}

.field input:focus,
.field textarea:focus,
.field select:focus {
    border-color: #3d2fff;
}

.field-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
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

.modal-overlay p {
    color: #585f58;
    font-size: small;
}

.detail-row {
    display: flex;
    gap: 5px;
}
</style>
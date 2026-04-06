<template>
    <HeaderView />
    <div class="settings">
        <div class="settings-page_header">
            <div class="settings-page_label">SETTINGS</div>
            <h1>Configuration</h1>
            <p>Manage your app preferences</p>
        </div>
        <div class="sett-wrapper">
            <div class="settings-grid">

                <div class="settings-card">
                    <div class="card-header">
                        <div class="card-header_left">
                            <i class="mdi mdi-bell-outline setting-icon"></i>
                        </div>
                        <div class="card-header_right">
                            <h3>Notifications</h3>
                            <p>Manage your Notification preferences</p>
                        </div>
                    </div>
                    <div class="card-toggles">
                        <div class="setting-toggle">
                            <div>Email Notification</div>
                            <i class="mdi mdi-toggle-switch-off-outline toggle"></i>
                        </div>
                        <div class="setting-toggle">
                            <div>Push Notification</div>
                            <i class="mdi mdi-toggle-switch-off-outline toggle"></i>
                        </div>
                        <div class="setting-toggle">
                            <div>Task Reminders</div>
                            <i class="mdi mdi-toggle-switch-off-outline toggle"></i>
                        </div>
                    </div>
                </div>

                <div class="settings-card">
                    <div class="card-header">
                        <div class="card-header_left">
                            <i class="mdi mdi-palette-outline setting-icon"></i>
                        </div>
                        <div class="card-header_right">
                            <h3>Appearance</h3>
                            <p>Customize the look and feel</p>
                        </div>
                    </div>
                    <div class="card-toggles">
                        <div class="setting-toggle">
                            <div>Dark Mode</div>
                            <i class="mdi mdi-toggle-switch-off-outline toggle"></i>
                        </div>
                        <div class="setting-toggle">
                            <div>Compact View</div>
                            <i class="mdi mdi-toggle-switch-off-outline toggle"></i>
                        </div>
                    </div>
                </div>

                <div class="settings-card">
                    <div class="card-header">
                        <div class="card-header_left">
                            <i class="mdi mdi-account-alert-outline setting-icon"></i>
                        </div>
                        <div class="card-header_right">
                            <h3>Account</h3>
                            <p>Manage your account</p>
                        </div>
                    </div>
                    <div class="card-toggles">
                        <div class="setting-toggle clickable" @click="showPasswordModal = true">
                            <div>Change Password</div>
                            <i class="mdi mdi-chevron-right"></i>
                        </div>
                        <div class="setting-toggle clickable danger" @click="showDeleteModal = true">
                            <div>Delete Account</div>
                            <i class="mdi mdi-chevron-right"></i>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
    <NavView />

    <!-- Change Password Modal -->
    <Teleport to="body">
        <div v-if="showPasswordModal" class="modal-overlay" @click.self="closePasswordModal">
            <div class="modal">
                <h2>Change Password</h2>
                <p>Enter your current password and choose a new one.</p>
                <div class="field">
                    <label>Current Password</label>
                    <input v-model="pwForm.current" type="password" placeholder="••••••••" />
                </div>
                <div class="field">
                    <label>New Password</label>
                    <input v-model="pwForm.new" type="password" placeholder="Min. 8 characters" />
                </div>
                <div class="field">
                    <label>Confirm New Password</label>
                    <input v-model="pwForm.confirm" type="password" placeholder="Re-enter new password" />
                </div>
                <p v-if="pwError" class="error-msg">{{ pwError }}</p>
                <p v-if="pwSuccess" class="success-msg">Password changed successfully!</p>
                <div class="modal-actions">
                    <button class="btn-cancel" @click="closePasswordModal">Cancel</button>
                    <button class="btn-confirm" :disabled="pwLoading" @click="handleChangePassword">
                        {{ pwLoading ? 'Saving...' : 'Save' }}
                    </button>
                </div>
            </div>
        </div>
    </Teleport>

    <!-- Delete Account Modal -->
    <Teleport to="body">
        <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
            <div class="modal">
                <h2 class="danger-title">Delete Account</h2>
                <p>This is <strong>permanent</strong>. All your quests, XP, and progress will be erased. Enter your
                    password to confirm.</p>
                <div class="field">
                    <label>Password</label>
                    <input v-model="deletePassword" type="password" placeholder="••••••••" />
                </div>
                <p v-if="deleteError" class="error-msg">{{ deleteError }}</p>
                <div class="modal-actions">
                    <button class="btn-cancel" @click="closeDeleteModal">Cancel</button>
                    <button class="btn-danger" :disabled="deleteLoading" @click="handleDeleteAccount">
                        {{ deleteLoading ? 'Deleting...' : 'Delete My Account' }}
                    </button>
                </div>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import questService from '~/services/questService'

const router = useRouter()

// --- Change Password ---
const showPasswordModal = ref(false)
const pwForm = ref({ current: '', new: '', confirm: '' })
const pwError = ref('')
const pwSuccess = ref(false)
const pwLoading = ref(false)

function closePasswordModal() {
    showPasswordModal.value = false
    pwForm.value = { current: '', new: '', confirm: '' }
    pwError.value = ''
    pwSuccess.value = false
}

async function handleChangePassword() {
    pwError.value = ''
    pwSuccess.value = false

    if (!pwForm.value.current || !pwForm.value.new || !pwForm.value.confirm) {
        pwError.value = 'All fields are required.'
        return
    }
    if (pwForm.value.new !== pwForm.value.confirm) {
        pwError.value = 'New passwords do not match.'
        return
    }
    if (pwForm.value.new.length < 8) {
        pwError.value = 'New password must be at least 8 characters.'
        return
    }

    pwLoading.value = true
    try {
        await questService.players.changePassword(pwForm.value.current, pwForm.value.new)
        pwSuccess.value = true
        setTimeout(closePasswordModal, 1500)
    } catch (err) {
        pwError.value = err.message || 'Something went wrong.'
    } finally {
        pwLoading.value = false
    }
}

// --- Delete Account ---
const showDeleteModal = ref(false)
const deletePassword = ref('')
const deleteError = ref('')
const deleteLoading = ref(false)

function closeDeleteModal() {
    showDeleteModal.value = false
    deletePassword.value = ''
    deleteError.value = ''
}

async function handleDeleteAccount() {
    deleteError.value = ''
    if (!deletePassword.value) {
        deleteError.value = 'Please enter your password.'
        return
    }

    deleteLoading.value = true
    try {
        await questService.players.deleteAccount(deletePassword.value)
        questService.auth.logout()
        router.push('/LoginView')
    } catch (err) {
        deleteError.value = err.message || 'Something went wrong.'
    } finally {
        deleteLoading.value = false
    }
}
</script>

<style scoped>
.settings {
    padding-top: 50px;
    padding-bottom: 80px;
    color: #bfbfcc;
}

.settings-page_header {
    padding: 16px 16px 8px;
}

.settings-page_label {
    font-size: 10px;
    font-weight: 600;
    color: #3d2fff;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.settings-page_header h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
}

.settings-page_header p {
    font-size: 11px;
    color: #5a5a7a;
    margin-top: 1px;
}

.settings-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
    padding: 0 14px 12px;
}

.settings-card {
    background: #1f1f3d;
    border-radius: 14px;
    padding: 14px;
    font-size: small;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgba(126, 126, 126, 0.5);
    margin-bottom: 10px;
}

.card-header h3,
.card-header p {
    margin: 0;
    padding: 0;
}

.setting-icon {
    font-size: 26px;
}

.setting-toggle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
}

.setting-toggle.clickable {
    cursor: pointer;
    border-radius: 8px;
    padding: 6px 4px;
    transition: background 0.15s;
}

.setting-toggle.clickable:hover {
    background: rgba(255, 255, 255, 0.05);
}

.setting-toggle.danger {
    color: #ff4d4d;
}

.toggle {
    font-size: 24px;
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

    padding: 24px;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
    color: #bfbfcc;
}

.modal h2 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #fff;
    margin: 0;
}

.modal p {
    font-size: 13px;
    margin: 0;
}

.danger-title {
    color: #ff4d4d;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.field label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #7a7a9a;
    text-transform: uppercase;
}

.field input {
    background: #12122a;
    border: 1px solid #2e2e5e;
    border-radius: 8px;
    padding: 10px 12px;
    color: #fff;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
}

.field input:focus {
    border-color: #3d2fff;
}

.error-msg {
    color: #ff4d4d;
    font-size: 12px;
    margin: 0;
}

.success-msg {
    color: #4dff91;
    font-size: 12px;
    margin: 0;
}

.modal-actions {
    display: flex;
    gap: 10px;
    margin-top: 4px;
}

.btn-cancel,
.btn-confirm,
.btn-danger {
    flex: 1;
    padding: 10px;
    border-radius: 8px;
    border: none;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
}

.btn-cancel {
    background: #2e2e5e;
    color: #bfbfcc;
}

.btn-confirm {
    background: #3d2fff;
    color: #fff;
}

.btn-danger {
    background: #ff4d4d;
    color: #fff;
}

.btn-cancel:hover,
.btn-confirm:hover,
.btn-danger:hover {
    opacity: 0.85;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>
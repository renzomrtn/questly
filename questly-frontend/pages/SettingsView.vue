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
                            <i class="mdi mdi-bell-outline"></i>
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
                            <i class="mdi mdi-palette-outline"></i>
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
                            <i class="mdi mdi-account-alert-outline"></i>
                        </div>
                        <div class="card-header_right">
                            <h3>Account</h3>
                            <p>Manage your account</p>
                        </div>
                    </div>
                    <div class="card-toggles">
                        <div class="setting-toggle">
                            <div>Change Password</div>
                        </div>
                        <div class="setting-toggle">
                            <div>Delete Account</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <NavView />
</template>
<script setup>
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
    display: flex;
    font-size: small;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgb(126, 126, 126, 0.5);
    margin-bottom: 10px;
}

.card-header h3, .card-header p {
    margin: 0;
    padding: 0;
}

.setting-toggle {
    display: flex;
    justify-content: space-between;
}

</style>
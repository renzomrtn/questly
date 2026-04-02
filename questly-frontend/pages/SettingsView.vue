<template>
    <HeaderView />
    <div class="settings">
        <div class="settings-page_header">
            <div class="settings-page_label">SETTINGS</div>
            <h1>Configuration</h1>
            <p>Manage your app preferences</p>
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
</style>
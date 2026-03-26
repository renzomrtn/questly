<template>
    <Teleport to="body">
        <div v-if="visible" class="modal-overlay" @click.self="close">
            <div class="modal">
                <div class="modal-icon" :class="typeClass">
                    <i :class="`mdi mdi-${icon}`"></i>
                </div>
                <div class="modal-body">
                    <div class="modal-title">{{ title }}</div>
                    <div class="modal-message">{{ message }}</div>
                </div>
                <button class="modal-btn" @click="close">Got it</button>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    visible: Boolean,
    title: { type: String, default: 'Notice' },
    message: { type: String, default: '' },
    type: { type: String, default: 'info' }, // 'info' | 'error' | 'success'
})

const emit = defineEmits(['close'])

function close() {
    emit('close')
}

const typeClass = computed(() => ({
    'modal-icon--error': props.type === 'error',
    'modal-icon--success': props.type === 'success',
    'modal-icon--info': props.type === 'info',
}))

const icon = computed(() => ({
    error: 'alert-circle-outline',
    success: 'check-circle-outline',
    info: 'information-outline',
}[props.type] ?? 'information-outline'))
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
    padding: 24px;
}

.modal {
    background: #1f1f3d;
    border: 1px solid #2a2a55;
    border-radius: 18px;
    padding: 24px 20px 20px;
    width: 100%;
    max-width: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    text-align: center;
}

.modal-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.modal-icon--error {
    background: #2a0a0a;
    color: #ef4444;
}

.modal-icon--success {
    background: #0a2318;
    color: #22c55e;
}

.modal-icon--info {
    background: #0e1a40;
    color: #3d2fff;
}

.modal-body {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.modal-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #fff;
}

.modal-message {
    font-size: 13px;
    color: #8888aa;
    line-height: 1.5;
}

.modal-btn {
    width: 100%;
    background: #3d2fff;
    color: #fff;
    border: none;
    border-radius: 12px;
    padding: 11px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 4px;
}
</style>
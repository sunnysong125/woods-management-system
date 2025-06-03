<template>
  <div class="user-menu">
    <el-dropdown v-if="isAuthenticated" trigger="click">
      <span class="el-dropdown-link">
        <el-avatar :size="28" :icon="UserFilled" class="user-avatar" />
        <span class="username">{{ displayUsername }}</span>
        <el-icon class="el-icon--right">
          <arrow-down />
        </el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item v-if="isAdmin" @click="handleAdminPanel">
            <el-icon><Setting /></el-icon>
            <span>管理員面板</span>
          </el-dropdown-item>
          <el-dropdown-item divided @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            <span>登出</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-button v-else type="success" size="small" @click="handleLogin">登入</el-button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  UserFilled,
  Setting,
  SwitchButton,
  ArrowDown
} from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()

const isAuthenticated = computed(() => store.state.isAuthenticated)
const isAdmin = computed(() => store.state.isAdmin)
const userInfo = computed(() => store.state.user)
const displayUsername = computed(() => {
  const user = store.state.user
  return user ? user.username : ''
})

const handleLogin = () => {
  router.push('/login')
}

const handleAdminPanel = () => {
  router.push('/admin')
}

const handleLogout = async () => {
  try {
    await store.dispatch('logout')
    ElMessage.success('已成功登出')
    router.push('/login')
  } catch (error) {
    ElMessage.error('登出時發生錯誤')
  }
}
</script>

<style scoped>
.user-menu {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0;
  margin: 0;
  background: none;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #fff;
  font-size: 14px;
  padding: 0;
  background: none;
}

.user-avatar {
  margin-right: 8px;
  background-color: var(--el-color-success);
}

.username {
  margin-right: 4px;
  color: var(--el-color-success);
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-button) {
  background-color: var(--el-color-success);
  border-color: var(--el-color-success);
  margin: 0;
  padding: 8px 16px;
}

:deep(.el-button:hover) {
  background-color: var(--el-color-success-light-3);
  border-color: var(--el-color-success-light-3);
}
</style> 
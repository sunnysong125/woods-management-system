<template>
  <div class="navbar">
    <div class="navbar-logo">
      <h1>WoodDB</h1>
    </div>
    <div class="navbar-menu">
      <router-link to="/" class="navbar-item">首頁</router-link>
      <router-link to="/trees" class="navbar-item">樹木數據</router-link>
      <router-link to="/query" class="navbar-item">數據查詢</router-link>
      <router-link v-if="isAuthenticated" to="/upload" class="navbar-item">數據上傳</router-link>
    </div>
    <div class="navbar-user">
      <template v-if="isAuthenticated">
        <el-dropdown trigger="click" @command="handleCommand">
          <span class="user-dropdown">
            <el-avatar :size="32" :src="userAvatar">{{ userInitials }}</el-avatar>
            <span class="user-name">{{ userName }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">個人資料</el-dropdown-item>
              <el-dropdown-item command="logout" divided>登出</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template v-else>
        <router-link to="/login">
          <el-button type="primary" size="small">登錄</el-button>
        </router-link>
      </template>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'NavBar',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // 是否已登錄
    const isAuthenticated = computed(() => store.state.isAuthenticated)
    
    // 用戶名稱
    const userName = computed(() => {
      if (store.state.user) {
        return store.state.user.username
      }
      return ''
    })
    
    // 用戶頭像
    const userAvatar = computed(() => {
      if (store.state.user && store.state.user.avatar) {
        return store.state.user.avatar
      }
      return ''
    })
    
    // 用戶名稱首字母
    const userInitials = computed(() => {
      if (userName.value) {
        return userName.value.charAt(0).toUpperCase()
      }
      return ''
    })
    
    // 處理下拉菜單命令
    const handleCommand = async (command) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'logout':
          try {
            await store.dispatch('logout')
            ElMessage.success('登出成功')
            router.push('/login')
          } catch (error) {
            ElMessage.error('登出失敗，請稍後再試')
          }
          break
      }
    }
    
    return {
      isAuthenticated,
      userName,
      userAvatar,
      userInitials,
      handleCommand
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
  background-color: rgba(46, 139, 87, 0.8);
  color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.navbar-logo {
  display: flex;
  align-items: center;
}

.logo-image {
  height: 40px;
  margin-right: 10px;
}

h1 {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.navbar-item {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar-item:hover,
.navbar-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-dropdown:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-name {
  font-weight: 500;
  color: #fff;
}

:deep(.el-dropdown-menu) {
  background-color: rgba(30, 30, 30, 0.9) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-dropdown-menu__item) {
  color: #fff !important;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

:deep(.el-dropdown-menu__item.is-disabled) {
  color: rgba(255, 255, 255, 0.5) !important;
}
</style> 
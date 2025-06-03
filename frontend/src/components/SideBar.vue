<template>
  <div class="sidebar">
    <div class="logo" @click="$router.push('/')">
      <div class="p-icon">森</div>
    </div>
    <div class="menu-items">
      <div class="menu-item" @click="$router.push('/')">
        <el-icon><House /></el-icon>
      </div>
      <div class="menu-item" @click="$router.push('/upload')">
        <el-icon><Upload /></el-icon>
      </div>
      <div class="menu-item" @click="$router.push('/query')">
        <el-icon><Search /></el-icon>
      </div>
      <div class="menu-item" @click="$router.push('/projects')">
        <el-icon><Grid /></el-icon>
      </div>
      <div class="menu-item" @click="$router.push('/about')">
        <el-icon><Setting /></el-icon>
      </div>
    </div>
    <div class="bottom-items">
      <div class="menu-item" @click="$router.push('/about')">
        <el-icon><QuestionFilled /></el-icon>
      </div>
      <div class="menu-item" @click="$router.push('/about')">
        <el-icon><InfoFilled /></el-icon>
      </div>
      <div class="menu-item" v-if="!isAuthenticated" @click="$router.push('/login')">
        <el-icon><User /></el-icon>
      </div>
      <div class="menu-item" v-if="isAuthenticated" @click="handleLogout">
        <el-tooltip content="登出" placement="right">
          <el-icon><SwitchButton /></el-icon>
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script>
import { House, Upload, Search, Grid, Setting, QuestionFilled, InfoFilled, User, SwitchButton } from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'SideBar',
  components: {
    House, Upload, Search, Grid, Setting, QuestionFilled, InfoFilled, User, SwitchButton
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    
    const handleLogout = async () => {
      await store.dispatch('logout')
      router.push('/login')
    }
    
    return {
      isAuthenticated,
      handleLogout
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 60px;
  height: 100vh;
  background-color: #1e1e1e;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.logo {
  padding: 20px 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.p-icon {
  width: 30px;
  height: 30px;
  background-color: #2E8B57;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
  font-weight: bold;
  font-size: 14px;
}

.menu-items {
  display: flex;
  flex-direction: column;
  width: 100%;
  flex: 1;
}

.menu-item {
  width: 100%;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #888;
  cursor: pointer;
  transition: all 0.3s ease;
}

.menu-item:hover {
  color: #2E8B57;
  background-color: rgba(46, 139, 87, 0.1);
}

.bottom-items {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 20px;
}

.el-icon {
  font-size: 18px;
}
</style> 
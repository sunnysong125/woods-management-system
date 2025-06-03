import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // 路由懶加載
    component: () => import('@/views/AboutView.vue')
  },
  {
    path: '/upload',
    name: 'upload',
    component: () => import('@/views/UploadView.vue'),
    meta: {
      requiresAuth: true // 需要登錄才能訪問
    }
  },
  {
    path: '/query',
    name: 'query',
    component: () => import('@/views/QueryView.vue')
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/views/ProjectsView.vue')
  },
  {
    path: '/trees',
    name: 'trees',
    component: () => import('@/views/TreesView.vue'),
    props: (route) => ({ projectId: parseInt(route.query.projectId) || null }),
    meta: {
      requiresAuth: true // 需要登錄才能訪問
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  }
]

// 直接使用固定的基礎URL
const baseUrl = '/woodsfrond/'

const router = createRouter({
  history: createWebHistory(baseUrl),
  routes
})

// 添加全局導航守衛
router.beforeEach((to, from, next) => {
  // 檢查訪問的頁面是否需要登入
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 如果需要登入但未登入，重定向到登入頁面
    if (!store.getters.isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 保存原始要訪問的頁面路徑
      })
    } else {
      next() // 已登入，允許訪問
    }
  } else {
    next() // 不需要登入，允許訪問
  }
})

export default router 
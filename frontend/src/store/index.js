import { createStore } from 'vuex'
import axios from '@/utils/axios'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    files: []
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    token: state => state.token,
    files: state => state.files
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },
    
    SET_TOKEN(state, token) {
      state.token = token
      state.isAuthenticated = !!token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    
    CLEAR_AUTH(state) {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
    
    SET_FILES(state, files) {
      state.files = files
    },
    
    ADD_FILE(state, file) {
      state.files.push(file)
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        console.log('開始登入流程...')
        
        // 首先獲取CSRF token
        console.log('獲取CSRF token...')
        await axios.get('/api/users/csrf-token/')
        
        // 等待一小段時間確保cookie設置完成
        await new Promise(resolve => setTimeout(resolve, 100))
        
        // 檢查CSRF token是否已設置
        const csrfToken = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1]
        
        console.log('當前CSRF token:', csrfToken)
        console.log('當前Origin:', window.location.origin)
        console.log('當前Host:', window.location.host)
        
        // 然後進行登入
        console.log('發送登入請求...')
        const response = await axios.post('/api/users/login/', credentials)
        
        const { token, user } = response.data
        
        // 設置token和用戶信息
        commit('SET_TOKEN', token)
        commit('SET_USER', user)
        
        // 保存用戶信息到localStorage
        localStorage.setItem('user', JSON.stringify(user))
        
        console.log('登入成功')
        return response.data
      } catch (error) {
        console.error('登入失敗:', error)
        console.error('錯誤詳情:', error.response?.data)
        commit('CLEAR_AUTH')
        throw error
      }
    },
    
    async logout({ commit }) {
      try {
        await axios.post('/api/users/logout/')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        commit('CLEAR_AUTH')
      }
    },
    
    async checkAuth({ commit, state }) {
      if (!state.token) {
        return false
      }
      
      try {
        const response = await axios.get('/api/users/current-user/')
        commit('SET_USER', response.data)
        return true
      } catch (error) {
        commit('CLEAR_AUTH')
        return false
      }
    },
    
    async fetchFiles({ commit }) {
      try {
        const response = await axios.get('/api/csv/')
        commit('SET_FILES', response.data)
        return response.data
      } catch (error) {
        console.error('獲取文件列表失敗:', error)
        return []
      }
    }
  },
  modules: {
  }
}) 
import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token') || '',
    isAuthenticated: !!localStorage.getItem('token'),
    files: []
  },
  getters: {
    isAuthenticated: state => !!state.token,
    user: state => state.user,
    files: state => state.files
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      state.isAuthenticated = true
      localStorage.setItem('token', token)
      // 設置 axios 默認 headers
      axios.defaults.headers.common['Authorization'] = `Token ${token}`
    },
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = true
      localStorage.setItem('user', JSON.stringify(user))
    },
    LOGOUT(state) {
      state.token = ''
      state.user = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 清除 axios 默認 headers
      delete axios.defaults.headers.common['Authorization']
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
        const response = await axios.post('/api/users/login/', credentials)
        const { user, token } = response.data
        
        // 更新 state
        commit('SET_TOKEN', token)
        commit('SET_USER', user)
        
        return response.data
      } catch (error) {
        console.error('登錄錯誤:', error)
        throw error
      }
    },
    
    async register({ commit }, userData) {
      try {
        const response = await axios.post('/api/users/register/', userData)
        const { user, token } = response.data
        
        // 更新 state
        commit('SET_TOKEN', token)
        commit('SET_USER', user)
        
        return response.data
      } catch (error) {
        console.error('註冊錯誤:', error)
        throw error
      }
    },
    
    async logout({ commit }) {
      try {
        await axios.post('/api/users/logout/')
      } catch (error) {
        console.error('登出錯誤:', error)
      } finally {
        commit('LOGOUT')
      }
    },
    
    async checkAuth({ commit, state }) {
      const token = localStorage.getItem('token')
      const user = JSON.parse(localStorage.getItem('user') || 'null')
      
      if (token && user) {
        // 設置 axios 默認 headers
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        
        try {
          // 驗證 token 是否有效
          const response = await axios.get('/api/users/current-user/')
          commit('SET_TOKEN', token)
          commit('SET_USER', response.data)
        } catch (error) {
          // token 無效，清除所有狀態
          commit('LOGOUT')
        }
      } else {
        // 如果沒有 token 但狀態中仍有用戶，則清除
        if (state.isAuthenticated) {
          commit('LOGOUT')
        }
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
import axios from 'axios'

// 設置基礎 URL
axios.defaults.baseURL = 'https://srv.orderble.com.tw/woodsbackend'

// 允許跨域請求攜帶憑證
axios.defaults.withCredentials = true

// 請求攔截器
axios.interceptors.request.use(
  config => {
    // 從 localStorage 獲取 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Token ${token}`
    }
    
    // 從 cookie 中獲取 CSRF 令牌
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1]
    
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 響應攔截器
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 清除本地存儲的認證信息
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 重定向到登錄頁面
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default axios 
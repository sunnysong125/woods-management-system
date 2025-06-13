import axios from 'axios'

// 設置基礎 URL
axios.defaults.baseURL = 'https://srv.orderble.com.tw/woodsbackend'

// 允許跨域請求攜帶憑證
axios.defaults.withCredentials = true

// 獲取CSRF Token的函數
const getCSRFToken = () => {
  // 首先嘗試從cookie獲取
  let csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]
  
  // 如果cookie中沒有，嘗試從meta標籤獲取
  if (!csrfToken) {
    const metaTag = document.querySelector('meta[name="csrf-token"]')
    if (metaTag) {
      csrfToken = metaTag.getAttribute('content')
    }
  }
  
  console.log('獲取到的CSRF Token:', csrfToken)
  return csrfToken
}

// 初始化CSRF Token的函數
const initCSRFToken = async () => {
  try {
    const response = await axios.get('/api/users/csrf-token/')
    console.log('CSRF token初始化成功:', response.data)
    return true
  } catch (error) {
    console.error('CSRF token初始化失敗:', error)
    return false
  }
}

// 請求攔截器
axios.interceptors.request.use(
  config => {
    // 從 localStorage 獲取 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Token ${token}`
    }
    
    // 獲取 CSRF 令牌
    const csrfToken = getCSRFToken()
    
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
    
    // 確保Content-Type正確設置
    if (config.method === 'post' || config.method === 'put' || config.method === 'patch') {
      if (!config.headers['Content-Type'] && !(config.data instanceof FormData)) {
        config.headers['Content-Type'] = 'application/json'
      }
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
      // 檢查當前是否已在登入頁面，避免無限重定向
      if (!window.location.pathname.includes('/login')) {
        // 重定向到正確的登錄頁面路由，而不是直接的URL
        if (window.location.pathname.includes('/woodsfrond/')) {
          window.location.href = '/woodsfrond/login'
        } else {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default axios 
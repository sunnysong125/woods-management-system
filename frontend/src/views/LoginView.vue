<template>
  <div class="login-container">
    <div class="content-box login-card">
      <div class="header">
        <h2>{{ isLogin ? '登錄系統' : '註冊帳號' }}</h2>
      </div>
      
      <!-- 登錄表單 -->
      <el-form v-if="isLogin" :model="loginForm" :rules="loginRules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用戶名" prop="username">
          <el-input v-model="loginForm.username" placeholder="請輸入用戶名"></el-input>
        </el-form-item>
        <el-form-item label="密碼" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="請輸入密碼" @keyup.enter="submitLoginForm"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitLoginForm" :loading="loading">登錄</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 註冊表單 -->
      <el-form v-else :model="registerForm" :rules="registerRules" ref="registerFormRef" label-width="80px">
        <el-form-item label="用戶名" prop="username">
          <el-input v-model="registerForm.username" placeholder="請輸入用戶名"></el-input>
        </el-form-item>
        <el-form-item label="密碼" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="請輸入密碼"></el-input>
        </el-form-item>
        <el-form-item label="確認密碼" prop="password2">
          <el-input v-model="registerForm.password2" type="password" placeholder="請再次輸入密碼"></el-input>
        </el-form-item>
        <el-form-item label="電子郵件" prop="email">
          <el-input v-model="registerForm.email" placeholder="請輸入電子郵件"></el-input>
        </el-form-item>
        <el-form-item label="電話" prop="phone_number">
          <el-input v-model="registerForm.phone_number" placeholder="請輸入電話號碼"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitRegisterForm" :loading="loading">註冊</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 切換按鈕 -->
      <div class="switch-form">
        <el-button type="text" @click="switchForm">
          {{ isLogin ? '沒有帳號？立即註冊' : '已有帳號？立即登錄' }}
        </el-button>
      </div>
      
      <!-- 錯誤提示 -->
      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        @close="errorMessage = ''"
      />
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from '@/utils/axios'

export default {
  name: 'LoginView',
  setup() {
    const store = useStore()
    const router = useRouter()
    const isLogin = ref(true)
    const loading = ref(false)
    const errorMessage = ref('')
    
    // 登錄表單
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    // 註冊表單
    const registerForm = reactive({
      username: '',
      password: '',
      password2: '',
      email: '',
      phone_number: ''
    })
    
    // 登錄表單驗證規則
    const loginRules = {
      username: [
        { required: true, message: '請輸入用戶名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '請輸入密碼', trigger: 'blur' }
      ]
    }
    
    // 註冊表單驗證規則
    const registerRules = {
      username: [
        { required: true, message: '請輸入用戶名', trigger: 'blur' },
        { min: 3, max: 20, message: '用戶名長度應在3-20個字符之間', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '請輸入密碼', trigger: 'blur' },
        { min: 6, message: '密碼長度不能少於6個字符', trigger: 'blur' }
      ],
      password2: [
        { required: true, message: '請再次輸入密碼', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== registerForm.password) {
              callback(new Error('兩次輸入的密碼不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ],
      email: [
        { required: true, message: '請輸入電子郵件', trigger: 'blur' },
        { type: 'email', message: '請輸入正確的電子郵件格式', trigger: 'blur' }
      ],
      phone_number: [
        { pattern: /^[0-9-+()]*$/, message: '請輸入正確的電話號碼格式', trigger: 'blur' }
      ]
    }
    
    const loginFormRef = ref(null)
    const registerFormRef = ref(null)
    
    // 切換表單
    const switchForm = () => {
      isLogin.value = !isLogin.value
      errorMessage.value = ''
    }
    
    // 提交登錄表單
    const submitLoginForm = () => {
      if (!loginFormRef.value) return
      
      loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          errorMessage.value = ''
          
          try {
            console.log('登錄數據:', loginForm) // 添加日誌
            await store.dispatch('login', {
              username: loginForm.username,
              password: loginForm.password
            })
            
            ElMessage.success('登錄成功')
            
            // 獲取查詢參數中的重定向路徑
            const redirectPath = router.currentRoute.value.query.redirect || '/'
            router.push(redirectPath)
          } catch (error) {
            console.error('登錄錯誤:', error.response?.data) // 添加錯誤日誌
            
            // 檢查是否為密碼錯誤或認證失敗
            if (error.response?.status === 400 || error.response?.status === 401) {
              // 顯示彈出視窗而不是跳轉到錯誤頁面
              let errorMsg = '登錄失敗'
              
              if (error.response?.data?.message) {
                errorMsg = error.response.data.message
              } else if (error.response?.data?.detail) {
                errorMsg = error.response.data.detail
              } else if (error.response?.data?.non_field_errors) {
                errorMsg = Array.isArray(error.response.data.non_field_errors) 
                  ? error.response.data.non_field_errors.join(', ')
                  : error.response.data.non_field_errors
              } else if (error.response?.status === 401) {
                errorMsg = '用戶名或密碼錯誤，請重新輸入'
              } else if (error.response?.status === 400) {
                errorMsg = '登錄信息有誤，請檢查用戶名和密碼'
              }
              
              // 使用彈出視窗顯示錯誤
              ElMessageBox.alert(errorMsg, '登錄失敗', {
                confirmButtonText: '確定',
                type: 'error',
                center: true
              })
            } else if (error.response?.data?.message) {
              errorMessage.value = error.response.data.message
            } else if (error.response?.data) {
              // 處理表單驗證錯誤
              const errors = Object.entries(error.response.data)
                .map(([field, messages]) => {
                  const messageArray = Array.isArray(messages) ? messages : [messages]
                  return `${field}: ${messageArray.join(', ')}`
                })
                .join('\n')
              errorMessage.value = errors
            } else {
              errorMessage.value = '登錄失敗，請稍後再試'
            }
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    // 提交註冊表單
    const submitRegisterForm = () => {
      if (!registerFormRef.value) return
      
      registerFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          errorMessage.value = ''
          
          try {
            // 確保包含 password2 字段
            const registerData = {
              ...registerForm,
              password2: registerForm.password // 使用相同的密碼作為確認密碼
            }
            console.log('註冊數據:', registerData) // 添加日誌
            await axios.post('/api/users/register/', registerData)
            ElMessage.success('註冊成功，請登錄')
            isLogin.value = true
          } catch (error) {
            console.error('註冊錯誤:', error.response?.data) // 添加錯誤日誌
            if (error.response?.data?.message) {
              errorMessage.value = error.response.data.message
            } else if (error.response?.data) {
              // 處理表單驗證錯誤
              const errors = Object.entries(error.response.data)
                .map(([field, messages]) => {
                  // 確保 messages 是數組
                  const messageArray = Array.isArray(messages) ? messages : [messages]
                  return `${field}: ${messageArray.join(', ')}`
                })
                .join('\n')
              errorMessage.value = errors
            } else {
              errorMessage.value = '註冊失敗，請稍後再試'
            }
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    return {
      isLogin,
      loginForm,
      registerForm,
      loginRules,
      registerRules,
      loginFormRef,
      registerFormRef,
      loading,
      errorMessage,
      switchForm,
      submitLoginForm,
      submitRegisterForm
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  color: #fff;
}

.login-card {
  width: 400px;
  background-color: rgba(30, 30, 30, 0.5) !important;
  padding: 20px;
  border-radius: 4px;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

h2 {
  color: #ffffff;
  margin: 0;
}

.switch-form {
  text-align: center;
  margin-top: 15px;
}

:deep(.el-form-item__label) {
  color: #fff !important;
}

:deep(.el-input__wrapper) {
  background-color: rgba(0, 0, 0, 0.3) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
}

:deep(.el-input__inner) {
  color: #fff !important;
  z-index: 1;
  position: relative;
  background: transparent !important;
}

:deep(.el-button--primary) {
  background-color: rgba(46, 139, 87, 0.8) !important;
  border-color: rgba(46, 139, 87, 0.9) !important;
}

:deep(.el-button--text) {
  color: #2E8B57 !important;
}

:deep(.el-alert) {
  margin-top: 15px;
  background-color: rgba(245, 108, 108, 0.3) !important;
}

/* 確保輸入框可以正常交互 */
:deep(.el-input) {
  z-index: 10;
}

:deep(.el-input__wrapper) {
  z-index: 10;
  pointer-events: auto !important;
}
</style> 
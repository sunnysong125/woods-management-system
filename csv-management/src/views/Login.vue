<template>
    <div class="login-container">
      <el-card class="login-card">
        <h2>登录</h2>
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="el-icon-lock"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%">登录</el-button>
          </el-form-item>
        </el-form>
        <div class="login-links">
          <router-link to="/register">没有账号？立即注册</router-link>
        </div>
      </el-card>
    </div>
  </template>
  
  <script>
  import { ref, reactive } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  
  export default {
    name: 'Login',
    setup() {
      const store = useStore()
      const router = useRouter()
      const loginFormRef = ref(null)
      const loading = ref(false)
      
      const loginForm = reactive({
        username: '',
        password: ''
      })
      
      const rules = {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
      
      const handleLogin = () => {
        loginFormRef.value.validate(async (valid) => {
          if (valid) {
            loading.value = true
            try {
              // 这里应该调用真实的登录API
              // 模拟登录成功
              const user = { 
                username: loginForm.username,
                role: 'MEMBER'
              }
              store.dispatch('login', user)
              ElMessage.success('登录成功')
              router.push('/dashboard')
            } catch (error) {
              ElMessage.error('登录失败：' + (error.message || '未知错误'))
            } finally {
              loading.value = false
            }
          }
        })
      }
      
      return {
        loginForm,
        rules,
        loginFormRef,
        loading,
        handleLogin
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
  }
  
  .login-card {
    width: 400px;
    max-width: 100%;
    padding: 20px;
  }
  
  h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #409EFF;
  }
  
  .login-links {
    margin-top: 15px;
    text-align: center;
  }
  
  a {
    color: #409EFF;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>
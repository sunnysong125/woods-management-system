<template>
    <div class="home">
      <el-row :gutter="20">
        <el-col :span="24">
          <h1>CSV数据管理系统</h1>
          <p>上传、管理和查询CSV数据的平台</p>
          
          <el-card v-if="!isLoggedIn" class="welcome-card">
            <h2>欢迎使用</h2>
            <p>请登录或注册以开始使用系统功能</p>
            <div class="action-buttons">
              <el-button type="primary" @click="$router.push('/login')">登录</el-button>
              <el-button @click="$router.push('/register')">注册</el-button>
            </div>
          </el-card>
          
          <el-card v-else class="feature-card">
            <h2>快速访问</h2>
            <el-row :gutter="20">
              <el-col :xs="24" :sm="8">
                <el-card class="box-card" shadow="hover" @click="$router.push('/upload')">
                  <h3>上传CSV文件</h3>
                  <p>上传新的CSV数据文件</p>
                </el-card>
              </el-col>
              <el-col :xs="24" :sm="8">
                <el-card class="box-card" shadow="hover" @click="$router.push('/data')">
                  <h3>数据管理</h3>
                  <p>查看和管理已上传的数据</p>
                </el-card>
              </el-col>
              <el-col :xs="24" :sm="8">
                <el-card class="box-card" shadow="hover" @click="$router.push('/dashboard')">
                  <h3>仪表板</h3>
                  <p>查看数据概览和统计</p>
                </el-card>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue'
  import { useStore } from 'vuex'
  
  export default {
    name: 'Home',
    setup() {
      const store = useStore()
      const isLoggedIn = computed(() => store.state.isAuthenticated)
      
      return {
        isLoggedIn
      }
    }
  }
  </script>
  
  <style scoped>
  .home {
    padding: 20px;
  }
  
  h1 {
    margin-bottom: 20px;
    color: #409EFF;
  }
  
  .welcome-card, .feature-card {
    margin-top: 30px;
    text-align: center;
  }
  
  .action-buttons {
    margin-top: 20px;
  }
  
  .box-card {
    cursor: pointer;
    transition: transform 0.3s;
    height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .box-card:hover {
    transform: translateY(-5px);
  }
  </style>
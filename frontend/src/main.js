import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from './utils/axios'
import './assets/css/main.css'
import ForestBackground from './components/ForestBackground.vue'

store.dispatch('checkAuth')

const app = createApp(App)

app.use(store)
app.use(router)
app.use(ElementPlus)

app.component('ForestBackground', ForestBackground)

app.config.globalProperties.$axios = axios

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

app.mount('#app') 
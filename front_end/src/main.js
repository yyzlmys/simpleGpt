import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import './assets/styles.css' 


// 创建 Vue 应用
const app = createApp(App)

// 全局注册 ElementPlus Icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用 ElementPlus 和 Vue Router
app.use(ElementPlus)
app.use(router)

// 配置 axios 为全局属性
app.config.globalProperties.$axios = axios

// 应用主题：根据 Vuex 状态动态应用主题类
store.watch(
  (state) => state.theme,
  (newTheme) => {
    if (newTheme === 'green') {
      document.body.classList.add('green-theme')
      document.body.classList.remove('light-theme')
    } else {
      document.body.classList.add('light-theme')
      document.body.classList.remove('green-theme')
    }
  },
  { immediate: true } // 立即应用当前的主题
)

// 挂载应用
app.use(store)
app.mount('#app')

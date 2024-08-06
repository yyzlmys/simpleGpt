import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import './assets/lightTheme.css' // 默认浅色主题

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

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

// 应用主题：根据 Vuex 状态动态加载主题
store.watch(
  (state) => state.theme,
  (newTheme) => {
    // 动态引入主题样式
    if (newTheme === 'dark') {
      import('./assets/darkTheme.css').then(() => {})
    } else {
      import('./assets/lightTheme.css').then(() => {})
    }
  },
  { immediate: true } // 立即应用当前的主题
)

// 挂载应用
app.use(store)
app.mount('#app')

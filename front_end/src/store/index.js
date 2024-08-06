import { createStore } from 'vuex'

export default createStore({
  state: {
    theme: 'light' // 初始主题为浅色
  },
  mutations: {
    setTheme(state, theme) {
      state.theme = theme
    }
  },
  actions: {
    toggleTheme({ commit, state }) {
      const newTheme = state.theme === 'light' ? 'dark' : 'light'
      commit('setTheme', newTheme)
    }
  }
})

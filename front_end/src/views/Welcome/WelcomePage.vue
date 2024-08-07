<template>
  <div>
    <div v-if="showAnimation" class="welcome-animation">
      <div class="animation-content">
        <h1>欢迎使用极简智能 !</h1>
        <h2>Welcome to SimpleGPT !</h2>
      </div>
    </div>
    <div v-else class="welcome-page">
      <section class="section section-blue">
        <h2>SimpleGPT 你的日常助手</h2>
        <p>既能写文档，读文档，分析视频，为您答疑解惑，快来跟我们对话吧！</p>
        <button @click="navigateToLogin">立即体验</button>
      </section>
      <section class="section section-light">
        <h2>SimpleGPT 可以为您做什么：</h2>
        <p>高效处理文档</p>
        <p>提高您的网页搜索效率</p>
        <p>帮助您编写程序</p>
        <p>总结视频内容...</p>
        <p>欢迎探索 ！</p>
      </section>
      <section class="section section-dark">
        <h2> 基于OpenAI ChatGPT-4o-mini 的大语言模型</h2>
      </section>
      <section class="section section-grey">
        <h2>期待您的宝贵意见！</h2>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showAnimation: true
    };
  },
  mounted() {
    if (localStorage.getItem('animationShown')) {
      this.showAnimation = false;
    } else {
      setTimeout(() => {
        this.showAnimation = false;
        localStorage.setItem('animationShown', 'true');
      }, 5000); // 动画持续时间
    }
  },
  methods: {
    navigateToLogin() {
      this.$emit('want-login');
    }
  }
};
</script>

<style scoped>
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeOut {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
  100% {
    opacity: 0;
    transform: scale(0.8);
  }
}

.welcome-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #45d5e2, #cac6ca); /* 渐变背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* 确保在最上层 */
  animation: fadeIn 1s ease-out, fadeOut 2s ease-out 1s; /* 动画效果 */
}

.animation-content {
  text-align: center;
  color: white;
  font-family: 'Arial', sans-serif;
}

h1 {
  font-size: 3rem;
  margin: 0;
  animation: fadeIn 1s ease-out;
}

h2 {
  font-size: 1.5rem;
  margin-top: 10px;
  animation: fadeIn 1s ease-out 0.5s; /* 延迟动画 */
}

.welcome-page {
  padding: 0;
}

.section {
  padding: 100px 20px;
  text-align: center;
}

.section-blue {
  background-color: #63abe6;
  color: white;
}

.section-light {
  background-color: #f9fafb;
  color: #000309;
}

.section-dark {
  background-color: #e5e6e8;
  color: rgb(0, 7, 13);
}

.section-grey {
  background-color: #63abe6;
  color: white;
}

h2 {
  font-size: 32px;
  margin-bottom: 20px;
}

p {
  font-size: 20px;
  margin-bottom: 20px;
}

button {
  padding: 15px 30px;
  font-size: 18px;
  background-color: #eee;
  color: #63abe6;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #c0c2c4;
}
</style>

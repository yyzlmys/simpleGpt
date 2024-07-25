<template>
    <div class="container">
      <div class="centered-icon">
        <el-icon :size="200"><Warning /></el-icon>
      </div>
      <div class="text">抱歉！您访问的页面不存在</div>
      <div class="buttons">
        <el-button type="primary" @click="redirect('/chat')">返回首页</el-button>
        <template v-if="!isLogin">
          <el-button type="primary" @click="handleLogin()">登录</el-button>
        </template>
      </div>
    </div>
  </template>
    
<script>
import { getToken } from '@/utils/auth';
export default {
  name: 'Error403',

  mounted() {
    this.init();
  },

  data() {
    return {
      isLogin: false,
    }
  },

  methods: {
    init()
    {
      if(getToken())
        this.isLogin = true;
    },

    redirect(path)
    {
        this.$router.push(path);
    },

    handleLogin() {
      this.$emit('want-login');
    }
  }
};

</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 60vh;
}

.centered-icon {
  margin-bottom: 20px;
}

.text {
  font-size: 24px;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  justify-content: center;
}

.buttons > .el-button {
  margin: 0 10px;
}
</style>

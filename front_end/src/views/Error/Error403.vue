<template>
    <div class="container">
      <div class="centered-icon">
        <el-icon :size="200"><Lock /></el-icon>
      </div>
      <div class="text">抱歉！您无权限访问该页面</div>
      <div class="buttons">
        <el-button type="primary" @click="handleLogin()">登录</el-button>
      </div>
    </div>
  </template>
    
<script>
export default {
  name: 'Error403',
    methods: {
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

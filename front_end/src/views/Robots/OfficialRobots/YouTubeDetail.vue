<template>
  <div class="container">
    <div class="box top-box">YouTube 视频助手</div>
    <div class="bottom-row">
      <div class="box bottom-box">功能1</div>
      <div class="box bottom-box">说明2</div>
      <div class="box bottom-box">。。。。。。</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ThreeBoxesLayout'
}
</script>

<style scoped>
/* 容器布局 */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh; /* 设置容器高度为视口高度 */
  padding: 20px;
  box-sizing: border-box;
}

/* 上方模块 */
.top-box {
  width: 100%;
  background-color: #84b0e9;
  color: white;
  text-align: center;
  padding: 20px;
  box-sizing: border-box;
  flex: 0 0 25%; /* 占据容器高度的1/4 */
}

/* 下方模块排列 */
.bottom-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
  flex: 0 0 60%; /* 占据容器高度的3/4 */
  margin-top: 20px;
}

/* 下方模块 */
.bottom-box {
  width: 32%;
  background-color: #ffffff;
  color: #35495e;
  text-align: center;
  padding: 20px;
  box-sizing: border-box;
  background-color: #e8f3fc; 
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1; 
}
</style>

<template>
    <div class="container">
      <div class="centered-icon">
        <img class="chat-icon" src="../../assets/ChatGPT.png"/>
      </div>
      <div class="text">你好！欢迎与我进行交流！</div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChatWelcome',
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
  
  .chat-icon {
    width: 100px; /* 调整图片的宽度 */
    height: 100px; /* 调整图片的高度 */
  }
  
  .text {
    font-size: 24px;
    margin-bottom: 20px;
  }
  </style>
  
<template>
    <div class="guide-page">
      <section class="section section-blue">
        <h2>Welcome to SimpleGPT !</h2>
        <p>SimpleGPT 是您的全能助手，帮助您更高效地处理文档、分析视频，以及提供智能问答服务。</p>
      </section>
  
      <section class="section section-light">
        <h2>SimpleGPT 可以帮您做什么 ？</h2>
        <ul>
          <li>智能文档编辑：自动撰写、修改和分析各种文档。</li>
          <li>视频分析：提取视频中的关键信息并提供有用的见解。</li>
          <li>实时问答：针对您的问题提供快速而准确的回答。</li>
        </ul>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: 'GuidePage',
  };
  </script>
  
  <style scoped>
  .guide-page {
    font-family: Arial, sans-serif;
  }
  
  .section {
    padding: 60px 20px;
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
  
  h2 {
    font-size: 32px;
    margin-bottom: 20px;
  }
  
  p {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  ul li {
    font-size: 20px;
    margin-bottom: 10px;
  }
  </style>
  
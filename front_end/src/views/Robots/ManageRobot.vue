<template>
  <el-page-header @back="goBack" content="机器人详情">
  </el-page-header>
  <div v-loading="loading" class="page-container">
    <div class="robot">
      <button v-if="robotUserId !== 1" class="delete-btn" @click="handleDeleteRobot">×</button>
      <div class="header">
        <img class="avatar" :src=getAvatarSrc alt="Avatar">
        <h2 class="name">{{ this.robotName }}</h2>
      </div>
      <p class="introduction">{{ this.robotIntro }}</p>
      <div v-if="this.robotUserId !== 1" class="prompt-section">
        <h3 class="prompt-label">System Prompt:</h3>
        <p class="prompt">"{{ this.robotPrompt }}"</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import { api_delete_robot, api_getRobot } from '@/api/robot';
import router from '@/router';

export default {
  name: 'ManageRobot',
  computed: {
    getAvatarSrc() {
      switch (this.id) {
        case 1:
          return require('@/assets/ChatGPT.png');
        case 2:
          return require('@/assets/Google.png');
        case 3:
          return require('@/assets/github.png');
        case 4:
          return require('@/assets/Bilibili.png');
        case 5:
          return require('@/assets/chrome.png');
        case 6:
          return require('@/assets/file.png');
        default:
          return require('@/assets/ChatGPT.png');
      }
    }
  },
  data() {
    return {
      id: this.$route.params.id,
      robotName: '',
      robotIntro: '',
      robotPrompt: '',
      robotUserId: null,
      loading: true,
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    async getRobotDetails(id) {
      const response = await api_getRobot(id);
      const data = response.data.data;
      this.id = data.id;
      this.robotName = data.name;
      this.robotIntro = data.intro;
      this.robotPrompt = data.prompt;
      this.robotUserId = data.userId;
    },
    async init() {
      this.loading = true;
      await this.getRobotDetails(this.id);
      this.loading = false;
    },
    handleDeleteRobot() {
      ElMessageBox.confirm(
        '该操作将删除此机器人，是否确认?',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'error',
        }
      )
        .then(async () => {
          const response = await api_delete_robot(this.id);
          if (response.data.code === 200) {
            ElMessage({
              message: '删除成功!',
              type: 'success',
            });
            router.push('/robot'); // 确保此处路由路径正确
          } else {
            ElMessage({
              message: '删除失败!',
              type: 'danger',
            });
          }
        })
        .catch(() => {
          ElMessage({
            message: '取消删除',
            type: 'info',
          });
        });
    },
    goBack() {
      router.push('/robot'); // 确保此处路由路径正确
    },
  },
};
</script>

<style scoped>
 .page-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    box-sizing: border-box;
  }

  .robot {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 550px;
    width: 100%;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
  }



  .delete-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 24px;
    color: #999;
    cursor: pointer;
    transition: color 0.3s;
  }

  .delete-btn:hover {
    color: #ff4444;
  }

  .header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    width: 100%;
    background-color: #ffffff;
  }

  .avatar {
    width: 80px;
    height: 80px;
    /* border-radius: 50%; */
    object-fit: cover;
    margin-right: 20px;
  }

  .name {
    font-size: 28px;
    font-weight: bold;
    margin: 0;
    color: #333;
  }

  .introduction {
    font-size: 16px;
    line-height: 1.5;
    text-align: center;
    margin: 0 0 25px 0;
    color: #666;
    font-style: italic;
  }

  .prompt-section {
    width: 100%;
    background-color: #f8f8f8;
    border-radius: 8px;
    padding: 15px;
    margin-top: 10px;
  }

  .prompt-label {
    font-size: 14px;
    font-weight: 600;
    color: #555;
    margin: 0 0 10px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .prompt {
    font-size: 16px;
    line-height: 1.5;
    color: #444;
    margin: 0;
    font-weight: 500;
  }
</style>

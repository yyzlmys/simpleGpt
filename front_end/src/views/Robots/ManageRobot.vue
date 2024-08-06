<template>
    <el-page-header @back="goBack" :content="robotName">
    </el-page-header>
    <div v-loading="loading">
      <div class="head">
        <div class="robot-info">
          <h1>{{ robotName }}</h1>
          <p>{{ robotIntro }}</p>
          <p>{{ robotPrompt }}</p>
        </div>
        <el-button class="total-delete" type="danger" circle @click="handleDeleteRobot()">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
      <el-form>
        <el-form-item label="名称">
          <el-input v-model="robotName" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="robotIntro" />
        </el-form-item>
        <el-form-item label="提示">
          <el-input v-model="robotPrompt" />
        </el-form-item>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </el-form>
    </div>
  </template>
  
  <script>
  import { ElMessage, ElMessageBox } from 'element-plus';
  import { api_delete_robot, api_getRobot, api_updateRobot } from '@/api/robot';
  export default {
    name: 'ManageRobot',
    data() {
      return {
        id: this.$route.params.id,
        robotName: '',
        robotIntro: '',
        robotPrompt: '',
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
        this.robotName = data.name;
        this.robotIntro = data.intro;
        this.robotPrompt = data.prompt;
      },
      async init() {
        this.loading = true;
        await this.getRobotDetails(this.id);
        this.loading = false;
      },
      async handleSave() {
        const updatedRobot = {
          name: this.robotName,
          intro: this.robotIntro,
          prompt: this.robotPrompt,
        };
        const response = await api_updateRobot(this.id, updatedRobot);
        if (response.data.code === 200) {
          ElMessage({
            message: '保存成功！',
            type: 'success',
          });
        } else {
          ElMessage({
            message: '保存失败！',
            type: 'danger',
          });
        }
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
              this.$router.push('/robots');
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
        this.$router.push('/robots');
      },
    },
  };
  </script>
  
  <style scoped>
  .head {
    display: flex;
    align-items: center;
    margin-top: 10px;
  }
  .head .robot-info {
    flex: 1;
  }
  .head .total-delete {
    flex-shrink: 0;
  }
  </style>
  
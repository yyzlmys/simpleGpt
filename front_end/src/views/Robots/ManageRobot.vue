<template>
  <el-page-header @back="goBack" content="机器人详情">
  </el-page-header>
  <div v-loading="loading" class="robot-details">
    <el-form label-width="120px" class="robot-form">
      <el-form-item label="名称">
        <el-input v-model="robotName" disabled />
      </el-form-item>
      <el-form-item label="简介">
        <el-input v-model="robotIntro" disabled />
      </el-form-item>
      <el-form-item label="提示">
        <el-input v-model="robotPrompt" disabled />
      </el-form-item>
    </el-form>
    <el-button 
      v-if="robotUserId !== 1"
      class="total-delete" 
      type="danger" 
      @click="handleDeleteRobot"
    >
      <el-icon><Delete /></el-icon> 删除
    </el-button>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import { api_delete_robot, api_getRobot } from '@/api/robot';
import router from '@/router';

export default {
  name: 'ManageRobot',
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
.robot-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
}
.robot-form {
  width: 100%;
  max-width: 600px;
}
.el-form-item {
  font-size: 18px;
}
.el-input {
  font-size: 18px;
}
.total-delete {
  margin-top: 20px;
  font-size: 18px;
}
</style>

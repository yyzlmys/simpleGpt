<template>
  <div v-loading="loading">

    <div v-loading="loading" class="robot-list">
      <h2>官方机器人</h2>
      <div class="robot-grid">
        <div v-for="robot in officialRobots" :key="robot.id" class="robot-card" @click="handleItemClick(robot.id)" tabindex="0">
          <img :src="getAvatarSrc(robot.id)" :alt="robot.name" class="robot-icon">
          <div class="robot-info">
            <h3>{{ robot.name }}</h3>
            <p>{{ robot.intro }}</p>
          </div>
        </div>
      </div>

      <h2>您专属的机器人</h2>
      <div class="robot-grid">
        <div v-for="robot in personalRobots" :key="robot.id" class="robot-card" @click="handleItemClick(robot.id)" tabindex="0">
          <img :src="getAvatarSrc(robot.id)" :alt="robot.name" class="robot-icon">
          <div class="robot-info">
            <h3>{{ robot.name }}</h3>
            <p>{{ robot.intro }}</p>
          </div>
        </div>
        <div class="add-robot-card" @click="dialogFormVisible = true" tabindex="0">
          <span class="add-icon">+</span>
          <span>添加新机器人</span>
        </div>
      </div>
    </div>

    <el-dialog v-model="dialogFormVisible" title="创建机器人" width="800">
      <el-form :model="form">
        <el-form-item label="名称" :label-width="formLabelWidth" label-position="top">
          <el-input
              v-model="form.name"
              placeholder="填写机器人名称..."
              clearable
            ></el-input>
        </el-form-item>
        <el-form-item label="简介" :label-width="formLabelWidth" label-position="top">
          <el-input
              v-model="form.intro"
              placeholder="这是一个苏格拉底式的机器人，用于让我在对话的过程中学会思考..."
              clearable
              type="textarea"
              :autosize="{ minRows: 2 }"
            ></el-input>
        </el-form-item>
        <el-form-item label="system prompt" :label-width="formLabelWidth" label-position="top">
          <el-input
              v-model="form.prompt"
              placeholder="你是一个苏格拉底式的导师，回答问题总是采用引导的方式，以此来让用户通过逐步思考来解决问题..."
              clearable
              type="textarea"
              :autosize="{ minRows: 2 }"
            ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateRobot">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { api_listRobots, api_create_robot } from '@/api/robot';
import { ElMessage } from 'element-plus';
import router from '@/router';

export default {
  name: 'ListRobots',
  components: {
  },
  setup() {
    const robots = ref([]);
    const officialRobots = ref([]);
    const personalRobots = ref([]);
    const dialogFormVisible = ref(false);
    const formLabelWidth = '200px';
    const form = ref({
      name: '',
      intro: '',
      prompt: ''
    });
    const loading = ref(true);

    const getAvatarSrc = (robotId) => {
      switch (robotId) {
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
    };

    const fetchRobots = async () => {
      loading.value = true;
      const response = await api_listRobots();
      robots.value = response.data.data;

      // 分类机器人
      officialRobots.value = robots.value.filter(robot => robot.userId === 1);
      personalRobots.value = robots.value.filter(robot => robot.userId !== 1);
      
      loading.value = false;
    };

    const handleItemClick = (id) => {
      router.push({ name: 'ManageRobot', params: { id } });
    };

    const handleCreateRobot = async () => {
      const newRobot = {
        name: form.value.name,
        intro: form.value.intro,
        prompt: form.value.prompt
      };
      const response = await api_create_robot(newRobot);
      if (response.data.code == 200) {
        ElMessage({
          message: '创建成功！',
          type: 'success',
        });
        fetchRobots();
      } else {
        ElMessage({
          message: '创建失败！',
          type: 'danger',
        });
      }
      form.value = { name: '', intro: '', prompt: '' };
      dialogFormVisible.value = false;
    };

    onMounted(fetchRobots);

    return {
      officialRobots,
      personalRobots,
      form,
      loading,
      dialogFormVisible,
      formLabelWidth,
      handleItemClick,
      handleCreateRobot,
      getAvatarSrc,
    };
  },
};
</script>

<style scoped>
.robot-list {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h2 {
  margin-bottom: 15px;
}

.robot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.robot-card, .add-robot-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 10px;
  background-color: #f5f5f5;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.robot-card:hover, .add-robot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.robot-card:focus, .add-robot-card:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
}

.robot-icon {
  width: 50px;
  height: 50px;
  margin-right: 15px;
  border-radius: 10px;
}

.robot-info {
  flex: 1;
}

.robot-info h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.robot-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.user-count {
  font-size: 12px;
  color: #888;
}

.add-robot-card {
  justify-content: center;
  flex-direction: column;
  text-align: center;
  color: #666;
}

.add-icon {
  font-size: 24px;
  margin-bottom: 5px;
}

.dialog-footer {
  text-align: right;
  margin-top: 20px;
}
</style>

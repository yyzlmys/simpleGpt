<template>
  <div class="robot-list" v-loading="loading">
    <!-- 官方机器人 -->
    <h2 class="section-title">官方机器人</h2>
    <RobotItem 
      v-for="robot in officialRobots" 
      :key="robot.id" 
      :name="robot.name"
      @click="handleItemClick(robot.id)" 
    />

    <!-- 自定义机器人 -->
    <h2 class="section-title">自定义机器人</h2>
    <RobotItem 
      v-for="robot in customRobots" 
      :key="robot.id" 
      :name="robot.name"
      @click="handleItemClick(robot.id)" 
    />
    <RobotItem 
      name="+" 
      isAddButton 
      @click="dialogFormVisible = true" 
    />

    <el-dialog v-model="dialogFormVisible" title="创建机器人" width="500">
      <el-form :model="form">
        <el-form-item label="名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="简介" :label-width="formLabelWidth">
          <el-input v-model="form.intro" autocomplete="off" />
        </el-form-item>
        <el-form-item label="提示" :label-width="formLabelWidth">
          <el-input v-model="form.prompt" autocomplete="off" />
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
import RobotItem from './RobotItem.vue';
import { api_listRobots, api_create_robot } from '@/api/robot';
import { ElMessage } from 'element-plus';
import router from '@/router';

export default {
  name: 'ListRobots',
  components: {
    RobotItem,
  },
  setup() {
    const robots = ref([]);
    const officialRobots = ref([]);
    const customRobots = ref([]);
    const dialogFormVisible = ref(false);
    const formLabelWidth = '80px';
    const form = ref({
      name: '',
      intro: '',
      prompt: ''
    });
    const loading = ref(true);

    const fetchRobots = async () => {
      loading.value = true;
      const response = await api_listRobots();
      robots.value = response.data.data;

      // 分类机器人
      officialRobots.value = robots.value.filter(robot => robot.userId === 1);
      customRobots.value = robots.value.filter(robot => robot.userId !== 1);
      
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
      customRobots,
      form,
      loading,
      dialogFormVisible,
      formLabelWidth,
      handleItemClick,
      handleCreateRobot,
    };
  },
};
</script>

<style scoped>
.robot-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  padding: 20px;
}
.section-title {
  width: 100%;
  text-align: left;
  margin: 20px 0 10px;
}
.dialog-footer {
  text-align: right;
}
</style>

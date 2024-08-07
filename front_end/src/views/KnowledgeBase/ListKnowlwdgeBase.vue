<template>
    <div v-loading="loading" class="knowledge-base-list">
      <h1>知识库列表</h1>
      <div class="add-card">
        <button class="add-button" @click="dialogFormVisible = true">添加新知识库</button>
      </div>
      <div class="card-container">
        <div 
          v-for="(kb, index) in knowledgeBases" 
          :key="index" 
          class="card"
          @click="handleItemClick(kb.id)"
        >
          <h2>{{ kb.name }}</h2>
          <p>大小: {{ kb.size }} MB</p>
        </div>
      </div>
    </div>
    <el-dialog v-model="dialogFormVisible" title="创建知识库" width="500">
        <el-form :model="form">
          <el-form-item label="名称" :label-width="formLabelWidth">
            <el-input v-model="form.name" autocomplete="off" />
          </el-form-item>
          <el-form-item label="描述" :label-width="formLabelWidth">
            <el-input v-model="form.description" autocomplete="off" />
          </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取消</el-button>
            <el-button type="primary" @click="handleCreateKnowledgeBase()">
              确定
            </el-button>
          </div>
        </template>
      </el-dialog>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { api_listKnowledgeBases, api_createKnowledgeBase, api_deleteKnowledgeBase} from '@/api/knowledgeBase'
  import { ElMessage } from 'element-plus';
  import router from '@/router'
  export default {
    name: 'ListKnowledgeBase',
    components: {
    },
    setup() {
      const knowledgeBases = ref([]);
  
      const dialogFormVisible = ref(false)
      const formLabelWidth = '80px'
      const form = ref({
        name: '',
        description: ''
      });

      const loading = ref(true);
  
      const fetchKnowledgeBases = async () => {
        loading.value = true;
        await api_listKnowledgeBases()
        .then((response)=>{
          knowledgeBases.value = response.data.data;
        })
        loading.value = false;
      };
  
      const handleItemClick = (id) => {
        router.push({ name: 'ManageKnowlwdgeBase', params: { id } });
      };

      const handleCreateKnowledgeBase = () => {
        const newKnowledgeBase = {
          name: form.value.name,
          description: form.value.description
        }
        api_createKnowledgeBase(newKnowledgeBase)
        .then((response)=>{
          if(response.data.code == 200)
          {
            ElMessage({
              message: '创建成功！',
              type: 'success',
            });
            fetchKnowledgeBases();
          }
          else
          {
            ElMessage({
              message: '创建失败！',
              type: 'danger',
            });
          }
        })
        form.value = {name: ''};
        dialogFormVisible.value = false;
      };

      onMounted(fetchKnowledgeBases);
  
      return {
        knowledgeBases,
        form,
        loading,
        dialogFormVisible,
        formLabelWidth,
        handleItemClick,
        handleCreateKnowledgeBase,
      };
    },
  };
  </script>
  
  <style scoped>
.knowledge-base-list {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.add-card {
  margin-bottom: 20px;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  background-color: #f0f0f0;
}

.card:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h1 {
  text-align: center;
}

h2 {
  margin-top: 0;
}

.add-button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-button:hover {
  background-color: #45a049;
}

.add-button:active {
  background-color: #3d8b40;
}
  </style>
  
<template>
    <div class="knowledge-base-list" v-loading="loading">
      <KnowledgeBaseItem 
        v-for="(item, index) in knowledgeBases" 
        :key="index" 
        :name="item.name"
        :totalCapacity=100
        :usedCapacity="item.size"
        @click="handleItemClick(item.id)" 
      />
      <KnowledgeBaseItem 
        name="+" 
        isAddButton 
        @click="dialogFormVisible = true" 
      />
  
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
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import KnowledgeBaseItem from './KnowledgeBaseItem.vue';
  import { api_listKnowledgeBases, api_createKnowledgeBase, api_deleteKnowledgeBase} from '@/api/knowledgeBase'
  import { ElMessage } from 'element-plus';
  import router from '@/router'
  export default {
    name: 'ListKnowledgeBase',
    components: {
      KnowledgeBaseItem,
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
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    padding: 20px;
  }
  .dialog-footer {
    text-align: right;
  }
  </style>
  
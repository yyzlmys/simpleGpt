<template>
  <el-page-header @back="goBack" :content=knowledgeBaseName>
  </el-page-header>
  <div v-loading="loading">
    <div class="head">
      <div class="base-name">
        <h1>{{ knowledgeBaseName }}</h1>
      </div>
      <el-button class="total-delete" type="danger" circle @click="handleDeleteKnowledgeBase()">
        <el-icon><Delete /></el-icon>
      </el-button>
    </div>
    <div class="progress-bar">
      <el-progress :text-inside="true" :stroke-width="26" :percentage=knowledgeBaseUsedcapacity />
    </div>
    <div class="files-table">
      <el-table :data="files" style="width: 100%">
        <el-table-column label="文件名" width="300">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span style="margin-left: 10px">{{ scope.row.fileName }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="类型" width="100">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span style="margin-left: 10px">{{ scope.row.type }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="大小" width="100">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span style="margin-left: 10px">{{ scope.row.size }}MB</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="日期" width="200">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span style="margin-left: 10px">{{ scope.row.date }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="success" circle @click="handleDownload(scope.row)">
              <el-icon><Download /></el-icon>
            </el-button>
            <el-button type="danger" circle @click="handleDelete(scope.row)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="file-upload">
      <label for="file-upload" class="custom-file-upload">
        选择文件
      </label>
      <input type="file" id="file-upload" @change="handleFileChange" />
      <span class="file-name" v-if="selectedFile">{{ selectedFile.name }}</span>
      <button class="upload-button" @click="uploadFile">上传文件</button>
    </div>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import { api_deleteKnowledgeBase, api_listFiles, api_getKnowledgeBase, api_downloadFile, api_uploadFile, api_deleteFile,   } from '@/api/knowledgeBase'
export default {
    name: 'ManageKnowledgeBase',
    mounted() {
      this.init();
    },
    data() {
      return {
        id: this.$route.params.id,
        knowledgeBaseName: '',
        knowledgeBaseUsedcapacity: 0,
        files:[],
        loading: true,
        selectedFile: null,
      };
    },
    methods:{
      async getDetails(id)
      {
        await api_getKnowledgeBase(id)
        .then((response)=>{
          this.knowledgeBaseName = response.data.data.name;
          this.knowledgeBaseUsedcapacity = response.data.data.size;
        })
      },

      async getFiles(id)
      {
        await api_listFiles(id)
        .then((response)=>{
          this.files = response.data.data;
        })
      },

      async init()
      {
        this.loading = true;
        await this.getDetails(this.id);
        await this.getFiles(this.id);
        this.loading = false;
      },

      handleDownload(row)
      {
        const fileId = row.id;
        api_downloadFile(fileId)
        .then((response)=>{
          if(response.data.code == 201)
          {
            ElMessage({
              message: '下载失败，请重试！',
              type: 'danger',
            });
          }
          else
          {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', row.fileName);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
          }
        })
      },

      handleDelete(row)
      {
        const fileId = row.id;
        api_deleteFile(fileId)
        .then((response)=>{
          if(response.data.code == 200)
          {
            ElMessage({
              message: '删除成功!',
              type: 'success',
            });  
            this.init();
          }
          else
          {
            ElMessage({
              message: '删除失败!',
              type: 'danger',
            }); 
          }
        })
      },

      handleFileChange(event) {
        this.selectedFile = event.target.files[0];
      },

      async uploadFile() {
        if (!this.selectedFile) {
          ElMessage({
            message: '请先选择文件!',
            type: 'error',
          });  
          return;
        }

        await api_uploadFile(this.id, this.selectedFile)
        .then((response)=>{
          if(response.data.code == 200) {
            ElMessage({
              message: '上传成功!',
              type: 'success',
            });  
            this.init();
          }
          else {
            ElMessage({
              message: '上传失败!',
              type: 'danger',
            }); 
          }
        })
        .catch(()=>{
          ElMessage({
              message: '上传失败!',
              type: 'danger',
          }); 
        })
      },

      handleDeleteKnowledgeBase()
      {
        ElMessageBox.confirm(
        '该操作将删除整个知识库，包括其中的信息，是否确认?',
          {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'error',
          }
        )
        .then(()=>{
          api_deleteKnowledgeBase(this.id)
          .then((response)=>{
            if(response.data.code == 200)
            {
              ElMessage({
                message: '删除成功!',
                type: 'success',
              }); 
              this.$router.push('/knowledgebase');
            }
            else
            {
              ElMessage({
                message: '删除失败!',
                type: 'danger',
              }); 
            }
          })
        })
        .catch(()=>{
          ElMessage({
            message: '取消删除',
            type: 'info',
          })
        })
        
      },
    
      goBack()
      {
        this.$router.push('/knowledgebase')
      }
    }
}
</script>


<style scoped>
.head {
  display: flex;
  align-items: center;
  margin-top: 10px;
  width: 800px;
}

.head .base-name {
  flex: 1;
  margin-right: 300px;
}

.head .total-delete {
  flex-shrink: 0;
}


.progress-bar .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}

.file-upload {
  display: flex;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.custom-file-upload {
  display: inline-block;
  padding: 6px 12px;
  cursor: pointer;
  background-color: #409EFF;
  color: white;
  border-radius: 4px;
  font-weight: bold;
}

.custom-file-upload:hover {
  background-color: #66b1ff;
}

input[type="file"] {
  display: none;
}

.file-name {
  margin-left: 10px;
  font-size: 14px;
  color: #333;
}

.upload-button {
  padding: 6px 12px;
  background-color: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.upload-button:hover {
  background-color: #85ce61;
}
</style>

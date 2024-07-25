<template>
  <el-page-header @back="goBack" :content=knowledgeBaseName>
  </el-page-header>
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
    <!-- <el-button type="primary">
      上传<el-icon class="el-icon--right" @click="handleUpload()"><Upload /></el-icon>
    </el-button> -->
    <input type="file" @change="handleFileChange" />
    <button @click="uploadFile">Upload File</button>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus';
import { api_deleteKnowledgeBase, api_listFiles, api_getKnowledgeBase, api_downloadFile, api_uploadFile, api_deleteFile,   } from '@/api/knowledgeBase'
export default {
    name: 'ManageKnowledgeBase',
    components:{
      //MarkdownContainer
    },
    mounted() {
      this.getInfo();
    },
    data() {
      return {
        id: this.$route.params.id,
        knowledgeBaseName: '',
        knowledgeBaseUsedcapacity: 0,
        files:[],
        //uploadDialogVisable: false,
        selectedFile: null,
      };
    },
    methods:{
      getDetails(id)
      {
        api_getKnowledgeBase(id)
        .then((response)=>{
          this.knowledgeBaseName = response.data.data.name;
          this.knowledgeBaseUsedcapacity = response.data.data.size;
        })
      },

      getFiles(id)
      {
        api_listFiles(id)
        .then((response)=>{
          this.files = response.data.data;
        })
      },

      getInfo()
      {
        this.getDetails(this.id);
        this.getFiles(this.id);
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
            this.getFiles(this.id);
            this.getDetails(this.id);
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
          console.error('No file selected');
          return;
        }

        try {
          const response = await api_uploadFile(this.id, this.selectedFile);
          console.log('File uploaded successfully', response);
          alert('File uploaded successfully');
          this.getInfo();
        } catch (error) {
          console.error('Error uploading file', error);
          alert('Error uploading file');
        }
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
            if(response == 200)
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

</style>

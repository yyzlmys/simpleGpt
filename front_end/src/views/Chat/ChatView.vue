<template>
  <div class="chat-layout">
    <el-container class="chat-container">
      <el-aside width="15%">
        <el-row class="tac">
            <el-col>
              <ChatConversation v-loading="conversationLoading" :conversations="conversations" :curConversation="curConversationId" @selected="handleSelect" />
            </el-col>
        </el-row>
      </el-aside>
      <el-main>
        <div class="head-tool">
          <div class="choose-knowledgeBase">
            <el-select v-model="curKnowledgeBase" :disabled="isSelectDisabled" placeholder="Select" size="large" style="width: 200px">
              <el-option v-loading="knowledgeBasesLoading"
                v-for="item in knowledgeBases"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
              <el-option 
                key="no"
                label="不使用知识库"
                value="no"
              />
            </el-select>
          </div>
          <div v-if="this.curConversationId!='new'" class="delete-conversation">
            <el-button type="danger" circle @click="handleDeleteConversion()">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
        <div class="chat-content">
          <div class="chat-history">
            <div v-if="this.curConversationId!='new'">
              <ChatHistory v-loading="historyLoading" :chatHistory="chatHistory" />
            </div>
            <div v-else>
              <ChatWelcome />
            </div>
          </div>
          <div class="chat-input">
            <el-input
              v-model="inputString"
              placeholder="给`GPT`发送消息..."
              clearable
              type="textarea"
              :autosize="{ minRows: 2 }"
            ></el-input>
            <el-button type="primary" round :disabled="sendDisabled" @click="getResponse()">发送</el-button>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>
  
<script>
import ChatHistory from './ChatHistory.vue';
import ChatConversation from './ChatConversation.vue';
import ChatWelcome from './ChatWelcome.vue';
import { api_listChatHistory, api_createConversation, api_deleteConversation, 
  api_listConversations, api_getResponse } from '@/api/chat'
import { api_listKnowledgeBases } from '@/api/knowledgeBase';

import { ElMessage, ElMessageBox } from 'element-plus';
export default {
  mounted() {
    this.init();
  },
  components: {
    ChatHistory,
    ChatConversation,
    ChatWelcome
  },
  computed: {
    isSelectDisabled() {
      return this.curConversationId !== 'new';
    }
  },
  data() {
    return {
      chatHistory: [],
      inputString: '',
      curConversationId: 'new',
      conversations:[],
      knowledgeBases: [],
      curKnowledgeBase: 'no',
      ws: null,
      receivedStr: '',
      sendDisabled: false,
      conversationLoading: true,
      historyLoading: true,
      knowledgeBasesLoading: true,
      isGPTthinking: false,
    };
  },
  beforeDestroy() {
    if (this.ws) {
      this.ws.close();
    }
  },
  methods: {
    init() {
      this.listKnowlwdgeBase();
      this.listConversions();
    },

    async listChatHistory(id) {
      this.historyLoading = true;
      await api_listChatHistory(id)
      .then((response)=>{
        if(response.data.code == 200)
        {
          this.chatHistory = response.data.data;
        }
        else if(response.data.code == 201)
        {
          ElMessage({
            message: '网络异常，请刷新！',
            type: 'error',
          })
        }
      })
      this.historyLoading = false;
    },

    async listKnowlwdgeBase() {
      this.knowledgeBasesLoading = true;
      await api_listKnowledgeBases()
      .then((response)=>{
        if(response.data.code == 200)
        {
          this.knowledgeBases = response.data.data;
        }
        else if(response.data.code == 201)
        {
          ElMessage({
            message: '网络异常，请刷新!',
            type: 'error',
          });
        }
      })
      this.knowledgeBasesLoading = false;
    },

    async listConversions() {
      this.conversationLoading = true;
      await api_listConversations()
      .then((response)=>{
        if(response.data.code == 200)
        {
          this.conversations = response.data.data
        }
        else if(response.data.code == 201)
        {
          ElMessage({
            message: '网络异常，请刷新!',
            type: 'error',
          });
        }
      })
      this.conversationLoading = false;
    },

    async getResponse() {
      if(this.inputString == '')
      {
        ElMessage({
            message: '不能发送空消息!',
            type: 'error',
          });
      }
      else
      {
        // 首先，若是新聊天，创建对话
        if(this.curConversationId == 'new')
        {
          this.chatHistory = [];
          await this.handleCreateConversion();
        }
        // 建立 websocket 
        this.initWebsocket('ws://firstdraft.cn:8080/get');
        const curForm = {
          "conversationId": this.curConversationId,
          "content": this.inputString
        }
        api_getResponse(curForm)
        .then((response)=>{
          if(response.data.code == 200) {
            this.isGPTthinking = true;
          }
          else {
            ElMessage({
              message: '网络异常，请重试！',
              type: 'error',
            }) 
          }
        });
        const curHumanMessage = {
          isPerson: true,
          content: this.inputString,
          };
        this.inputString = '';
        this.chatHistory.push(curHumanMessage);
        const curAIMessage = {
          isPerson: false,
          content: 'GPT正在思考您的问题，请稍等...'
        };
        this.chatHistory.push(curAIMessage);
      }
      
    },

    initWebsocket(url) {
      if (this.ws) {
        this.ws.close();
      }
      this.ws = new WebSocket(url);

      this.ws.onopen = () => {
        console.log('WebSocket connection opened');
        this.sendWebsocket(this.curConversationId);
        this.sendDisabled = true;

      };

      this.ws.onmessage = (event) => {
        if(this.isGPTthinking)
        {
          this.isGPTthinking = false;
          this.chatHistory[this.chatHistory.length - 1].content = '';
        }
        this.receivedStr += event.data; // 追加收到的字符
        this.chatHistory[this.chatHistory.length - 1].content = this.receivedStr;
      };

      this.ws.onclose = () => {
        console.log('WebSocket connection closed');
        this.receivedStr = '';
        this.sendDisabled = false;
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

    },

    sendWebsocket(data) {
      if(this.ws)
      {
        this.ws.send(data);
      }
      else
      {
        console.log('websocket不存在，您却试图发送');
      }
    },

    async handleCreateConversion() {
      let selectedKnowledgeBase = null;
      if(this.curKnowledgeBase == 'no')
      {
        selectedKnowledgeBase = {
          "ifUseLib": 0,
          "libId": null
        }
      }
      else
      {
        selectedKnowledgeBase = {
          "ifUseLib": 1,
          "libId": this.curKnowledgeBase
        }
      }
      await api_createConversation(selectedKnowledgeBase)
      .then((response)=>{
        if(response.data.code != 200)
        {
          ElMessage({
            message: '网络异常，请刷新！',
            type: 'error',
          });
        }
        else
        {
          this.curConversationId = response.data.data;
          this.listConversions();
        }
      });
    },

    handleSelect(id) {
      if(id != 'new' && id != this.curConversationId)
      {
        this.listChatHistory(id);
      }
      this.curConversationId = id;
      this.curKnowledgeBase = this.conversations.find(item => item.id === this.curConversationId).libId;
    },

    handleDeleteConversion() {
      ElMessageBox.confirm(
        '这个操作将删除该会话的所有信息，是否继续?',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'error',
        }
      )
        .then(() => {
        api_deleteConversation(this.curConversationId)
          .then((response)=>{
            if(response.data.code == 200)
            {
              ElMessage({
                message: '删除成功！',
                type: 'success',
              });
              this.curConversationId = 'new';
              this.listConversions();
            }
            else
            {
              ElMessage({
                message: '删除失败！',
                type: 'error',
              });
            }
          })
        })
        .catch(() => {
          ElMessage({
            type: 'info',
            message: '取消删除',
          })
        })
    }

  }
}
  </script>

  <style scoped>
  html, body {
    height: 100%;
    margin: 0;
  }
  
  #app {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .chat-layout {
    flex: 1;
    display: flex;
    flex-direction: row;
    height: 100%;
  }
  
  .chat-container {
    height: 100%;
  }
  
  .el-container {
    display: flex;
    flex-direction: row;
    height: 100%;
  }
  
  .el-aside {
    /* background: gray; */
  }
  
  .el-main {
    flex: 1;
  }
  
  .chat-content {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    height: 94%;
  }
  
  .chat-history {
    flex: 1;
    overflow-y: auto;
  }
  
  .chat-input {
    display: flex;
    align-items: center;
    margin-top: 10px;
  }
  
  .chat-input .el-input {
    flex: 1;
    margin-right: 10px;
  }
  
  .chat-input .el-button {
    margin-left: 10px;
    flex-shrink: 0;
  }

  .head-tool {
    display: flex;
    align-items: center;
  }
  
  .head-tool .choose-knowledgeBase {
    flex: 1;
    margin-right: 10px;
  }
  
  .head-tool .delete-conversation {
    margin-left: 10px;
    flex-shrink: 0;
  }
  </style>
  
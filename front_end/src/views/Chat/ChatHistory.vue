<template>
    <div class="chat-container" ref="chatHistoryContainer">
      <div
        v-for="(chat, index) in chatHistory"
        :key="index"
        :class="['chat-item', { 'chat-person': chat.isPerson, 'chat-bot': !chat.isPerson }]"
      >
        <div class="chat-content-wrapper">
            <img v-if="!chat.isPerson" class="chat-icon" src="../../assets/ChatGPT.png" alt="bot-icon" />
            <div class="chat-content">
                <MarkdownContainer :markdownContent="chat.content" />
            </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import MarkdownContainer from '@/components/MarkdownContainer.vue';
  
  export default {
    mounted() {
      //this.getInfo();
      this.scrollToBottom();
    },
    props: {
      chatHistory: {
        type: Array,
        required: true,
      },
    },
    components: {
      MarkdownContainer,
    },
    watch: {
      chatHistory() {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
    },

    methods: {
      scrollToBottom() {
      // console.log('滚动了');
      // const container = this.$refs.chatHistoryContainer;
      // console.log(container)
      // container.scrollTop = container.scrollHeight;
      },
    }
    
  };
  </script>
  
<style scoped>

.chat-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  height: 100%;
  overflow-y: auto;
}

.chat-item {
  display: flex;
}

.chat-content-wrapper {
  display: flex;
  align-items: flex-start;
  
}

.chat-person {
  display: flex;
  justify-content: flex-end;
  
}

.chat-person .chat-content-wrapper {
  margin-left: auto;
  max-width: 80%;
  display: flex;
  justify-content: flex-end;
}

.chat-bot {
  justify-content: flex-start;
  width: 100%;
}

.chat-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

.chat-content {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 10px;
  box-sizing: border-box;
  width: 100%;
}

</style>

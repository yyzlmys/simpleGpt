<template>
    <el-menu
      :default-active="curConversation"
      @select="handleSelect">

        <el-menu-item index="new" key="new">
            <span>New Chat</span>
        </el-menu-item>

        <template v-for="conversation in conversations" :key="conversation.id">

            <el-menu-item :index="conversation.id" >
                <span>{{ conversation.name }}</span>
            </el-menu-item>

        </template>
    </el-menu>
</template>
  
  <script>
  export default {
    props: {
      conversations: {
        type: Array,
        required: true
      },
      curConversation: {
        required: true
      }
    },
    methods: {
      handleSelect(index)
      {
        this.$emit('selected', index);
      },
    }
  };
  </script>
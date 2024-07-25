<template>
    <div 
      class="knowledge-base-item" 
      :class="{ 'add-button': isAddButton }" 
      @click="handleClick"
    >
      <span v-if="isAddButton" class="plus-icon">+</span>
      <div v-else>
        <div class="name">{{ name }}</div>
        <div class="capacity-bar">
          <div 
            class="used-capacity" 
            :style="{ width: usedCapacityPercentage + '%' }"
          ></div>
        </div>
        <div class="capacity-info">{{ usedCapacity }} / {{ totalCapacity }}</div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'KnowledgeBaseItem',
    props: {
      name: {
        type: String,
        required: true,
      },
      totalCapacity: {
        type: Number,
        default: 100,
      },
      usedCapacity: {
        type: Number,
        default: 0,
      },
      isAddButton: {
        type: Boolean,
        default: false,
      },
    },
    emits: ['click'],
    computed: {
      usedCapacityPercentage() {
        return (this.usedCapacity / this.totalCapacity) * 100;
      },
    },
    setup(props, { emit }) {
      const handleClick = () => {
        emit('click');
      };
  
      return {
        handleClick,
      };
    },
  };
  </script>
  
  <style scoped>
  .knowledge-base-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 150px;
    height: 150px;
    background: linear-gradient(135deg, #6e8efb, #a777e3);
    border-radius: 10px;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    color: #fff;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  .knowledge-base-item:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 25px rgba(0, 0, 0, 0.2);
  }
  .plus-icon {
    font-size: 50px;
    font-weight: bold;
  }
  .name {
    margin-bottom: 10px;
  }
  .capacity-bar {
    width: 100%;
    height: 10px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 5px;
    overflow: hidden;
  }
  .used-capacity {
    height: 100%;
    background: #ffcc00;
  }
  .capacity-info {
    margin-top: 5px;
    font-size: 14px;
  }
  </style>
  
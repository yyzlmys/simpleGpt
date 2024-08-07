<template>
  <div 
    class="robot-item" 
    :class="{ 'add-button': isAddButton }" 
    @click="handleClick"
  >
    <div v-if="!isAddButton" class="name">{{ name }}</div>
    <span v-if="isAddButton" class="plus-icon">+</span>
  </div>
</template>

<script>
export default {
  name: 'RobotItem',
  props: {
    name: {
      type: String,
      required: true,
    },
    isAddButton: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['click'],
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
.robot-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  border-radius: 10px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  color: #fff;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.robot-item:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.2);
}
.plus-icon {
  font-size: 50px;
  font-weight: bold;
}
.name {
  text-align: center;
  font-size: 24px;
}
.add-button {
  background: linear-gradient(135deg, #ff4081, #ff8e53);
}
</style>

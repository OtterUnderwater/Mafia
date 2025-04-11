<template>
  <div class="function-buttons">
    <button @click="togglePause">{{ isPaused ? 'Resume' : 'Pause' }}</button>
    <button @click="addTime">Add Time</button>
  </div>
</template>

<script>
export default {
  props: {
    isPaused: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    togglePause() {
      this.$emit('toggle-pause');
    },
    addTime() {
      this.$emit('add-time', 15);
    }
  }
};
</script>

<style scoped>
.function-buttons {
  display: flex;
  flex-direction: column;
}

button {
  margin-bottom: 5px;
}
</style>
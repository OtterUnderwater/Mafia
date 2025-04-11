<template>
  <button class="button-role" @click="handleClick">
    {{ index + 1 }}
  </button>
</template>

<script>
export default {
  props: {
    item: {
      type: String,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  methods: {
    handleClick() {
      this.$emit('show-role', this.index);
    },
  },
};
</script>

<style scoped>
.button-role {
  background-color: white;
  color: black;
  border: 1px solid black;
  padding: 10px;
  cursor: pointer;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.button-role:hover {
  background-color: #0BDB83;
}
</style>
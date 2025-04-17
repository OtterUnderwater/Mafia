<template>
  <div class="container">
    <button @click="handleClick" class="btn-next">NEXT STAGE</button>
    <div class="stage-title">{{ titleStage }}</div>
  </div>
</template>

<script>

export default {
  props: {
    item: {
      type: Object,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
    idStage: {
      type: Number,
      required: true,
    },
  },

  computed: {
    titleStage() {
      switch (this.idStage) {
        case 0:
          return "Night\n The Don and the Mafia wake up";
        case 1:
          return "Night\n The Sheriff wake up";
        default:
          return "Morning\n The city is waking up";
      }
    }
  },

  methods: {
    handleClick() {
      this.$emit('next-stage');
    }
  }
};
</script>

<style scoped lang="scss">
@use "@/assets/styles/colors" as *;

.container {
  display: flex;
  flex-direction: column;
  width: 200px;
}

.btn-next {
  width: 100%;
  min-height: 40px;
  padding: 10px 15px;
  border: 1px solid $black;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  background-color: $red;
  color: $black;
  &:hover {
    background-color: $dark-red;
  }
}

.stage-title {
  margin-top: 10px;
  padding: 10px 20px;
  border-radius: 4px;
  border: 1px solid $red;
  color: white;
  font-size: 14px;
  flex-grow: 1;
  white-space: pre-line;
  display:flex;
  justify-content:center;
  align-items:center;
  text-align:center;
  min-height: 100px;
}
</style>
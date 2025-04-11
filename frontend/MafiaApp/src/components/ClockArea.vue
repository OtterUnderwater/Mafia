<template>
  <div class="clock-area">
    <span>{{ formattedTime }}</span>
  </div>
</template>

<script>
export default {
  props: {
    totalSeconds: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      remainingTime: this.totalSeconds,
      timer: null
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.remainingTime / 60);
      const seconds = this.remainingTime % 60;
      return `${this.padZero(minutes)}:${this.padZero(seconds)}`;
    }
  },
  methods: {
    padZero(num) {
      return num < 10 ? '0' + num : num;
    },
    startTimer() {
      this.timer = setInterval(() => {
        if (this.remainingTime > 0) {
          this.remainingTime--;
        } else {
          clearInterval(this.timer);
        }
      }, 1000);
    }
  },
  mounted() {
    this.startTimer();
  },
  beforeDestroy() {
    clearInterval(this.timer);
  }
};
</script>

<style scoped>
.clock-area {
  font-size: 24px; /* Размер шрифта для таймера */
}
</style>
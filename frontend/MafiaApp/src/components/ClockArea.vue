<template>
  <div :class="['clock-area', colorTime]">
    <span>{{ formattedTime }}</span>
  </div>
</template>

<script>
export default {
  props: {
    totalSeconds: {
      type: Number,
      required: true
    },
    isPaused: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      remainingTime: this.totalSeconds,
      timer: null
    };
  },
  watch: {
    totalSeconds(newVal) {
      this.remainingTime = newVal;
    },
    isPaused(newVal) {
      if (newVal) {
        this.stopTimer();
      } else {
        this.startTimer();
      }
    }
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.remainingTime / 60);
      const seconds = this.remainingTime % 60;
      if (!this.isPaused){
        this.startTimer();
      }  
      return `${this.padZero(minutes)}:${this.padZero(seconds)}`;
    },  
    colorTime() {
      if (this.remainingTime <= 5) return 'red-time';
      return '';
    }
  },
  methods: {
    padZero(num) {
      return num < 10 ? '0' + num : num;
    },
    startTimer() {
      if (this.timer) return;
      this.timer = setInterval(() => {
        if (this.remainingTime > 0) {
          this.remainingTime--;
          this.$emit('update:totalSeconds', this.remainingTime);
        } else {
          this.stopTimer();
        }
      }, 1000);
    },
    stopTimer() {
      clearInterval(this.timer);
      this.timer = null;
    }
  },
  mounted() {
    if (!this.isPaused) {
      this.startTimer();
    }
  }
};
</script>

<style scoped lang="scss">
@use "@/assets/styles/colors" as *;

.clock-area {
  font-size: 24px;
  border-radius: 4px;
  border: 1px solid white;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;    
  min-height: 150px;
}

.red-time {
  border: 1px solid $red;
  color: $red;
}
</style>
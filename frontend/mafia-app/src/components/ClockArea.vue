<template>
  <v-card
    :border="`md opacity-100 double ${remainingTime <= 5 ? 'accent' : 'text'}`"
    class="d-flex align-center justify-center flex-grow-1 pa-0 ma-0"
    height="100%"
    rounded
    style="background-color: #161819;"
  >
    <v-card-text :class="[ remainingTime <= 5 ? 'text-accent' : 'text-text', 'text-h4', 'text-center']">
      {{ formattedTime }}
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
  import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

  const props = defineProps({
    totalSeconds: {
      type: Number,
      required: true,
    },
    isPaused: {
      type: Boolean,
      required: true,
    },
  })

  const emit = defineEmits(['update:totalSeconds'])

  const remainingTime = ref(props.totalSeconds)
  const timer = ref(null)

  const formattedTime = computed(() => {
    const minutes = Math.floor(remainingTime.value / 60);
    const seconds = remainingTime.value % 60;
    if (!props.isPaused){
      startTimer();
    }
    return `${padZero(minutes)}:${padZero(seconds)}`
  })

  const padZero = (num: number): string => {
    return num < 10 ? `0${num}` : num.toString()
  }

  const startTimer = () => {
    if (timer.value !== null) return
    timer.value = window.setInterval(() => {
      if (remainingTime.value > 0) {
        remainingTime.value--
        emit('update:totalSeconds', remainingTime.value)
      } else {
        stopTimer()
        remainingTime.value = 0;
        emit('update:totalSeconds', remainingTime.value);
      }
    }, 1000)
  }

  const stopTimer = () => {
    if (timer.value !== null) {
      clearInterval(timer.value)
      timer.value = null
    }
  }

  watch(() => props.totalSeconds, newVal => {
    remainingTime.value = newVal
  })

  watch(() => props.isPaused, newVal => {
    if (newVal) {
      stopTimer()
    } else {
      startTimer()
    }
  })

  onMounted(() => {
    if (!props.isPaused) {
      startTimer()
    }
  })

  onBeforeUnmount(() => {
    stopTimer()
  })
</script>

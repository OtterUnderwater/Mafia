<template>
  <div class="container">
    <button @click="handleClick">NEXT STAGE</button>
    <div class="stage-title">{{ titleStage }}</div>
  </div>
</template>

<script setup lang="ts">
  import { defineProps } from "vue";

  const props = defineProps<{
    idStage: number;
  }>();

  const emit = defineEmits<{
    (e: 'next-stage'): void;
  }>();

  const titleStage = computed(() => {
    switch (props.idStage) {
      case 0:
        return "Night\n The Don and the Mafia wake up";
      case 1:
        return "Night\n The Sheriff wake up";
      default:
        return "Morning\n The city is waking up";
    }
  });

  const handleClick = () => {
    emit('next-stage');
  };
</script>

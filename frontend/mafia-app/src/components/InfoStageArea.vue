<template>
  <v-card class="pa-0 ma-0 d-flex flex-column flex-grow-1" color="transparent">
    <v-btn v-if="store.isHost" block class="mb-2" color="primary" @click="handleClick">NEXT STAGE</v-btn>
    <v-card class="pa-4 ma-0 d-flex justify-center align-center h-100">
      {{ titleStage }}
    </v-card>
  </v-card>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue';
  import { useAppStore } from '@/stores/app.ts';

  const store = useAppStore();
  const props = defineProps<{
    idStage: number;
  }>();

  const emit = defineEmits<{
    (e: 'next-stage'): void;
  }>();

  const titleStage = computed(() => {
    switch (props.idStage) {
      case 0:
        return 'Night\n The Don and the Mafia wake up';
      case 1:
        return 'Night\n The Sheriff wake up';
      default:
        return 'Morning\n The city is waking up';
    }
  });

  const handleClick = () => {
    emit('next-stage');
  };
</script>

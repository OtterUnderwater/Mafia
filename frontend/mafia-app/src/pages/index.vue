<template>
  <v-container class="mt-8 pa-4" max-width="600">
    <div v-if="access_token === ''">
      <PlayerNicknameForm />
    </div>
    <div v-else>
      <div v-if="!gameStarted">
        <StartOnlineGame @start-game="startGame" />
      </div>
      <div v-else>
        <CreatingGame />
      </div>
    </div>
  </v-container>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useAppStore } from '@/stores/app.ts';

  const store = useAppStore();
  const access_token = computed(() => store.access_token);
  const gameStarted = ref(false)
  const startGame = () => gameStarted.value = true;
</script>

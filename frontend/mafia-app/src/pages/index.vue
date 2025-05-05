<template>
  <v-container class="pa-4" max-width="600">
    <div v-if="!gameStarted">
      <PlayerNicknameForm @start-game="startGame" />
    </div>
    <div v-else>
      <RoleSelection />
    </div>
  </v-container>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  const gameStarted = ref(false)
  const startGame = () => gameStarted.value = true;
</script>

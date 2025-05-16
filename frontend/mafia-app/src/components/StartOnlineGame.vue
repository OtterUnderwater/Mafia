<template>
  <v-container>
    <v-row align="stretch">
      <v-col cols="12" md="6" class="d-flex">
        <v-btn
          block
          color="primary"
          size="x-large"
          @click="createGame"
          min-height="56"
          class="h-100"
          variant="flat"
        >
          Create the game
        </v-btn>
      </v-col>
      <v-col cols="12" md="6" class="d-flex flex-column">
        <v-text-field
          v-model="gameId"
          label="Game ID"
          variant="outlined"
          :rules="[v => !!v || 'Game ID is required']"
          hide-details="auto"
        ></v-text-field>

        <v-spacer class="my-2"></v-spacer>

        <v-btn
          block
          color="primary"
          size="x-large"
          @click="joinGame"
          :disabled="!gameId"
          class="mt-2"
          variant="flat"
        >
          Join the game
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { ApiClient } from '@/domain/api-client.js';
  import { WebSocketService } from '@/domain/web-socket-client.js';

  const api = new ApiClient();
  const gameId = ref('');
  const ws = new WebSocketService();
  const emit = defineEmits(['start-game']);

  const createGame = async () => {
    try{
      await api.postGame();
      ws.connect();
      emit('start-game');
    }
    catch (e) {
      alert(e)
    }
  };

  const joinGame = async () => {
    if (gameId.value) {
      await api.postPlayerStatus(gameId.value);
      await api.getPlayersStatus();
      ws.connect();
      emit('start-game');
      //router.push('/CreatingGame');
    }
  }
</script>

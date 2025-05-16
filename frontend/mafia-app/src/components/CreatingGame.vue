<template>
  <v-container class="pa-4">
    <v-card class="mb-6" color="primary" dark>
      <v-card-title class="text-h6 justify-center">
        Game ID: {{ gameId }}
      </v-card-title>
    </v-card>
    <div class="mb-4 justify-center" style="font-size: 1.25rem; font-weight: 500;">
      You need 10 players to start the game.
    </div>
    <div v-if="players.length > 0">
      <v-row>
        <v-col
          v-for="player in players"
          :key="player.id"
          cols="12"
          md="4"
          sm="6"
        >
          <v-card class="pa-3" outlined>
            <div class="d-flex align-center">
              {{ player.id }}. {{ player.nickname }}
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div v-else class="mt-4" style="font-size: 1.2rem;">
      Share the game ID with the players so they can join.
    </div>
    <v-fade-transition>
      <div v-if="players.length >= 10" class="text-center mt-6">
        <v-btn
          color="success"
          x-large
          @click="handleStartGame"
        >
          Start game
          <v-icon right>mdi-play</v-icon>
        </v-btn>
      </div>
    </v-fade-transition>
  </v-container>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app';
  import { computed } from 'vue';
  import { useRouter } from 'vue-router';

  const store = useAppStore();
  const gameId = computed(() => store.gameId);
  const players = computed(() => store.players);

  const router = useRouter()
  const handleStartGame = () => {
    router.push('/RoleSelection');
  };
</script>

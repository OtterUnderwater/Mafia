<template>
  <v-card>
    <v-card-title class="d-flex justify-center pa-4">
      <h3 class="text-h5 text-center">
        Start the game without registration
      </h3>
    </v-card-title>
    <v-card-text>
      <v-form
        ref="form"
        v-model="formValid"
        lazy-validation
      >
        <v-row dense>
          <v-col
            v-for="player in players"
            :key="player.id"
            class="pa-2"
            cols="12"
            sm="6"
          >
            <v-text-field
              v-model="player.nickname"
              :label="`Player ${player.id} Nickname`"
              required
              :rules="[v => !!v || 'Nickname is required']"
              variant="outlined"
            />
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="12" sm="12">
            <v-btn
              block
              color="primary"
              :disabled="!formValid || players.some(player => !player.nickname.trim())"
              height="56"
              variant="flat"
              @click="handleStartGame"
            >
              Start the game
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app.js';
  import { computed, ref } from 'vue';

  const formValid = ref(false);
  const emit = defineEmits(['start-game']);
  const store = useAppStore();
  const players = computed(() => store.players);

  const handleStartGame = () => {
    store.setPlayers(players.value);
    emit('start-game');
  };
</script>

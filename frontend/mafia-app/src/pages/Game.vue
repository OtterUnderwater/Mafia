<template>
  <v-card class="pa-4" color="transparent">
    <v-row v-if="store.isHost" class="mx-auto" style="min-height: 100px; display: flex; align-items: stretch;">
      <v-col class="d-flex h-auto" cols="12" lg="4" md="3">
        <InfoStageArea :idStage="idStage" @next-stage="nextStage" />
      </v-col>
      <v-col class="d-flex h-auto" cols="12" lg="4" md="3">
        <ClockArea :isPaused="isPaused" :totalSeconds="totalSeconds" @update:totalSeconds="val => totalSeconds = val" />
      </v-col>
      <v-col class="d-flex h-auto" cols="12" lg="4" md="6">
        <FunctionButtons :isPaused="isPaused" @toggle-pause="togglePause" @add-time="addTime" />
      </v-col>
    </v-row>
    <v-row v-else class="mx-auto" style="min-height: 100px; display: flex; align-items: stretch;">
      <v-col class="d-flex h-auto" cols="12" lg="6" md="6">
        <InfoStageArea :idStage="idStage" @next-stage="nextStage" />
      </v-col>
      <v-col class="d-flex h-auto" cols="12" lg="6" md="6">
        <ClockArea :isPaused="isPaused" :totalSeconds="totalSeconds" @update:totalSeconds="val => totalSeconds = val" />
      </v-col>
    </v-row>
    <v-row class="d-flex flex-wrap justify-center" style="gap: 10px;">
      <v-col
        v-for="player in players"
        :key="player.id"
        class="flex-grow-0"
        style="flex: 0 0 calc(20% - 8px); width: 360px;"
      >
        <div class="d-flex flex-column align-center">
          <PlayerCard :player="player" />
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app';
  import { computed, ref } from 'vue';
  const store = useAppStore();
  const players = computed(() => store.players);

  const totalSeconds = ref(60);
  const isPaused = ref(false);
  const idStage = ref(0);

  const togglePause = () => {
    isPaused.value = !isPaused.value;
  };

  const addTime = () => {
    totalSeconds.value += 10;
  };

  const nextStage = () => {
    totalSeconds.value = 0;
    idStage.value++;
    if (idStage.value >= 3) {
      idStage.value = 0;
    }
    const stageTimes = [60, 20, 180];
    totalSeconds.value = stageTimes[idStage.value];
  };
</script>

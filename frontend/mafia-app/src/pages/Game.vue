<template>
  <v-row class="mb-6 align-center">
    <v-col cols="12" md="3" lg="4">
      <ClockArea :isPaused="isPaused" :totalSeconds="totalSeconds" @update:totalSeconds="val => totalSeconds = val"/>
    </v-col>

    <v-col cols="12" md="3" lg="4">
      <InfoStageArea :idStage="idStage" @next-stage="nextStage"/>
    </v-col>

    <v-col cols="12" md="6" lg="4">
      <FunctionButtons :isPaused="isPaused" @toggle-pause="togglePause" @add-time="addTime"/>
    </v-col>
  </v-row>

  <v-row class="d-flex flex-wrap">
    <v-col
      v-for="player in players"
      :key="player.id"
      class="flex-grow-0"
      style="flex-basis: 20%; max-width: 20%; min-width: 20%;"
    >
      <PlayerCard
        :player="player"
        class="flex-grow-1 d-flex flex-column"
      />
    </v-col>
  </v-row>
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


<style scoped>

</style>

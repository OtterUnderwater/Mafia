<template>
  <v-card
    class="pa-4 text-white mx-auto"
    color="#99948E"
    rounded
  >
    <v-card
      class="pa-4 text-white mx-auto"
      color="#161819"
      max-width="170"
      rounded
    >
      <h4 class="text-h5 font-weight-bold mb-4 text-center">Player №{{ player.id }}</h4>

      <v-card
        :border="`md opacity-100 double ${isMafiaRole ? 'accent' : 'tooltip'}`"
        class="pa-1 text-center bg-transparent"
        max-width="130"
        rounded="lg"
      >
        <h4 class="font-weight-bold" :class="isMafiaRole ? 'text-accent' : 'text-tooltip'">{{ player.role }}</h4>
      </v-card>

      <p class="mt-4 mb-2 text-tooltip">
        {{ player.nickname }}
      </p>

      <p class="mb-4 text-tooltip">
        {{ player.status }}
      </p>
      {{ player.fouls }}
      <v-row class="pa-0 ma-0" justify="space-between" align="center" style="width: 100%">
        <v-col
          v-for="n in 4"
          :key="n"
          cols="3"
          class="pa-0"
          style="text-align: center"
        >
          <v-icon
            :color="n <= player.fouls ? 'accent' : 'tooltip'"
            small
          >
            mdi-circle
          </v-icon>
        </v-col>
      </v-row>
    </v-card>
  </v-card>
</template>

<script setup lang="ts">
  import type { Player } from '@/custom_types/interfaces.ts';
  import { RoleEnum } from '@/custom_types/enums.ts';

  const props = defineProps<{
    player: Player
  }>();

  // const playerFouls = computed(() => {
  //   props.player.fouls
  // });

  const isMafiaRole = computed(() => {
    return props.player.role === RoleEnum.Mafia || props.player.role === RoleEnum.Don;
  });
</script>

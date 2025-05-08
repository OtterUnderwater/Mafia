<template>
  <v-card
    class="pa-4 text-white d-flex align-center"
    color="#99948E"
    rounded
  >
    <v-row>
      <v-card
        class="flex-grow-0 pa-0 mx-1 my-1 text-center"
        color="#161819"
        :style="{
        width: '160px',
        flexShrink: 0
      }"
        rounded
      >
        img
      </v-card>

      <v-card
        class="flex-grow-1 pa-4 mx-1 my-1"
        color="#161819"
        :style="{
        width: '160px'
      }"
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
          {{
            player.status === StatusEnum.Dead
              ? `${player.status} (${player.elimination_reason})`
              : player.status
          }}
        </p>

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
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import type { Player } from '@/custom_types/interfaces.ts';
import { RoleEnum, StatusEnum } from '@/custom_types/enums.ts';

const props = defineProps<{
  player: Player
}>();

const isMafiaRole = computed(() => {
  return props.player.role === RoleEnum.Mafia || props.player.role === RoleEnum.Don;
});
</script>

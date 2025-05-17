<template>
  <v-card
    class="pa-4 text-white align-center"
    :color="player.status === StatusEnum.Alive ? 'tooltip' : 'primary'"
    rounded
    :style="{
      width: '344px'
    }"
  >
    <v-row class="align-stretch">
      <v-card
        class="flex-grow-0 mx-1 my-1"
        color="#161819"
        rounded
        :style="{
          width: '160px',
          height: '250px',
          flexShrink: 0
        }"
      >
        <v-img
          alt="Role image"
          cover
          :src="getRoleImage(player.role)"
          :style="{
            width: '100%',
            height: '100%'
          }"
        />
      </v-card>

      <v-card
        class="pa-4 mx-1 my-1"
        color="#161819"
        rounded
        :style="{
          width: '160px',
          height: '250px',
          flexShrink: 0
        }"
      >
        <div class="d-flex flex-column" style="height: 100%;">
          <div class="flex-grow-1 overflow-y-auto">
            <h4 class="text-h5 font-weight-bold mb-4 text-center">Player №{{ player.id }}</h4>

            <v-card
              v-if="store.isHost || props.player.nickname == store.username"
              :border="`md opacity-100 double ${isMafiaRole ? 'accent' : 'tooltip'}`"
              class="pa-1 text-center bg-transparent"
              max-width="130"
              rounded="lg"
            >
              <h4 class="font-weight-bold" :class="isMafiaRole ? 'text-accent' : 'text-tooltip'">{{ player.role }}</h4>
            </v-card>
            <v-card
              v-else
              :border="`md opacity-100 double tooltip`"
              class="pa-1 text-center bg-transparent"
              max-width="130"
              rounded="lg"
            >
              <h4 class="font-weight-bold text-tooltip"> Role </h4>
            </v-card>

            <p class="mt-4 mb-2 text-tooltip">
              {{ player.nickname }}
            </p>

            <p class="mb-4 text-tooltip">
              {{ player.status === StatusEnum.Dead ? `${player.status} (${player.elimination_reason})` : player.status }}
            </p>
          </div>
          <v-row align="center" class="pa-0 ma-0 mt-2 flex-grow-0">
            <v-col
              v-for="n in 4"
              :key="n"
              class="pa-0 ma-0"
              cols="3"
              style="text-align: center"
            >
              <v-icon
                :color="n <= player.fouls ? 'accent' : 'tooltip'"
                small
                style="margin: 0; padding: 0"
              >
                mdi-circle
              </v-icon>
            </v-col>
          </v-row>
        </div>
      </v-card>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
  import type { Player } from '@/custom_types/interfaces.ts';
  import { RoleEnum, StatusEnum } from '@/custom_types/enums.ts';
  import donImage from '@/assets/images/don.png';
  import sheriffImage from '@/assets/images/sheriff.png';
  import mafiaImage from '@/assets/images/mafia.png';
  import civilianImage from '@/assets/images/civilian.png';
  import { useAppStore } from '@/stores/app.ts';

  const props = defineProps<{
    player: Player
  }>();

  const isMafiaRole = computed(() => {
    return props.player.role === RoleEnum.Mafia || props.player.role === RoleEnum.Don;
  });

  const store = useAppStore();
  const getRoleImage = (role: RoleEnum) => {
    if (store.isHost || props.player.nickname === store.username) {
      const images = {
        [RoleEnum.Don]: donImage,
        [RoleEnum.Sheriff]: sheriffImage,
        [RoleEnum.Mafia]: mafiaImage,
        [RoleEnum.Civilian]: civilianImage,
      };
      return images[role];
    }
    return civilianImage;
  };
</script>

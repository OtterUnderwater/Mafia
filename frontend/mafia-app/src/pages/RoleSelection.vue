<template>
  <v-container class="pa-4 mt-8" max-width="600">
    <v-card>
      <v-card-title class="d-flex flex-wrap text-wrap">
        Select Roles Mode
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" class="py-1">
            <v-btn
              block
              class="ma-1"
              :color="selectedMode === 'random' ? 'primary' : 'secondary'"
              variant="flat"
              @click="handleRandomMode"
            >
              Random
            </v-btn>
          </v-col>

          <v-col cols="12" sm="6" class="py-1">
            <v-btn
              block
              :color="selectedMode === 'manual' ? 'primary' : 'secondary'"
              @click="handleManualMode"
              variant="flat"
              class="ma-1"
            >
              Manual
            </v-btn>
          </v-col>
        </v-row>

        <!-- Manual mode -->
        <div v-if="selectedMode === 'manual'" class="mt-4">
          <div class="text-body-1 mb-4">
            Select the role number
          </div>

          <div class="d-flex flex-wrap">
            <v-dialog
              v-for="(num, index) in availableNumbers"
              :key="index"
              cols="2"
              max-width="400"
              sm="3"
              md="4"
              lg="6"
              @after-leave="assignRole(num)"
            >
              <template v-slot:activator="{ props: activatorProps }">
                <v-btn
                  class="mx-2 mb-2"
                  v-bind="activatorProps"
                  color="secondary"
                  width="90"
                  variant="flat"
                >
                  {{ index + 1 }}
                </v-btn>
              </template>


              <template v-slot:default="{ isActive }">
                <v-card>
                  <v-card-title class="text-h5">
                    Your role: {{ rolesRandom[num] }}
                  </v-card-title>
                  <v-img
                    :src="getRoleImage(rolesRandom[num])"
                    height="200"
                    contain
                    alt="Role image"
                  />
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      class="text-h6"
                      @click="isActive.value = false;"
                      variant="flat"
                    >
                      OK
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </template>
            </v-dialog>
          </div>
        </div>

        <!-- Random mode -->
        <div v-if="selectedMode === 'random'" class="mt-4">
          <p class="text-body-1">Roles are assigned randomly</p>
        </div>
        <v-btn
          v-if="availableNumbers.length === 0 || selectedMode === 'random'"
          block
          class="mt-4"
          color="success"
          variant="flat"
          @click="confirmRoles"
        >
          Next
        </v-btn>

      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app';
  import { RoleEnum } from '@/custom_types/enums.ts';
  import { computed, ref } from 'vue';
  import { shuffle } from '@/functions/methodsArray.ts';
  import { useRouter } from 'vue-router'
  import { ApiClient } from '@/domain/api-client.js';

  const store = useAppStore();
  const players = computed(() => store.players);
  const selectedMode = ref<'random' | 'manual' | null>(null);
  const roleList: RoleEnum[] = [
    RoleEnum.Don,
    RoleEnum.Sheriff,
    RoleEnum.Mafia,
    RoleEnum.Mafia,
    RoleEnum.Civilian,
    RoleEnum.Civilian,
    RoleEnum.Civilian,
    RoleEnum.Civilian,
    RoleEnum.Civilian,
    RoleEnum.Civilian,
  ];
  const rolesRandom = ref<RoleEnum[]>(shuffle([...roleList]));

  const handleRandomMode = () => {
    selectedMode.value = 'random';
    rolesRandom.value = shuffle([...roleList]);
    players.value.forEach((_, index) => {
      players.value[index].role = rolesRandom.value[index];
    });
  };

  const currentPlayerIndex = ref(0);
  const availableNumbers = ref<number[]>(Array.from({ length: 10 }, (_, i) => i + 1));

  const handleManualMode = () => {
    selectedMode.value = 'manual';
    rolesRandom.value = shuffle([...roleList]);
    availableNumbers.value = Array.from({ length: 10 }, (_, i) => i);
    currentPlayerIndex.value = 0;
  };

  const assignRole = (roleIndex: number) => {
    if (currentPlayerIndex.value >= store.players.length) return;
    currentPlayerIndex.value++;
    availableNumbers.value = availableNumbers.value.filter(n => n !== roleIndex);
  };

  const api = new ApiClient();
  const router = useRouter();
  const confirmRoles = async () => {
    selectedMode.value = null;
    store.setPlayers(players.value);
    if (store.access_token !== '') {
      for (const player of players.value) {
        await api.updatePlayerStatus(
          player.idPS,
          player.role,
          null,
          null,
          null
        );
      }
    }
    await router.push('/Game')
  };

  import donImage from '@/assets/images/don.png'
  import sheriffImage from '@/assets/images/sheriff.png'
  import mafiaImage from '@/assets/images/mafia.png'
  import civilianImage from '@/assets/images/civilian.png'

  const getRoleImage = (role: RoleEnum) => {
    const images = {
      [RoleEnum.Don]: donImage,
      [RoleEnum.Sheriff]: sheriffImage,
      [RoleEnum.Mafia]: mafiaImage,
      [RoleEnum.Civilian]: civilianImage,
    };
    return images[role];
  };
</script>

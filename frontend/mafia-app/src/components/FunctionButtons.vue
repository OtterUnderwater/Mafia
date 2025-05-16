<template>
  <v-container class="flex-grow-1 pa-0 ma-0 h-100">
    <v-row class="function-buttons">
      <v-col>
        <v-btn block class="mb-2 my-4" color="primary" @click="togglePause">
          {{ isPaused ? 'Resume' : 'Pause' }}
        </v-btn>
        <v-btn block class="mb-2 my-4" color="primary" @click="addTime">Add time</v-btn>
      </v-col>
      <v-col>
        <v-btn block class="mb-2 my-4" color="primary" @click="openActionPopup('awardFoul')">Award Foul</v-btn>
        <v-btn block class="mb-2 my-4" color="primary" @click="openActionPopup('killed')">Killed</v-btn>
        <v-btn block class="my-4" color="primary" @click="openActionPopup('kickedOut')">Kicked out</v-btn>
      </v-col>
    </v-row>

    <v-dialog v-model="showActionPopup" max-width="600px">
      <v-card>
        <v-card-text>
          <h3 class="text-h5 text-center mt-2">
            {{ popupTitle }}
          </h3>
          <div v-if="currentAction != null">
            <v-btn
              v-for="player in alivePlayers"
              :key="player.id"
              block
              class="mb-2 my-4 text-wrap"
              color="primary"
              @click="performAction(currentAction, player.id - 1)"
            >
              Player №{{ player.id }}. {{ player.nickname || '' }}
            </v-btn>
          </div>
          <v-btn block class="my-4 opacity-100" color="secondary" @click="closeActionPopup">Cancel</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showPopupVictory" max-width="400px">
      <v-card>
        <v-card-title>
          <span>Victory of the {{ victory }}</span>
        </v-card-title>
        <v-card-actions>
          <v-btn @click="showPopupVictory = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app';
  import { defineProps } from 'vue';
  import { EliminationReasonEnum, RoleEnum, StatusEnum, ResultEnum } from '@/custom_types/enums.ts';
  import { ApiClient } from '@/domain/api-client';

  const props = defineProps<{
    isPaused: boolean;
  }>();

  const emit = defineEmits<{
    (e: 'toggle-pause'): void;
    (e: 'add-time'): void;
  }>();

  const store = useAppStore();
  const players = computed(() => store.players);

  const showActionPopup = ref(false);
  const showPopupVictory = ref(false);
  const victory = ref('');
  const currentAction = ref('');

  const alivePlayers = computed(() => {
    return players.value.filter(player => player.status === StatusEnum.Alive);
  });

  const popupTitle = computed(() =>{
    switch (currentAction.value) {
      case 'killed':
        return 'Select Player to Kill';
      case 'awardFoul':
        return 'Award Foul';
      case 'kickedOut':
        return 'Kick Out Player';
      default:
        return 'Confirm Action';
    }
  });

  const togglePause = () => {
    emit('toggle-pause');
  };

  const addTime = () => {
    emit('add-time');
  };

  const openActionPopup = (action: string) => {
    currentAction.value = action;
    showActionPopup.value = true;
  };

  const closeActionPopup = () => {
    showActionPopup.value = false;
    currentAction.value= '';
  };

  const victoryRole = role => {
    victory.value = role;
    showPopupVictory.value = true;
  };

  const api = new ApiClient();
  const performAction = async (action: string, index: number) => {
    switch (action) {
      case 'killed':
        store.updatePlayer({ index, property: 'status', value: StatusEnum.Dead });
        store.updatePlayer({ index, property: 'elimination_reason', value: EliminationReasonEnum.Killed });
        break;
      case 'awardFoul':
        store.updatePlayer({ index, property: 'fouls', value: players.value[index].fouls + 1 });
        if (players.value[index].fouls >= 4) {
          store.updatePlayer({ index, property: 'status', value: StatusEnum.Dead });
          store.updatePlayer({ index, property: 'elimination_reason', value: EliminationReasonEnum.Deleted });
        }
        break;
      case 'kickedOut':
        store.updatePlayer({ index, property: 'status', value: StatusEnum.Dead });
        store.updatePlayer({ index, property: 'elimination_reason', value: EliminationReasonEnum.Voted });
        break;
      default: break;
    }
    if (store.access_token !== '') {
      await api.updatePlayerStatus(
        players.value[index].idPS,
        null,
        players.value[index].fouls,
        players.value[index].status,
        players.value[index].elimination_reason,
      );
    }
    closeActionPopup();
    let countMafia = 0;
    let countCivilian = 0;
    for(let i = 0; i < players.value.length; i++) {
      if (players.value[i].status === StatusEnum.Alive)
        if (players.value[i].role === RoleEnum.Mafia || players.value[i].role === RoleEnum.Don)
          countMafia++;
        else
          countCivilian++;
    }
    if(countMafia <= 0) {
      victoryRole(RoleEnum.Civilian);
      if (store.access_token !== '') await api.updateGame(ResultEnum.CiviliansWin);
    }
    else if(countCivilian < countMafia) {
      victoryRole(RoleEnum.Mafia);
      if (store.access_token !== '') await api.updateGame(ResultEnum.MafiaWin);
    }
  };
</script>

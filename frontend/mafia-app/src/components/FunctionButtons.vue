<template>
  <v-container>
    <v-row class="function-buttons">
      <v-col>
        <v-btn color="primary" @click="togglePause">
          {{ isPaused ? 'Resume' : 'Pause' }}
        </v-btn>
        <v-btn color="primary" @click="addTime">Add time</v-btn>
        <v-btn color="primary" @click="openActionPopup('awardFoul')">Award Foul</v-btn>
        <v-btn color="primary" @click="openActionPopup('killed')">Killed</v-btn>
        <v-btn color="primary" @click="openActionPopup('kickedOut')">Kicked out</v-btn>
      </v-col>
    </v-row>

    <v-dialog v-model="showActionPopup" max-width="600px">
      <v-card>
        <v-card-title>
          <span>{{ popupTitle }}</span>
        </v-card-title>
        <v-card-text>
          <div v-if="currentAction != null" class="player-list">
            <v-btn
              v-for="(player, index) in alivePlayers"
              :key="player.id"
              @click="performAction(currentAction, index)"
              color="primary"
              class="mb-2"
              block
            >
              {{ index + 1 }}. {{ player.nickname || '' }}
            </v-btn>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="closeActionPopup" color="grey" text>Cancel</v-btn>
        </v-card-actions>
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
import { defineProps } from "vue";
import {EliminationReasonEnum, RoleEnum, StatusEnum} from "@/custom_types/enums.ts";

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
const victory = null;
const currentAction = ref('');

const alivePlayers = computed(() => {
  return players.value.filter((player) => player.status === StatusEnum.Alive);
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
  currentAction.value= action;
  showActionPopup.value = true;
};

const closeActionPopup = () => {
  showActionPopup.value = false;
  currentAction.value= null;
};

const victoryRole = (role) => {
  victory.value = role;
  showPopupVictory.value = true;
};

const performAction = (action: string, index: number) => {
  switch (action) {
    case 'killed':
      store.updatePlayer({ index: index, property: 'status', value: StatusEnum.Dead });
      store.updatePlayer({ index: index, property: 'elimination_reason', value: EliminationReasonEnum.Killed });
      break;
    case 'awardFoul':
      store.updatePlayer({ index: index, property: 'fouls', value: this.players[index].fouls + 1 });
      if (players.value[index].fouls >= 4) {
        store.updatePlayer({ index: index, property: 'status', value: StatusEnum.Dead });
        store.updatePlayer({ index: index, property: 'elimination_reason', value: EliminationReasonEnum.Deleted });
      }
      break;
    case 'kickedOut':
      store.updatePlayer({ index: index, property: 'status', value: StatusEnum.Dead });
      store.updatePlayer({ index: index, property: 'elimination_reason', value: EliminationReasonEnum.Voted });
      break;
    default: break;
  }
  this.closeActionPopup()
  let countMafia = 0;
  let countCivilian = 0;
  for(let i = 0; i < players.value.length; i++) {
    if (players.value[i].status === StatusEnum.Alive)
      if (players.value[i].role === RoleEnum.Mafia || players.value[i].role === RoleEnum.Don)
        countMafia++;
      else
        countCivilian++;
  }
  if(countMafia <= 0)
  {
    this.victoryRole(RoleEnum.Civilian);
  }
  else if(countCivilian < countMafia)
  {
    this.victoryRole(RoleEnum.Mafia);
  }

};
</script>

<style scoped>
button {
  width: 100%;
  min-height: 40px;
  padding: 10px 15px;
  border: 1px solid #000000;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  background-color: white;
  color: #000000;
  &:hover {
    background-color: #0BDB83;
  }
}

.function-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
  position: relative;
  width: 200px;
}

.player-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.player-list button {
  padding: 5px 10px;
  background-color: #ffffff;
  border: 1px solid #000000;
  cursor: pointer;
  color: #000000;
}

.player-list button:hover {
  background-color: #0BDB83;
}
</style>

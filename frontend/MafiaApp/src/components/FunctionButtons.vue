<template>
  <div class="function-buttons">
    <button @click="togglePause">{{ isPaused ? 'Resume' : 'Pause' }}</button>
    <button @click="addTime">Add time</button>
    <button @click="openActionPopup('awardFoul')">Award Foul</button>
    <button @click="openActionPopup('killed')">Killed</button>
    <button @click="openActionPopup('kickedOut')">Kicked out</button>
    <div v-if="showActionPopup" class="popup-overlay">
      <div class="popup">
        <h2>{{ popupTitle }}</h2>
        <div v-if="currentAction != null" class="player-list">
          <button v-for="(player) in alivePlayers" :key="player.id" @click="performAction(currentAction, players.findIndex(p => p.id === player.id))">
            {{ players.findIndex(p => p.id === player.id) + 1 }}. {{ (player.nickname) ? player.nickname : ''}}
          </button>
        </div>
        <button @click="closeActionPopup" class="close-button">Cancel</button>
      </div>
    </div>
    <div v-if="showPopupVictory" class="popup-overlay">
      <div class="popup">
        <h2> Victory of the {{victory}}</h2>
      </div>
    </div>
  </div>
</template>

<script>
import { StatusEnum, EliminationReasonEnum, RoleEnum } from '@/constants/enums.js';
import { ApiClient } from '@domain/api-client.js';
import { mapState } from 'vuex';

export default {
  props: {
    isPaused: {
      type: Boolean,
      required: true
    }
  },

  data() {
    return {
      showActionPopup: false,
      showPopupVictory: false,
      api: new ApiClient(),
      victory: null,
      currentAction: null
    };
  },

  computed: {
    ...mapState({
      players: state => state.players
    }),

    alivePlayers() {
      return this.players.filter((player) => player.status === StatusEnum.ALIVE);
    },

    popupTitle() {
      switch (this.currentAction) {
        case 'killed':
          return 'Select Player to Kill';
        case 'awardFoul':
          return 'Award Foul';
        case 'kickedOut':
          return 'Kick Out Player';
        default:
          return 'Confirm Action';
      }
    }
  },

  methods: {
    togglePause() {
      this.$emit('toggle-pause');
    },
    addTime() {
      this.$emit('add-time');
    },
    openActionPopup(action) {
      this.currentAction = action;
      this.showActionPopup = true;
    },
    closeActionPopup() {
      this.showActionPopup = false;
      this.currentAction = null;
    },
    victoryRole(role) {
      this.victory = role;
      this.showPopupVictory = true;
    },
    async performAction(action, index) {
      switch (action) {
        case 'killed':
          this.$store.commit('updatePlayer', { index: index, property: 'status', value: StatusEnum.DEAD });
          this.$store.commit('updatePlayer', { index: index, property: 'elimination_reason', value: EliminationReasonEnum.KILLED });
          break;
        case 'awardFoul':
          this.$store.commit('updatePlayer', { index: index, property: 'fouls', value: this.players[index].fouls + 1 });
          if (this.players[index].fouls >= 4) {
            this.$store.commit('updatePlayer', { index: index, property: 'status', value: StatusEnum.DEAD });
            this.$store.commit('updatePlayer', { index: index, property: 'elimination_reason', value: EliminationReasonEnum.DELETED });
          }
          break;
        case 'kickedOut':
          this.$store.commit('updatePlayer', { index: index, property: 'status', value: StatusEnum.DEAD });
          this.$store.commit('updatePlayer', { index: index, property: 'elimination_reason', value: EliminationReasonEnum.VOTED });
          break;
        default: break;
      }
      this.closeActionPopup()
      let countMafia = 0;
      let countCivilian = 0;
      for(let i = 0; i < this.players.length; i++) {
        if (this.players[i].status === StatusEnum.ALIVE)
          if (this.players[i].role === RoleEnum.MAFIA || this.players[i].role === RoleEnum.DON)
            countMafia++;
          else
            countCivilian++;
      }
      if(countMafia <= 0) 
      {
        this.victoryRole(RoleEnum.CIVILIAN);
        if (!this.$store.state.anonymousGame)
          await this.updatePlayerStatus();
      }
      else if(countCivilian < countMafia)
       {
        this.victoryRole(RoleEnum.MAFIA); 
        if (!this.$store.state.anonymousGame)
          await this.updatePlayerStatus();
      }
    },
    async updatePlayerStatus() {
      try {
        for (let i = 0; i < this.$store.state.players.length; i++) {
          await this.api.updatePlayerStatus(
            this.$store.state.players[i].idPS,
            this.$store.state.players[i].fouls,
            this.$store.state.players[i].status,
            this.$store.state.players[i].elimination_reason
          );
        }
      } catch (error) {
        console.error('Error:', error);
        alert(error);
      }
    },
  }
};
</script>

<style scoped lang="scss">
@use "@/assets/styles/colors" as *;

button {
  width: 100%;
  min-height: 40px;
  padding: 10px 15px;
  border: 1px solid $black;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  background-color: white;
  color: $black;
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

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.popup {
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  width: 300px;
  text-align: center;
  background-color: $gray;
  color: $black;
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
  border: 1px solid $black;
  cursor: pointer;
  color: $black;
}

.player-list button:hover {
  background-color: #0BDB83;
}

.close-button {
  margin-top: 15px;
  padding: 8px 15px;
  background-color: $red;
  border: 1px solid $black;
  color: $black;
  cursor: pointer;
  &:hover {
    background-color: $dark-red;
  }
}
</style>
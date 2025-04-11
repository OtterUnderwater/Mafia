<template>
    <header class="mafia-header">
      <img class="icon-mafia" src="./components/icons/IconMafia.png" alt="Mafia Icon"/>
      MAFIA
    </header>
    <main>
    <div id="app">
      <button class="start-game-button" v-if="showBtnStartGame" @click="startGame">Create a game</button>
      <div class="main-content" >
        <PlayerDropdown v-if="showPlayerDropdown" @start-distribution="startRoleDistribution"/>
        <RoleAllocationButtons :gameId="gameId" :listPlayers="listPlayers"
        v-if="showRoleAllocationButtons" @show-game="showGame"/>
        <GameComponent :listPlayers="listPlayers" v-if="showGameComponent"/>
      </div>
    </div>
  </main>
</template>

<script>
import RoleAllocationButtons from './components/RoleAllocationButtons.vue';
import PlayerDropdown from './components/PlayerDropdown.vue';
import GameComponent from './components/GameComponent.vue';
import { ApiClient } from '@domain/api-client.js';

export default {
  components: {
    RoleAllocationButtons,
    PlayerDropdown,
    GameComponent
  },

  data() {
    return {
      showBtnStartGame: true,
      showPlayerDropdown: false,
      showRoleAllocationButtons: false,
      showGameComponent: false,
      listPlayers: [],
      currentPlayerIndex: 0,
      api: new ApiClient(),
      gameId: null
    };
  },

  methods: {
    async startGame() {
      try {
        const response = await this.api.postGame();
        this.gameId = response.id;
        this.showBtnStartGame = false;
        this.showPlayerDropdown = true;
        console.log('Game created with ID:', this.gameId);
      } catch (error) {
        console.error('Error creating game:', error);
        alert('Error creating game');
      }
    },
    startRoleDistribution(players) {
      this.listPlayers = [...players];
      this.currentPlayerIndex = 0;
      this.showPlayerDropdown = false;
      this.showRoleAllocationButtons = true;
    },
    showGame(players) {    
      this.listPlayers = [...players];
      this.showRoleAllocationButtons = false;
      this.showGameComponent = true;
    }
  }
};
</script>

<style scoped>
.mafia-header {
  background-color: #dc2a0b;
  color: white;
  text-align: center;
  padding: 10px 0;
  width: 100%;
  margin: 0;
  position: fixed;
  top: 0;
  left: 0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  z-index: 1000;
  font-size: 18px;
  font-weight: bold;
}

.icon-mafia {
  filter: brightness(0) invert(1);
  height: 18px;
  margin-right: 5px;
  vertical-align: middle;
}

.start-game-button {
  background-color: #dc2a0b;
  color: white;
  cursor: pointer;
  font-size: 24px;
  padding: 15px;
  border-radius: 5px;
  border: none;
  transition: background-color .3s ease, transform .3s ease; 
}

.start-game-button:hover {
   background-color: #b22424;
}

.main-content {
  display: flex;
  justify-content: center;
}
</style>
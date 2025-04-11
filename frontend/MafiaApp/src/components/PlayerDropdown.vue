<template>
  <div>
    <label for="user-select">Choose a player: </label>
    <select id="user-select" v-model="selectedUser">
      <option v-for="user in users" :key="user.id" :value="user.id">
        {{ user.nickname }}
      </option>
    </select>
    <button @click="addPlayer">Add</button>
    
    <h3>Added Players ({{ addedPlayers.length }} / 10):</h3>
    <ul>
      <li v-for="player in addedPlayers" :key="player.id">
        {{ player.nickname }}
      </li>
    </ul>
    
    <button v-if="addedPlayers.length === 10" @click="startRoleDistribution">
      Start assigning roles
    </button>
  </div>
</template>

<script>
import { ApiClient } from '@domain/api-client.js';

export default {
  data() {
    return {
      users: [],
      selectedUser: null,
      api: new ApiClient(),
      addedPlayers: []
    };
  },
  async mounted() {
    await this.loadPlayers();
  },
  methods: {
    async loadPlayers() {
      try {
        const players = await this.api.getPlayers();
        this.users = players;
      } catch (error) {
        console.error('Failed to load players:', error);
      }
    },
    addPlayer() {
      const userToAdd = this.users.find(user => user.id === this.selectedUser);
      if (userToAdd && !this.addedPlayers.some(player => player.id === userToAdd.id)) {
        this.addedPlayers.push({...userToAdd, role: null});   
        this.users = this.users.filter(user => user.id !== this.selectedUser);
        this.selectedUser = null;
      }
    },

    startRoleDistribution() {
      this.$emit('start-distribution', this.addedPlayers);
    }
  }
};
</script>

<style scoped>
select {
  margin-top: 10px;
}
</style>
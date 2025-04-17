<template>
  <div>
    <label for="user-select">Choose a player: </label>
    <select id="user-select" v-model="selectedUser">
      <option v-for="user in users" :key="user.id" :value="user.id">
        {{ user.nickname }}
      </option>
    </select>
    <button @click="addPlayer" class="button-add">Add</button>

    <h3>Added Players ({{ addedPlayers.length }} / 10):</h3>
    <ul>
      <li v-for="player in addedPlayers" :key="player.id">
        {{ player.nickname }}
      </li>
    </ul>

    <button class="button-start" v-if="addedPlayers.length === 10" @click="startRoleDistribution">
      Start assigning roles
    </button>
  </div>
</template>

<script>
import { StatusEnum } from '@/constants/enums.js';
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
      if (this.addedPlayers.length < 10) {
        const userToAdd = this.users.find(user => user.id === this.selectedUser);
        if (userToAdd && !this.addedPlayers.some(player => player.id === userToAdd.id)) {
          this.addedPlayers.push({ ...userToAdd, role: null });
          this.users = this.users.filter(user => user.id !== this.selectedUser);
          this.selectedUser = null;
        }
      }
      else alert('You have already added 10 players');
    },
    startRoleDistribution() {
      const players = [];
      for (let i = 0; i < this.addedPlayers.length; i++) {
        players.push({
          id: this.addedPlayers[i].id,
          nickname: this.addedPlayers[i].nickname,
          status: StatusEnum.ALIVE,
          fouls: 0
        });
      }
      this.$emit('start-distribution', players);
    }
  }
};
</script>


<style scoped lang="scss">
@use "@/assets/styles/colors" as *;

label {
  font-size: 16px;
  margin: 10px;
  color: #ffffff;
}

select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid $black;
  font-size: 14px;
  margin: 10px 5px 10px 0;
  width: 200px;
}

h3 {
  margin: 20px 0 15px;
  color: #ffffff;
  font-size: 18px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f8f9fa;
  color: $black;
  border-radius: 4px;
  padding: 4px 6px;
  margin: 10px 0;
}

button {
  padding: 10px 20px;
  border: $black;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.button-add:hover {
  background-color: $gray;
}

.button-start {
  margin: 30px;
  background-color: $red;
  color: white;
  padding: 12px 25px;
  font-size: 16px;
  font-weight: bold;
}

.button-start:hover {
  background-color: $dark-red;
}

</style>
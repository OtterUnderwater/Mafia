<template>
  <div v-if="rolesToAssign.length" class="buttons-grid" @click.self="hidePopup">
    <div class="column">
      <div v-for="(item, index) in firstColumn" :key="index">
        <ButtonRole
          :item="item"
          :index="index"
          @show-role="showRole(index)" />
      </div>
    </div>
    <div class="column">
      <div v-for="(item, index) in secondColumn" :key="index">
        <ButtonRole
          :item="item"
          :index="index + 5"
          @show-role="showRole(index)" />
      </div>
    </div>
    <div v-if="showPopup && selectedRole" :class="['popup', roleColorClass]" @click="hidePopup">
      <p>{{ selectedRole }}</p>
    </div>
  </div>
</template>

<script>
import ButtonRole from './items/ButtonRole.vue';
import { ApiClient } from '@domain/api-client.js';
import { RoleEnum } from '@/constants/enums.js';

export default {
  components: {
    ButtonRole,
  },

  computed: {
    firstColumn() {
      return this.rolesToAssign.slice(0, 5);
    },
    secondColumn() {
      return this.rolesToAssign.slice(5);
    },
    roleColorClass() {
      if (!this.selectedRole) {
        return '';
      }
      if (this.selectedRole === RoleEnum.MAFIA || this.selectedRole === RoleEnum.DON) {
        return 'popup-black';
      }
      if (this.selectedRole === RoleEnum.CIVILIAN || this.selectedRole === RoleEnum.SHERIFF) {
        return 'popup-red';
      }
      return '';
    },
  },

  data() {
    return {
      roleList: ['Don', 'Sheriff', 'Mafia', 'Mafia', 'Civilian', 'Civilian', 'Civilian', 'Civilian', 'Civilian', 'Civilian' ],
      api: new ApiClient(),
      rolesToAssign: [],
      currentPlayerIndex: 0,
      showPopup: false,
      selectedRoleIndex: null,
      selectedRole: null,
    };
  },

  created() {
    this.rolesToAssign = this.shuffle([...this.roleList]);
    this.currentPlayerIndex = 0;
  },

  methods: {
    shuffle(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },

    showRole(index) {
      this.selectedRoleIndex = index;
      this.selectedRole = this.rolesToAssign[index];
      this.showPopup = true;
    },

    async assignRole() {
      if (!this.showPopup) return;
      if (this.currentPlayerIndex >= this.$store.state.players.length) return;
      const role = this.rolesToAssign[this.selectedRoleIndex];
      this.$store.commit('updatePlayer', { index: this.currentPlayerIndex, property: 'role', value: role });
      this.rolesToAssign.splice(this.selectedRoleIndex, 1);
      this.currentPlayerIndex++;
      if (this.currentPlayerIndex === this.$store.state.players.length) {
        if (!this.$store.state.anonymousGame) {
          await this.postPlayerStatus();
        }
        this.$emit('show-game');
      }
      this.selectedRoleIndex = null;
      this.selectedRole = null;
      this.showPopup = false;
    },

    async postPlayerStatus() {
      try {
        for (let i = 0; i < this.$store.state.players.length; i++) {
          const idPS = await this.api.postPlayerStatus(
            this.$store.state.players[i].id,
            this.$store.state.gameId,
            this.$store.state.players[i].role
          );
          this.$store.commit('updatePlayer', { index: i, property: 'idPS', value: idPS });
        }
      } catch (error) {
        console.error('Error when sending roles to the database:', error);
      }
    },
    
    hidePopup() {
      if (!this.showPopup) return;
      this.assignRole();
    },
  },
};
</script>

<style scoped>
.buttons-grid {
  display: flex;
  gap: 20px;
  position: relative;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 60px;
  min-height: 400px;
}

.popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  padding: 80px 40px;
  border-radius: 10px;
  z-index: 10;
}

.popup-black {
  background-color: #000000;
}

.popup-red {
  background-color: #dc2a0b;
}
</style>
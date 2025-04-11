<template>
  <div v-if="listPlayers.length" class="buttons-grid">
    <div class="column">
      <div v-for="(item, index) in firstColumn" :key="index">
        <ButtonPlayer :item="item" :index="index" @show-player="showPlayer(item)" />
      </div>
    </div>
    <div class="column">
      <div v-for="(item, index) in secondColumn" :key="index">
        <ButtonPlayer :item="item" :index="index + 5" @show-player="showPlayer(item)" />
      </div>
    </div>
  </div>
</template>

<script>
import ButtonPlayer from './ButtonPlayer.vue';

export default {
  components: {
    ButtonPlayer
  },

  props: {
    listPlayers: {
      type: Array,
      required: true,
    },
    currentRole: {
      type: String,
      default: null,
    },
  },

  computed: {
    firstColumn() {
      return this.listPlayers.slice(0, 5);
    },
    secondColumn() {
      return this.listPlayers.slice(5);
    },
  },

  data() {
    return {
      api: new ApiClient(),
      currentPlayerIndex: 0,
      showPopup: false,
      selectedRole: null,
    };
  },

  methods: {
    showPlayer(player) {
      player.showNickname = !player.showNickname;
    },
  },
};
</script>

<style scoped>
.buttons-grid {
  display: flex;
  gap: 20px;
  justify-content: center;
  position: relative;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
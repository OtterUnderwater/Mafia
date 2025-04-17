<template>
  <div v-if="players.length" class="buttons-grid">
    <div class="column">
      <div v-for="(item, index) in firstColumn" :key="index">
        <ButtonPlayer :item="item" :index="index" :idStage="idStage" @show-player="showPlayer"/>
      </div>
    </div>
    <div class="column">
      <div v-for="(item, index) in secondColumn" :key="index">
        <ButtonPlayer :item="item" :index="index + 5" :idStage="idStage" @show-player="showPlayer"/>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonPlayer from './items/ButtonPlayer.vue';
import { mapState } from 'vuex';

export default {
  components: {
    ButtonPlayer
  },
  props: {
    idStage: {
      type: Number,
      required: true
    },
  }, 
  computed: {
    ...mapState({
      players: state => state.players
    }),
    firstColumn() {
      return this.players.slice(0, 5);
    },
    secondColumn() {
      return this.players.slice(5);
    },
  },
  methods: {
    showPlayer(index) {
      this.$store.commit('updatePlayer',
      { index: index, property: 'showNickname', value: !this.$store.state.players[index].showNickname });
    }
  }
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
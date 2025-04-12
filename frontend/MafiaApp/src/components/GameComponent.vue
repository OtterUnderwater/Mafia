<template>
    <div class="content-area">
        <div class="top-row">
          <div class="box">
            <ClockArea :totalSeconds="totalSeconds" :isPaused="isPaused" @toggle-pause="togglePause" @add-time="addTime" />
          </div>
          <div class="box">
            <ControlArea />
          </div>
        </div>
  
        <div class="bottom-row">
          <div class="box">
            <PlayerButtons :listPlayers="listPlayers" :currentRole="currentRole"/>
          </div>
          <div class="box">
            <FunctionButtons :isPaused="isPaused" @toggle-pause="togglePause" @add-time="addTime" />
          </div>
        </div>
      </div>
</template>

<script>
import ClockArea from './ClockArea.vue';
import ControlArea from './ControlArea.vue';
import PlayerButtons from './PlayerButtons.vue';
import FunctionButtons from './FunctionButtons.vue';

export default {
    components: {
      ClockArea,
      ControlArea,
      PlayerButtons,
      FunctionButtons
    },
    
    props: {
      listPlayers: {
        type: Array,
        required: true
      }
    },

    data() {
      return {
        totalSeconds: 30,
        isPaused: true,
        rolesTime: [ 'Don', 'Mafia', 'Sheriff'],
        currentRole: null
      };
    },

    created() {
      this.currentRole = this.rolesTime[0]
    },

    methods: {
      togglePause() {
        this.isPaused = !this.isPaused;
      },
      addTime(seconds) {
        this.totalSeconds += seconds;
        if (!this.isPaused) {
          this.$refs.clockArea.remainingTime += seconds;
        }
      }
    }
  };
</script>
  
<style scoped>

.content-area {
  display: center;
  flex-direction: column;
  margin-top: 70px;
  padding: 20px;
  box-sizing: border-box;
  height: calc(100vh - 70px);
}

.top-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.top-row > * {
  width: 48%;
}

.bottom-row {
  display: flex;
  justify-content: space-between;
  flex: 1;
}

.bottom-row > * {
  width: 48%;
}

.box {
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-sizing: border-box;
}

</style>

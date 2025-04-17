<template>
    <div class="content-area">
        <div class="top-row">
          <div class="box">
            <ClockArea :totalSeconds="totalSeconds" :isPaused="isPaused" @update:totalSeconds="val => totalSeconds = val"/>
          </div>
          <div class="box">
            <ControlArea :idStage="idStage" @next-stage="nextStage"/>
          </div>
        </div>
        <div class="bottom-row">
          <div class="box">
            <PlayerButtons :idStage="idStage"/>
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
    
    data() {
      return {
        totalSeconds: 60,
        isPaused: false,
        idStage: 0
      };
    },

    methods: {
      togglePause() {
        this.isPaused = !this.isPaused;
      },
      addTime() {
        this.totalSeconds += 10;
      },
      nextStage() {
        this.totalSeconds = 0;
        this.idStage = this.idStage + 1;
        if (this.idStage >= 3) {
          this.idStage = 0;
        }
        if (this.idStage === 0) {
          this.totalSeconds = 60;
        }
        if (this.idStage === 1) {
          this.totalSeconds = 20;
        }
        if (this.idStage === 2) {
          this.totalSeconds = 180;
        }
      },
      beforeDestroy() {
        this.stopTimer();
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

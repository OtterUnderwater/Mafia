import { createStore } from 'vuex'

const store = createStore({
  state: {
    gameId: 0,
    anonymousGame: false,
    players: [],
  },
  mutations: {
    setGameId(state, gameId) {
      state.gameId = gameId;
    },
    setAnonymousGame(state, anonymousGame) {
      state.anonymousGame = anonymousGame;
    },
    setPlayers(state, players) {
      state.players = players;
    },
    updatePlayer(state, { index, property, value }) {
      if (state.players[index]) {
        state.players[index][property] = value;
      }
    }
  },
});

export default store;
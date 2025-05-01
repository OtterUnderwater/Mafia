// Utilities
import { defineStore } from 'pinia'
import type { Player } from '@/custom_types/interfaces.ts';

export const useAppStore = defineStore('app', {
  state: () => ({
    gameId: 0 as number,
    anonymousGame: false as boolean,
    players: [] as Player[],
  }),
  actions: {
    setGameId (gameId: number) {
      this.gameId = gameId;
    },
    setAnonymousGame (anonymousGame: boolean) {
      this.anonymousGame = anonymousGame;
    },
    setPlayers (players: Player[]) {
      this.players = players;
    },
    updatePlayer ({ index, property, value }: { index: number; property: keyof Player; value: never }) {
      if (this.players[index]) {
        this.players[index][property] = value;
      }
    },
  },
})

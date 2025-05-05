// Utilities
import { defineStore } from 'pinia'
import { RoleEnum, StatusEnum } from '@/custom_types/enums.ts';
import type { Player } from '@/custom_types/interfaces.ts';

export const useAppStore = defineStore('app', {
  state: () => ({
    gameId: 0 as number,
    anonymousGame: false as boolean,
    isHost: false as boolean,
    players: Array.from({ length: 10 }, (_, index) => ({
      id: index + 1,
      nickname: '',
      fouls: 0,
      role: RoleEnum.Civilian,
      status: StatusEnum.Alive,
      elimination_reason: null,
      show_role: false,
    } as Player)),
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

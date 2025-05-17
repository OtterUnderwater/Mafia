// Utilities
import { defineStore } from 'pinia'
import { RoleEnum, StatusEnum } from '@/custom_types/enums.ts';
import type { JwtPayload, Player } from '@/custom_types/interfaces.ts';
import router from '@/router';
import { jwtDecode } from 'jwt-decode';

export const useAppStore = defineStore('app', {
  state: () => ({
    gameId: 0 as number,
    isHost: false as boolean,
    access_token: '' as string,
    username: '' as string,
    players: Array.from({ length: 10 }, (_, index) => ({
      id: index + 1,
      nickname: '',
      fouls: 0,
      role: RoleEnum.Civilian,
      status: StatusEnum.Alive,
      elimination_reason: null,
      idPS: 0,
    } as Player)),
  }),
  actions: {
    setAccessToken (access_token: string) {
      this.access_token = access_token;
      const decoded = jwtDecode<JwtPayload>(access_token);
      this.username = decoded.username;
    },
    setGameId (gameId: number) {
      this.gameId = gameId;
    },
    setIsHost (isHost: boolean) {
      this.isHost = isHost;
    },
    setPlayers (players: Player[]) {
      this.players = players;
    },
    navigateTo (activity: string) {
      router.push(activity);
    },
    updatePlayer ({ index, property, value }: { index: number; property: keyof Player; value: any }) {
      if (this.players[index]) {
        this.players[index][property] = value;
      }
    },
    clearPlayers () {
      this.players = [];
    },
  },
})

import { useAppStore } from '@/stores/app';
import { RoleEnum, StatusEnum } from '@/custom_types/enums.ts';

export class WebSocketService {
  constructor () {
    this.socket = null;
    this.store = useAppStore();
  }

  connect () {
    if (!this.store.gameId) {
      console.error('Game ID is not set. Cannot connect to WebSocket.');
      return;
    }
    this.socket = new WebSocket(`ws://127.0.0.1:8000/web_socket/updates_game/${this.store.gameId}`);
    this.socket.onopen = e => {
      console.log('WebSocket connected', e);
    };
    this.socket.onmessage = e => {
      try {
        const message = JSON.parse(e.data);
        if (message.type === 'add') {
          const playersData = message.data;
          const updatedPlayers = playersData.map((player, index) => ({
            id: index + 1,
            nickname: player.nickname,
            fouls: player.fouls || 0,
            role: player.role || RoleEnum.Civilian,
            status: player.status === 'alive' ? StatusEnum.Alive : StatusEnum.Dead,
            elimination_reason: player.elimination_reason,
            show_role: false,
            idPS: player.id,
          }));
          this.store.setPlayers(updatedPlayers);
        }
        if (message.type === 'update') {
          const player = message.data;
          const currentPlayers = [...this.store.players];
          const playerIndex = currentPlayers.findIndex(p => p.idPS === player.id);
          if (playerIndex !== -1) {
            currentPlayers[playerIndex] = {
              ...currentPlayers[playerIndex],
              nickname: player.nickname || currentPlayers[playerIndex].nickname,
              fouls: player.fouls ?? currentPlayers[playerIndex].fouls,
              role: player.role || currentPlayers[playerIndex].role,
              status: player.status === 'alive' ? StatusEnum.Alive : StatusEnum.Dead,
              elimination_reason: player.elimination_reason || currentPlayers[playerIndex].elimination_reason,
              show_role: currentPlayers[playerIndex].show_role,
              idPS: player.id,
            };
            this.store.setPlayers(currentPlayers);
          }
        }
      } catch (error) {
        console.error('Error processing WebSocket message:', error);
      }
    };
    this.socket.onerror = e => {
      console.error('WebSocket error:', e);
    };
    this.socket.onclose = e => {
      console.log('WebSocket connection closed:', e);
    };
  }

  disconnect () {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

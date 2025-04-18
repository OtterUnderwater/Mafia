import axios from 'axios';

export class ApiClient {
  constructor() {
    this.baseUrl = 'http://127.0.0.1:8000';
    this.instance = axios.create({
      baseURL: this.baseUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      },
    });
  }

  async getPlayers() {
    try {
      const response = await this.instance.get('/players');
      return response.data;
    } catch (error) {
      console.error('Error fetching players:', error);
      throw error;
    }
  }

  async postGame() {
    const requestBody = {
      id_master: 1
    };

    try {
      const response = await this.instance.post('/games/game', requestBody);
      return response.data;
    } catch (error) {
      console.error('Error posting game:', error);
      throw error;
    }
  }

  async postPlayerStatus(id_player, id_game, role) {
    const requestBody = {
      id_player: id_player,
      id_game: id_game,
      role: role,
    };

    try {
      const response = await this.instance.post('/player_status/add_player_status', requestBody);
      return response.data.id;
    } catch (error) {
      console.error('Error posting player status:', error);
      throw error;
    }
  }

  async updatePlayerStatus(id, fouls, status, elimination_reason) {
    const requestBody = {
      fouls: fouls,
      status: status,
      elimination_reason: elimination_reason
    };
    try {
      const response = await this.instance.patch(`/player_status/${id}`, requestBody);
      return response.data;
    } catch (error) {
      console.error('Error update player status:', error);
      throw error;
    }
  }
}

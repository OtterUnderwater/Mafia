import axios from 'axios';
import { useAppStore } from '@/stores/app';

export class ApiClient {
  constructor () {
    this.baseUrl = 'http://127.0.0.1:8000';
    this.instance = axios.create({
      baseURL: this.baseUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });
  }
  //   fetch('/api/protected', {
  //   headers: {
  //     'Authorization': `Bearer ${accessToken}`
  //   }
  // })
  async postAuthorization (username, password) {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      const response = await this.instance.post('/jwt/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      const { access_token } = response.data;
      const store = useAppStore();
      store.setAccessToken(access_token);
      return response.data;
    } catch (error) {
      alert(`Error authorization user: ${error}`);
      console.error('Error authorization user:', error);
      throw error;
    }
  }

  async updateToken () {
    try {
      const response = await this.instance.post('/jwt/refresh');
      const { access_token } = response.data;
      const store = useAppStore();
      store.setAccessToken(access_token);
      return response.data;
    } catch (error) {
      alert(`Error update tokens: ${error}`);
      console.error('Error update tokens:', error);
      throw error;
    }
  }

  async postRegistration (username, password) {
    try {
      const requestBody = {
        username,
        password,
      };
      const response = await this.instance.post('/players/registration', requestBody);
      return response.data;
    } catch (error) {
      console.error('Error registration user:', error);
      throw error;
    }
  }

  async getPlayers () {
    try {
      const response = await this.instance.get('/players');
      return response.data;
    } catch (error) {
      console.error('Error fetching players:', error);
      throw error;
    }
  }

  async postGame () {
    const requestBody = {
      id_master: 1,
    };

    try {
      const response = await this.instance.post('/games/game', requestBody);
      return response.data;
    } catch (error) {
      console.error('Error posting game:', error);
      throw error;
    }
  }

  async postPlayerStatus (id_player, id_game, role) {
    const requestBody = {
      id_player,
      id_game,
      role,
    };

    try {
      const response = await this.instance.post('/player_status/add_player_status', requestBody);
      return response.data.id;
    } catch (error) {
      console.error('Error posting player status:', error);
      throw error;
    }
  }

  async updatePlayerStatus (id, fouls, status, elimination_reason) {
    const requestBody = {
      fouls,
      status,
      elimination_reason,
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

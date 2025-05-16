import { RoleEnum, StatusEnum } from "@/custom_types/enums.js";
import axios from 'axios';
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';

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
    this.store = useAppStore();
    this.router = useRouter();
    this.setupInterceptors();
  }

  setupInterceptors () {
    this.instance.interceptors.response.use(
      response => response,
      async error => {
        const originalRequest = error.config;
        if (originalRequest._skipRefresh) {
          return Promise.reject(error);
        }
        if (error.response?.status === 401 && !originalRequest._isRetry) {
          originalRequest._isRetry = true;
          try {
            const tokenUpdated = await this.updateToken();
            if (!tokenUpdated) {
              throw new Error('Invalid refresh token');
            }
            return this.instance(originalRequest);
          } catch (refreshError) {
            await this.redirectToLogin();
            return Promise.reject(error);
          }
        }
        return Promise.reject(error);
      }
    );
  }

  async redirectToLogin ()
  {
    this.store.setAccessToken('');
    await this.router.push('/LogIn');
  }

  async updateToken (){
    try {
      const response = await this.instance.post('/jwt/refresh', {},{
        _skipRefresh: true,
      });
      const { access_token } = response.data;
      this.store.setAccessToken(access_token);
      return true;
    } catch (error) {
      this.store.setAccessToken('');
      if (error.response?.status === 401) {
        return false;
      }
      else {
        console.error('Error update token:', error);
        throw error;
      }
    }
  }

  async logout (){
    try {
      const response = await this.instance.post('/logout');
      this.store.setAccessToken('');
      return response.data;
    } catch (error) {
      alert(`Error logout: ${error}`);
      console.error('Error logout:', error);
      throw error;
    }
  }

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
      return true;
    } catch (error) {
      if (error.response?.status === 401) {
        return false;
      }
      console.error('Error authorization user:', error);
      throw error;
    }
  }

  async postRegistration (nickname, password) {
    try {
      const requestBody = {
        nickname,
        password,
      };
      const response = await this.instance.post('/players/registration', requestBody);
      return response.data;
    } catch (error) {
      console.error('Error registration user:', error);
      throw error;
    }
  }

  async postGame () {
    try {
      const response = await this.instance.post('/games/game', {},{
        headers: { 'Authorization': `Bearer ${this.store.access_token}` },
      });
      const { id } = response.data;
      this.store.setGameId(id);
      this.store.clearPlayers();
      return response.data;
    } catch (error) {
      alert(`Error posting game: ${error}`);
      console.error('Error posting game:', error);
      throw error;
    }
  }

  async updateGame ( result ) {
    const requestBody = {
      result,
    };
    try {
      const response = await this.instance.patch(`/games/game/${this.store.gameId}`, requestBody, {
        headers: { 'Authorization': `Bearer ${this.store.access_token}` },
      });
      return response.data.id;
    } catch (error) {
      console.error('Error update game:', error);
      throw error;
    }
  }

  async postPlayerStatus (gameId) {
    try {
      const response = await this.instance.post(`/player_status/add_player_status/${gameId}`, {}, {
        headers: { 'Authorization': `Bearer ${this.store.access_token}` },
      });
      this.store.setGameId(gameId);
      return response.data.id;
    } catch (error) {
      console.error('Error posting player status:', error);
      throw error;
    }
  }

  async getPlayersStatus () {
    try {
      const response = await this.instance.get(`/player_status/all_status/${this.store.gameId}`);
      const data = response.data;
      const updatedPlayers = data.map((player, index) => ({
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
      return data;
    } catch (error) {
      console.error('Error fetching players:', error);
      throw error;
    }
  }

  async updatePlayerStatus (id, role, fouls, status, elimination_reason) {
    const requestBody = Object.fromEntries(
      Object.entries({
        role,
        fouls,
        status,
        elimination_reason,
      }).filter(([_, v]) => v != null)
    );
    try {
      const response = await this.instance.patch(`/player_status/${id}`, requestBody);
      return response.data;
    } catch (error) {
      console.error('Error update player status:', error);
      throw error;
    }
  }
}

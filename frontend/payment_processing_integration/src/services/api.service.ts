import axios, { AxiosInstance, AxiosResponse } from 'axios';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
}

class ApiService {
  private api: AxiosInstance;

  constructor(baseURL: string = 'http://localhost:8080') {
    this.api = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add interceptors
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
  }

  async getAll<T>(endpoint: string): Promise<T[]> {
    const response: AxiosResponse<ApiResponse<T[]>> = await this.api.get(endpoint);
    return response.data.data;
  }

  async getById<T>(endpoint: string, id: string): Promise<T> {
    const response: AxiosResponse<ApiResponse<T>> = await this.api.get(`${endpoint}/${id}`);
    return response.data.data;
  }

  async create<T>(endpoint: string, data: any): Promise<T> {
    const response: AxiosResponse<ApiResponse<T>> = await this.api.post(endpoint, data);
    return response.data.data;
  }

  async update<T>(endpoint: string, id: string, data: any): Promise<T> {
    const response: AxiosResponse<ApiResponse<T>> = await this.api.put(`${endpoint}/${id}`, data);
    return response.data.data;
  }

  async delete(endpoint: string, id: string): Promise<void> {
    await this.api.delete(`${endpoint}/${id}`);
  }
}

export default new ApiService();

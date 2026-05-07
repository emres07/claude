import axios, { AxiosInstance, AxiosError } from 'axios';

interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

interface ApiErrorResponse {
  success: false;
  message: string;
  errors?: Record<string, string[]>;
}

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
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

    this.api.interceptors.response.use(
      (response) => response.data,
      (error: AxiosError<ApiErrorResponse>) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error.response?.data || error);
      }
    );
  }

  public setToken(token: string): void {
    this.token = token;
    localStorage.setItem('token', token);
  }

  public getToken(): string | null {
    return this.token || localStorage.getItem('token');
  }

  public clearToken(): void {
    this.token = null;
    localStorage.removeItem('token');
  }

  public async get<T>(url: string, params?: any): Promise<ApiResponse<T>> {
    return this.api.get<any, ApiResponse<T>>(url, { params });
  }

  public async post<T>(url: string, data?: any): Promise<ApiResponse<T>> {
    return this.api.post<any, ApiResponse<T>>(url, data);
  }

  public async put<T>(url: string, data?: any): Promise<ApiResponse<T>> {
    return this.api.put<any, ApiResponse<T>>(url, data);
  }

  public async delete<T>(url: string): Promise<ApiResponse<T>> {
    return this.api.delete<any, ApiResponse<T>>(url);
  }

  public async patch<T>(url: string, data?: any): Promise<ApiResponse<T>> {
    return this.api.patch<any, ApiResponse<T>>(url, data);
  }
}

export const apiService = new ApiService();
export default apiService;

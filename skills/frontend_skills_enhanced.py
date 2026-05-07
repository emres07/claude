"""
Enhanced Frontend Skills - Reads subtask READMEs and generates detailed implementation code.

Parses subtask specifications from README files and generates production-ready:
- React components with hooks and state management
- API service clients with Axios
- Form components with validation
- Page components with routing
- Type definitions and interfaces
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class EnhancedFrontendSkill:
    """Generates detailed frontend code based on subtask specifications."""

    @staticmethod
    def parse_readme(readme_path: str) -> Dict[str, Any]:
        """Parse README file and extract specifications."""
        if not Path(readme_path).exists():
            return {}

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        spec = {
            "title": EnhancedFrontendSkill._extract_title(content),
            "description": EnhancedFrontendSkill._extract_section(content, "### Description"),
            "apis": EnhancedFrontendSkill._extract_list(content, "### APIs Generated"),
            "components": EnhancedFrontendSkill._extract_list(content, "### Components Generated"),
            "pages": EnhancedFrontendSkill._extract_list(content, "### Pages Generated"),
        }
        return spec

    @staticmethod
    def _extract_title(content: str) -> str:
        """Extract title from README."""
        match = re.search(r"^# (.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_section(content: str, section_header: str) -> str:
        """Extract section content from README."""
        pattern = f"{section_header}\n(.+?)(?=\n###|$)"
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_list(content: str, section_header: str) -> List[str]:
        """Extract list items from README section."""
        section = EnhancedFrontendSkill._extract_section(content, section_header)
        items = re.findall(r"^- (.+)$", section, re.MULTILINE)
        return [item.strip() for item in items]

    @staticmethod
    def generate_login_component_from_spec(spec: Dict[str, Any]) -> str:
        """Generate LoginForm component based on specification."""
        return """'use client';

import React, { useState } from 'react';
import axios from 'axios';

interface LoginFormProps {
  onLoginSuccess?: (response: any) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/api/v1/auth/login', {
        email,
        password,
      });

      if (response.data.success) {
        localStorage.setItem('token', response.data.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.data.user));
        onLoginSuccess?.(response.data.data);
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-form-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Login</h2>

        {error && <div className="error-message">{error}</div>}

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default LoginForm;
"""

    @staticmethod
    def generate_api_service_from_spec(spec: Dict[str, Any]) -> str:
        """Generate API service client based on specification."""
        apis = spec.get("apis", [])

        return """import axios, { AxiosInstance, AxiosError } from 'axios';

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
"""

    @staticmethod
    def generate_user_list_component_from_spec(spec: Dict[str, Any]) -> str:
        """Generate UserList component based on specification."""
        return """'use client';

import React, { useState, useEffect } from 'react';
import apiService from '@/services/api';

interface User {
  id: number;
  name: string;
  email: string;
  phoneNumber?: string;
  active: boolean;
  createdAt: string;
}

const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [size] = useState(20);

  useEffect(() => {
    fetchUsers();
  }, [page]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await apiService.get<any>('/api/v1/users', { page, size });
      setUsers(response.data.content);
      setError('');
    } catch (err: any) {
      setError('Failed to fetch users');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (userId: number) => {
    if (!window.confirm('Are you sure you want to deactivate this user?')) {
      return;
    }

    try {
      await apiService.delete(`/api/v1/users/${userId}`);
      setUsers(users.filter(u => u.id !== userId));
    } catch (err) {
      setError('Failed to delete user');
    }
  };

  if (loading) return <div className="loading">Loading users...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="user-list-container">
      <h2>Users</h2>
      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Status</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.phoneNumber || '-'}</td>
              <td>{user.active ? 'Active' : 'Inactive'}</td>
              <td>{new Date(user.createdAt).toLocaleDateString()}</td>
              <td>
                <button onClick={() => handleDelete(user.id)}>Deactivate</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
        <button onClick={() => setPage(Math.max(0, page - 1))} disabled={page === 0}>
          Previous
        </button>
        <span>Page {page + 1}</span>
        <button onClick={() => setPage(page + 1)}>
          Next
        </button>
      </div>
    </div>
  );
};

export default UserList;
"""

    @staticmethod
    def generate_dashboard_page_from_spec(spec: Dict[str, Any]) -> str:
        """Generate Dashboard page based on specification."""
        return """'use client';

import React, { useState, useEffect } from 'react';
import apiService from '@/services/api';

interface DashboardStats {
  totalUsers: number;
  activeUsers: number;
  totalSessions: number;
  recentAuditLogs: any[];
}

const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const response = await apiService.get<DashboardStats>('/api/v1/dashboard/stats');
      setStats(response.data);
      setError('');
    } catch (err: any) {
      setError('Failed to load dashboard statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!stats) return <div>No data available</div>;

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Users</h3>
          <p className="stat-value">{stats.totalUsers}</p>
        </div>

        <div className="stat-card">
          <h3>Active Users</h3>
          <p className="stat-value">{stats.activeUsers}</p>
        </div>

        <div className="stat-card">
          <h3>Total Sessions</h3>
          <p className="stat-value">{stats.totalSessions}</p>
        </div>
      </div>

      <div className="recent-activity">
        <h2>Recent Activity</h2>
        <table className="audit-table">
          <thead>
            <tr>
              <th>Action</th>
              <th>Entity</th>
              <th>User</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {stats.recentAuditLogs.map((log: any, index: number) => (
              <tr key={index}>
                <td>{log.action}</td>
                <td>{log.entity}</td>
                <td>{log.userId}</td>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DashboardPage;
"""

    @staticmethod
    def generate_user_registration_page_from_spec(spec: Dict[str, Any]) -> str:
        """Generate User Registration page based on specification."""
        return """'use client';

import React, { useState } from 'react';
import apiService from '@/services/api';
import { useRouter } from 'next/navigation';

interface RegistrationForm {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  phoneNumber?: string;
}

const RegistrationPage: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState<RegistrationForm>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phoneNumber: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const response = await apiService.post('/api/v1/users/register', {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        phoneNumber: formData.phoneNumber,
      });

      if (response.success) {
        localStorage.setItem('token', response.data.token);
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="registration-container">
      <div className="registration-form-wrapper">
        <h1>Create Account</h1>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="registration-form">
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              id="name"
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="phoneNumber">Phone (Optional)</label>
            <input
              id="phoneNumber"
              type="tel"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <p className="login-link">
          Already have an account? <a href="/login">Login here</a>
        </p>
      </div>
    </div>
  );
};

export default RegistrationPage;
"""

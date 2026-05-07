# Frontend Code Templates - Jinja2 Format

## Package JSON Template

<!-- package_json -->
```json
{
  "name": "{{ project_name | lower | replace(' ', '-') }}",
  "version": "{{ version | default('1.0.0') }}",
  "description": "{{ project_name }} - Next.js Frontend Application",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "next": "^14.1.0",
    "typescript": "^5.3.3",
    {% if dependencies -%}
    {% for dep, version in dependencies.items() -%}
    "{{ dep }}": "{{ version }}",
    {% endfor %}
    {% endif -%}
    "tailwindcss": "^3.4.1",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16"
  },
  "devDependencies": {
    "@types/node": "^20.10.6",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "@types/jest": "^29.5.11",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0"
  }
}
```
<!-- /package_json -->

## Component Template

<!-- component_template -->
```typescript
import React, { useState } from 'react';
{% if imports %}
{% for imp in imports -%}
import {{ imp }};
{% endfor %}
{% endif -%}

interface {{ component_name }}Props {
  {% if props -%}
  {% for prop in props -%}
  {{ prop.name }}: {{ prop.type }};
  {% endfor %}
  {% else -%}
  // TODO: Add component props
  {% endif -%}
}

const {{ component_name }}: React.FC<{{ component_name }}Props> = (props) => {
  {% if state_vars -%}
  {% for var in state_vars -%}
  const [{{ var.name }}, set{{ var.name | capitalize }}] = useState<{{ var.type }}>({{ var.default }});
  {% endfor %}
  {% else -%}
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [data, setData] = useState<any>(null);
  {% endif -%}

  React.useEffect(() => {
    // TODO: Fetch data on mount
  }, []);

  {% if error_handling -%}
  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  {% endif -%}

  return (
    <div className="{{ component_name_kebab }}">
      <h2>{{ component_name }}</h2>
      {/* TODO: Add component content */}
    </div>
  );
};

export default {{ component_name }};
```
<!-- /component_template -->

## Page Template

<!-- page_template -->
```typescript
import React from 'react';
{% if use_query -%}
import { useQuery } from '@tanstack/react-query';
{% endif -%}
{% if imports %}
{% for imp in imports -%}
import {{ imp }};
{% endfor %}
{% endif -%}

const {{ page_name }}Page = () => {
  {% if use_query -%}
  const { data, isLoading, error } = useQuery({
    queryKey: ['{{ page_name_lower }}'],
    queryFn: async () => {
      // TODO: Fetch data from API
      return null;
    },
  });
  {% else -%}
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  {% endif -%}

  {% if use_query -%}
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading {{ page_name_lower }}</div>;
  {% else -%}
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error</div>;
  {% endif -%}

  return (
    <div className="{{ page_name_lower }}-page">
      <h1>{{ page_name }}</h1>
      {/* TODO: Add page content */}
    </div>
  );
};

export default {{ page_name }}Page;
```
<!-- /page_template -->

## API Service Template

<!-- api_service -->
```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api/v1';

class ApiService {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.axiosInstance.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async get<T>(url: string) {
    try {
      const response = await this.axiosInstance.get<T>(url);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async post<T>(url: string, data: unknown) {
    try {
      const response = await this.axiosInstance.post<T>(url, data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async put<T>(url: string, data: unknown) {
    try {
      const response = await this.axiosInstance.put<T>(url, data);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async delete<T>(url: string) {
    try {
      const response = await this.axiosInstance.delete<T>(url);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  private handleError(error: unknown): Error {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.message || error.message;
      return new Error(message);
    }
    return new Error('An unknown error occurred');
  }
}

export const apiService = new ApiService();
```
<!-- /api_service -->

## TSConfig Template

<!-- tsconfig -->
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "moduleResolution": "bundler",
    "types": ["jest", "@testing-library/jest-dom"],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```
<!-- /tsconfig -->

## ESLint Config Template

<!-- eslint_config -->
```json
{
  "extends": "next/core-web-vitals",
  "rules": {
    "react/display-name": "off",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn"
  }
}
```
<!-- /eslint_config -->

## Next Config Template

<!-- next_config -->
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api/v1',
  },
}

module.exports = nextConfig
```
<!-- /next_config -->

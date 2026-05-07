"""Frontend Skills - React, Next.js, Vite, Axios, TypeScript, Design patterns."""


class FrontendSkill:
    """Skills for frontend development with React, Next.js, Vite, TypeScript."""

    name = "frontend"
    description = "Frontend with React, Vite, Next.js, Axios, TypeScript & Design"

    FRAMEWORKS = {
        "nextjs": "Next.js (React framework with SSR)",
        "react": "React with Vite",
        "vite": "Vite build tool",
    }

    TOOLS = ["Axios", "TypeScript", "TailwindCSS", "Material-UI", "React Query"]

    @staticmethod
    def generate_package_json(project_name: str, version: str = "1.0.0") -> str:
        """Generate package.json for Next.js/React project."""
        return f"""{{
  "name": "{project_name.lower().replace(' ', '-')}",
  "version": "{version}",
  "description": "Frontend application with Next.js, React, Vite, TypeScript",
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx",
    "type-check": "tsc --noEmit",
    "format": "prettier --write ."
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "^14.0.0",
    "axios": "^1.6.0",
    "typescript": "^5.0.0",
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0"
  }},
  "devDependencies": {{
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0"
  }}
}}
"""

    @staticmethod
    def generate_tsconfig() -> str:
        """Generate TypeScript configuration."""
        return """{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
"""

    @staticmethod
    def generate_component_template(component_name: str) -> str:
        """Generate React component template with TypeScript."""
        camel_case = ''.join(word.title() for word in component_name.split('_'))
        return f"""'use client';

import React, {{ useState, useEffect }} from 'react';
import axios from 'axios';

interface {camel_case}Props {{
  // Define props here
}}

interface {camel_case}State {{
  // Define state here
}}

export const {camel_case}: React.FC<{camel_case}Props> = (props) => {{
  const [state, setState] = useState<{camel_case}State>({{
    // Initialize state
  }});

  useEffect(() => {{
    // Initialize component
  }}, []);

  const handleLoad = async () => {{
    try {{
      const response = await axios.get('/api/data');
      // Handle response
    }} catch (error) {{
      console.error('Error:', error);
    }}
  }};

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">{camel_case}</h1>
      {/* Component JSX */}}
    </div>
  );
}};

export default {camel_case};
"""

    @staticmethod
    def generate_api_service(service_name: str, base_url: str = "http://localhost:8080") -> str:
        """Generate API service with Axios and TypeScript."""
        service_class = ''.join(word.title() for word in service_name.split('_')) + 'Service'
        return f"""import axios, {{ AxiosInstance, AxiosResponse }} from 'axios';

interface ApiResponse<T> {{
  success: boolean;
  data: T;
  message: string;
}}

class {service_class} {{
  private api: AxiosInstance;

  constructor(baseURL: string = '{base_url}') {{
    this.api = axios.create({{
      baseURL,
      headers: {{
        'Content-Type': 'application/json',
      }},
    }});

    // Add interceptors
    this.api.interceptors.request.use(
      (config) => {{
        const token = localStorage.getItem('token');
        if (token) {{
          config.headers.Authorization = `Bearer ${{token}}`;
        }}
        return config;
      }},
      (error) => Promise.reject(error)
    );
  }}

  async getAll<T>(endpoint: string): Promise<T[]> {{
    const response: AxiosResponse<ApiResponse<T[]>> = await this.api.get(endpoint);
    return response.data.data;
  }}

  async getById<T>(endpoint: string, id: string): Promise<T> {{
    const response: AxiosResponse<ApiResponse<T>> = await this.api.get(`${{endpoint}}/${{id}}`);
    return response.data.data;
  }}

  async create<T>(endpoint: string, data: any): Promise<T> {{
    const response: AxiosResponse<ApiResponse<T>> = await this.api.post(endpoint, data);
    return response.data.data;
  }}

  async update<T>(endpoint: string, id: string, data: any): Promise<T> {{
    const response: AxiosResponse<ApiResponse<T>> = await this.api.put(`${{endpoint}}/${{id}}`, data);
    return response.data.data;
  }}

  async delete(endpoint: string, id: string): Promise<void> {{
    await this.api.delete(`${{endpoint}}/${{id}}`);
  }}
}}

export default new {service_class}();
"""

    @staticmethod
    def generate_page_template(page_name: str) -> str:
        """Generate Next.js page with TypeScript."""
        pascal_case = ''.join(word.title() for word in page_name.replace('-', '_').split('_'))
        return f"""'use client';

import React, {{ useState, useEffect }} from 'react';
import Link from 'next/link';

interface {pascal_case}Props {{}}

const {pascal_case}: React.FC<{pascal_case}Props> = () => {{
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    setLoading(false);
  }}, []);

  if (loading) {{
    return <div>Loading...</div>;
  }}

  return (
    <div className="min-h-screen bg-white">
      <header className="bg-gray-100 p-4">
        <h1 className="text-3xl font-bold">{pascal_case}</h1>
      </header>
      <main className="container mx-auto p-4">
        {/* Page content */}}
      </main>
    </div>
  );
}};

export default {pascal_case};
"""

    @staticmethod
    def get_design_patterns() -> dict:
        """Get recommended design patterns for frontend."""
        return {
            "component_structure": [
                "Atomic Design (atoms, molecules, organisms)",
                "Container/Presentational Pattern",
                "Compound Components",
            ],
            "state_management": [
                "React Context API",
                "Redux Toolkit",
                "Zustand",
                "Jotai",
            ],
            "styling": [
                "TailwindCSS",
                "CSS Modules",
                "Styled Components",
                "Emotion",
            ],
            "data_fetching": [
                "React Query (TanStack Query)",
                "SWR",
                "Axios with custom hooks",
            ],
        }

    @staticmethod
    def generate_eslint_config() -> str:
        """Generate ESLint configuration."""
        return """{
  "extends": [
    "next/core-web-vitals",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }]
  }
}
"""

    @staticmethod
    def generate_setup_script() -> str:
        """Generate setup script for Node.js frontend."""
        return """#!/bin/bash

echo "🎨 Frontend Setup Script"
echo "======================="

# Check Node.js version
NODE_VERSION=$(node -v)
echo "✓ Node.js version: $NODE_VERSION"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Create .env.local
echo ""
echo "🔐 Creating .env.local..."
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8080/api
NEXT_PUBLIC_APP_NAME=My App
EOF

echo "✓ .env.local created"

# Create necessary directories
echo ""
echo "📁 Creating directory structure..."
mkdir -p src/components
mkdir -p src/pages
mkdir -p src/services
mkdir -p src/hooks
mkdir -p src/types
mkdir -p src/utils
mkdir -p src/styles

echo "✓ Directories created"

# Initialize git
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial frontend setup"
fi

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "Next steps:"
echo "  npm run dev      - Start development server"
echo "  npm run build    - Build for production"
echo "  npm run lint     - Run linter"
echo "  npm run format   - Format code"
"""

# Code Generation Guide

This agent team automatically generates production-ready code for full-stack applications. Each agent specializes in generating code for their domain.

## 📂 Folder Structure

```
project_root/
├── backend/                          # 🔧 Java Spring Boot Code
│   └── [project_name]/
│       ├── pom.xml
│       ├── src/main/java/com/example/
│       │   ├── entity/              # JPA Entities
│       │   ├── repository/          # Spring Data JPA Repositories
│       │   ├── service/             # Business Logic (Services)
│       │   └── controller/          # REST Controllers
│       ├── src/main/resources/
│       │   └── application.yml      # Configuration
│       └── setup.sh                 # Maven setup script
│
├── frontend/                         # 🎨 React/Next.js TypeScript Code
│   └── [project_name]/
│       ├── package.json             # Node.js dependencies
│       ├── tsconfig.json            # TypeScript config
│       ├── .eslintrc.json           # Linting rules
│       ├── src/
│       │   ├── components/          # React components
│       │   ├── pages/               # Next.js pages
│       │   ├── services/            # API services (Axios)
│       │   ├── hooks/               # Custom React hooks
│       │   ├── types/               # TypeScript types
│       │   ├── utils/               # Utility functions
│       │   └── styles/              # CSS/Styling
│       ├── public/                  # Static files
│       └── setup.sh                 # Node.js setup script
│
└── dbadmin/                          # 💾 Oracle/PL-SQL Code
    └── [project_name]/
        ├── 001_schema_creation.sql  # Schema & user setup
        ├── tables/
        │   ├── 02_user_table.sql
        │   ├── 02_transaction_table.sql
        │   └── 02_audit_table.sql
        ├── procedures/
        │   ├── 03_user_crud.sql     # CRUD procedures
        │   ├── 03_transaction_crud.sql
        │   └── 03_audit_crud.sql
        ├── packages/                # PL/SQL packages
        ├── migrations/              # Migration scripts
        ├── setup.sh                 # Oracle setup script
        └── README.md                # Database documentation
```

## 🚀 Quick Start

### 1. Interactive Project Input (Easiest)

```bash
python main.py --interactive
```

You'll be prompted:
```
📝 Project name: My E-Commerce App
📝 Project description: Complete e-commerce platform
⭐ Select priority: 3 (High)
🔧 Select domains: all (backend, frontend, database)
```

The agents will then generate:
- ✅ Full Spring Boot backend structure
- ✅ Complete React/Next.js frontend
- ✅ Oracle database schema with CRUD procedures

### 2. Sample Projects

```bash
python main.py --sample
```

Runs with pre-configured sample projects that showcase all features.

### 3. CLI Arguments

```bash
python main.py --add-project "My Project" \
  --description "Project description" \
  --priority high \
  --domains backend,frontend,database
```

### 4. From File

```bash
python main.py --projects projects.json
```

## 🛠️ Generated Code Details

### Backend Agent - Spring Boot Java

**Generated Files:**
- `pom.xml` - Maven configuration with Spring Boot, Hibernate, Lombok
- `Entity.java` - JPA entities with Hibernate annotations
- `Repository.java` - Spring Data JPA repositories
- `Service.java` - Business logic layer
- `Controller.java` - REST API endpoints
- `application.yml` - Database and app configuration

**Example Entity:**
```java
@Entity
@Table(name = "user")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
}
```

**Example Controller:**
```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping
    public ResponseEntity<List<User>> getAll() {
        return ResponseEntity.ok(userService.getAll());
    }

    @PostMapping
    public ResponseEntity<User> create(@RequestBody User user) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(userService.create(user));
    }
}
```

**Setup:**
```bash
cd backend/[project_name]
./setup.sh
mvn clean compile
mvn spring-boot:run
```

### Frontend Agent - React/Next.js TypeScript

**Generated Files:**
- `package.json` - Node.js dependencies (React, Next.js, Axios, TypeScript)
- `tsconfig.json` - TypeScript configuration
- `.eslintrc.json` - ESLint rules
- Components with TypeScript
- API services with Axios
- Page templates

**Example Component:**
```typescript
'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface ButtonProps {
  // Define props here
}

export const Button: React.FC<ButtonProps> = (props) => {
  const [state, setState] = useState<ButtonState>({
    // Initialize state
  });

  useEffect(() => {
    // Initialize component
  }, []);

  const handleClick = async () => {
    try {
      const response = await axios.get('/api/v1/data');
      // Handle response
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">Button Component</h1>
    </div>
  );
};
```

**Example API Service:**
```typescript
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
      headers: { 'Content-Type': 'application/json' },
    });

    // Add auth interceptor
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async getAll<T>(endpoint: string): Promise<T[]> {
    const response: AxiosResponse<ApiResponse<T[]>> = 
      await this.api.get(endpoint);
    return response.data.data;
  }

  async create<T>(endpoint: string, data: any): Promise<T> {
    const response: AxiosResponse<ApiResponse<T>> = 
      await this.api.post(endpoint, data);
    return response.data.data;
  }
}

export default new ApiService();
```

**Setup:**
```bash
cd frontend/[project_name]
./setup.sh
npm install
npm run dev    # Development server
npm run build  # Production build
```

### Database Agent - Oracle/PL-SQL

**Generated Files:**
- `001_schema_creation.sql` - Schema, tablespace, user creation
- `02_*.sql` - Table definitions with indexes and triggers
- `03_*_crud.sql` - CRUD stored procedures
- Packages for PL/SQL operations
- Migration scripts

**Example Table Creation:**
```sql
CREATE TABLE user (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500),
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE INDEX idx_user_created_at ON user(created_at);
CREATE INDEX idx_user_updated_at ON user(updated_at);
```

**Example CRUD Procedure:**
```sql
CREATE OR REPLACE PROCEDURE sp_user_insert (
  p_name IN VARCHAR2,
  p_description IN VARCHAR2,
  p_id OUT NUMBER
)
IS
BEGIN
  INSERT INTO user (id, name, description, status, created_at, updated_at)
  VALUES (user_seq.NEXTVAL, p_name, p_description, 'ACTIVE', 
          SYSTIMESTAMP, SYSTIMESTAMP)
  RETURNING id INTO p_id;
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END sp_user_insert;
/
```

**Setup:**
```bash
cd dbadmin/[project_name]
./setup.sh
sqlplus /nolog
@001_schema_creation.sql
@tables/02_user_table.sql
@procedures/03_user_crud.sql
```

## 📋 Skills Used by Each Agent

### Backend Agent Skills
- ✅ Java programming
- ✅ Spring Boot framework
- ✅ Hibernate ORM
- ✅ Maven build system
- ✅ Clean code principles
- ✅ REST API design
- ✅ Repository pattern
- ✅ Service layer design

### Frontend Agent Skills
- ✅ React library
- ✅ Next.js framework
- ✅ Vite build tool
- ✅ TypeScript
- ✅ Axios HTTP client
- ✅ Component architecture
- ✅ Responsive design
- ✅ State management
- ✅ Design patterns

### Database Agent Skills
- ✅ Oracle Database
- ✅ PL/SQL
- ✅ Schema design
- ✅ Table design
- ✅ CRUD procedures
- ✅ Triggers and indexes
- ✅ Migration scripts
- ✅ Performance optimization

## 🔄 Full Example Workflow

### Step 1: Interactive Project Input

```bash
python main.py --interactive

📝 Project name: Social Media App
📝 Project description: A complete social media platform with user authentication, 
                       posts, comments, and real-time notifications
⭐ Select priority: 3 (High)
🔧 Select domains: all
```

### Step 2: Agents Process Project

```
📋 Task Creator Agent is working...
  ✓ Main task created: Social Media App

🔍 Database Agent is clarifying requirements...
  ✓ Task requirements clarified

🔧 Backend Agent is creating Java/Spring Boot code...
  ✓ Backend API Implementation - Social Media App
  ✓ Database Schema & Hibernate Mapping - Social Media App
  ✓ Generated: pom.xml, entities, repositories, services, controllers

🎨 Frontend Agent is creating React/Next.js & TypeScript code...
  ✓ UI Components - Social Media App
  ✓ Pages - Social Media App
  ✓ Generated: package.json, tsconfig, components, services, pages

💾 Database Agent is creating Oracle/PL-SQL code...
  ✓ Database Schema - Social Media App
  ✓ Query Optimization - Social Media App
  ✓ Generated: schema, tables, CRUD procedures, migrations
```

### Step 3: Generated Folder Structure

```
backend/social_media_app/
├── pom.xml
├── src/main/java/com/example/socialmediaapp/
│   ├── entity/User.java
│   ├── entity/Post.java
│   ├── repository/UserRepository.java
│   ├── service/UserService.java
│   └── controller/UserController.java
└── src/main/resources/application.yml

frontend/social_media_app/
├── package.json
├── tsconfig.json
├── src/components/Post.tsx
├── src/pages/Feed.tsx
├── src/services/api.service.ts
└── setup.sh

dbadmin/social_media_app/
├── 001_schema_creation.sql
├── tables/02_user_table.sql
├── tables/02_post_table.sql
├── procedures/03_user_crud.sql
└── procedures/03_post_crud.sql
```

### Step 4: Setup Each Component

**Backend:**
```bash
cd backend/social_media_app
./setup.sh
mvn spring-boot:run
# Server starts on http://localhost:8080
```

**Frontend:**
```bash
cd frontend/social_media_app
./setup.sh
npm run dev
# Dev server on http://localhost:3000
```

**Database:**
```bash
cd dbadmin/social_media_app
./setup.sh
sqlplus /nolog
@001_schema_creation.sql
@tables/02_user_table.sql
@procedures/03_user_crud.sql
```

### Step 5: Push to GitHub

```bash
git add backend/ frontend/ dbadmin/
git commit -m "Auto-generated full-stack code for Social Media App"
git push origin main
```

## 🎯 Best Practices

### Backend (Java/Spring Boot)
- Use Entity-Repository-Service pattern
- Keep controllers thin
- Use Lombok for less boilerplate
- Hibernate manages database operations
- Clean code: SRP, DRY, KISS

### Frontend (React/Next.js)
- Use TypeScript for type safety
- Component-based architecture
- Axios for API calls
- Responsive design with Tailwind
- Proper error handling

### Database (Oracle/PL-SQL)
- Proper schema design
- Automated CRUD procedures
- Audit triggers
- Performance indexes
- Parameterized queries

## 📝 Notes

- Generated code is production-ready templates
- Customize for your specific needs
- Commit generated code to version control
- Each agent generates in its respective folder
- Scripts handle setup automatically
- All agents work independently but coordinate

## 🚀 Next Steps

1. **Generate code**: `python main.py --interactive`
2. **Review generated files** in backend/, frontend/, dbadmin/
3. **Customize** for your specific requirements
4. **Setup** each component with setup.sh
5. **Develop** on top of generated templates
6. **Commit** to GitHub

Happy coding! 🎉

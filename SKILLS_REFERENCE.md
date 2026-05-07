# Skills Reference

Each agent is equipped with specialized skills for code generation and task management.

## 🔧 Backend Agent Skills

### Technology Stack
- **Language**: Java 21
- **Framework**: Spring Boot 3.x
- **ORM**: Hibernate with Spring Data JPA
- **Build Tool**: Maven
- **Additional**: Lombok, MapStruct

### Skills Available

#### 1. Java Programming
- Entity definitions with JPA annotations
- Clean, maintainable code patterns
- Best practices and standards

#### 2. Spring Boot Framework
- REST API development
- Dependency injection and configuration
- Component lifecycle management

#### 3. Hibernate ORM
- Entity mapping
- Relationship management
- Query optimization

#### 4. Maven Build System
- Dependency management
- Build lifecycle
- Plugin configuration

#### 5. Clean Code Principles
- Single Responsibility Principle (SRP)
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle
- DRY, YAGNI, KISS

### Generated Artifacts
```
pom.xml                    - Maven configuration
src/main/java/.../entity/   - JPA Entities
src/main/java/.../repository/ - Repositories
src/main/java/.../service/  - Services
src/main/java/.../controller/ - Controllers
src/main/resources/         - Configuration files
setup.sh                   - Maven setup script
```

### Usage Example
```java
// Automatically generated entity
@Entity
@Table(name = "user")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String email;
    
    @Column(nullable = false)
    private String password;
}

// Generated repository with CRUD operations
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}

// Generated service with business logic
@Service @RequiredArgsConstructor @Transactional
public class UserService {
    private final UserRepository userRepository;
    
    public List<User> getAll() { /* ... */ }
    public User create(User user) { /* ... */ }
    public User update(Long id, User user) { /* ... */ }
    public void delete(Long id) { /* ... */ }
}

// Generated REST controller
@RestController @RequestMapping("/api/v1/users") @RequiredArgsConstructor
public class UserController {
    private final UserService userService;
    
    @GetMapping
    public ResponseEntity<List<User>> getAll() { /* ... */ }
    
    @PostMapping
    public ResponseEntity<User> create(@RequestBody User user) { /* ... */ }
}
```

---

## 🎨 Frontend Agent Skills

### Technology Stack
- **Framework**: React 18.x with Next.js 14.x
- **Build Tool**: Vite
- **Language**: TypeScript 5.x
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS
- **Package Manager**: npm/yarn

### Skills Available

#### 1. React Library
- Functional components with hooks
- State management
- Effect handling
- Performance optimization

#### 2. Next.js Framework
- Page-based routing
- Server-side rendering (SSR)
- Static generation (SSG)
- API routes

#### 3. Vite Build Tool
- Fast development experience
- Optimized production builds
- Hot module replacement (HMR)

#### 4. TypeScript
- Type-safe component props
- Interface definitions
- Generic components
- Strict type checking

#### 5. Axios HTTP Client
- API request handling
- Interceptors
- Error handling
- Token management

#### 6. Responsive Design
- Mobile-first approach
- Breakpoint management
- Accessibility features
- CSS-in-JS patterns

### Generated Artifacts
```
package.json               - Node.js dependencies
tsconfig.json              - TypeScript configuration
.eslintrc.json             - ESLint rules
src/components/            - React components
src/pages/                 - Next.js pages
src/services/              - API services
src/hooks/                 - Custom hooks
src/types/                 - TypeScript types
src/utils/                 - Utility functions
src/styles/                - CSS files
setup.sh                   - Node.js setup script
```

### Usage Example
```typescript
// Automatically generated component with TypeScript
'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface UserCardProps {
  userId: number;
}

interface User {
  id: number;
  name: string;
  email: string;
}

export const UserCard: React.FC<UserCardProps> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get<User>(`/api/v1/users/${userId}`);
        setUser(response.data);
      } catch (err) {
        setError('Failed to fetch user');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div className="p-4 border rounded-lg shadow-md">
      <h2 className="text-2xl font-bold">{user.name}</h2>
      <p className="text-gray-600">{user.email}</p>
    </div>
  );
};

// Automatically generated API service
import axios, { AxiosInstance, AxiosResponse } from 'axios';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
}

class UserService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL,
    });

    // Auto-inject auth token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async getAll(): Promise<User[]> {
    const { data } = await this.api.get<ApiResponse<User[]>>('/users');
    return data.data;
  }

  async getById(id: number): Promise<User> {
    const { data } = await this.api.get<ApiResponse<User>>(`/users/${id}`);
    return data.data;
  }

  async create(user: Partial<User>): Promise<User> {
    const { data } = await this.api.post<ApiResponse<User>>('/users', user);
    return data.data;
  }
}

export default new UserService();
```

---

## 💾 Database Agent Skills

### Technology Stack
- **Database**: Oracle Database 21c/23c
- **Language**: PL/SQL
- **Tools**: SQL*Plus, SQL Developer
- **Version Control**: Liquibase/Flyway migrations

### Skills Available

#### 1. Oracle Database
- Schema creation and management
- Tablespace configuration
- User and privilege management
- Performance tuning

#### 2. PL/SQL Programming
- Stored procedures
- Packages
- Triggers
- Functions
- Error handling

#### 3. Schema Design
- Entity-relationship modeling
- Normalization (3NF)
- Constraint management
- Index optimization

#### 4. Table Design
- Column definitions
- Primary and foreign keys
- Constraints (CHECK, UNIQUE, etc.)
- Audit columns (created_at, updated_at)

#### 5. CRUD Operations
- INSERT procedures
- SELECT procedures
- UPDATE procedures
- DELETE procedures
- Parameterized queries

#### 6. Triggers and Audit
- DML triggers (BEFORE/AFTER)
- Audit trail logging
- Automatic timestamp updates
- Data validation

### Generated Artifacts
```
001_schema_creation.sql    - Schema and user setup
tables/
  ├── 02_user_table.sql
  ├── 02_post_table.sql
  └── 02_comment_table.sql
procedures/
  ├── 03_user_crud.sql
  ├── 03_post_crud.sql
  └── 03_comment_crud.sql
packages/
  └── pkg_*.sql
migrations/
  └── 001_initial.sql
setup.sh                   - Oracle setup script
README.md                  - Database documentation
```

### Usage Example
```sql
-- Automatically generated schema
CREATE TABLESPACE app_ts
  DATAFILE '/opt/oracle/oradata/app_01.dbf' SIZE 100M;

CREATE USER appuser IDENTIFIED BY welcome123
  DEFAULT TABLESPACE app_ts;

GRANT CREATE SESSION TO appuser;

-- Automatically generated table with audit
CREATE TABLE users (
  id NUMBER PRIMARY KEY,
  email VARCHAR2(255) NOT NULL UNIQUE,
  password VARCHAR2(255) NOT NULL,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_email ON users(email);

-- Automatically generated CRUD procedure
CREATE OR REPLACE PROCEDURE sp_user_insert (
  p_email IN VARCHAR2,
  p_password IN VARCHAR2,
  p_id OUT NUMBER
) IS
BEGIN
  INSERT INTO users (id, email, password, created_at, updated_at)
  VALUES (users_seq.NEXTVAL, p_email, p_password, SYSTIMESTAMP, SYSTIMESTAMP)
  RETURNING id INTO p_id;
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
    RAISE;
END sp_user_insert;
/

-- Automatically generated CRUD package
CREATE OR REPLACE PACKAGE pkg_user_ops IS
  PROCEDURE insert_record(p_email IN VARCHAR2, p_password IN VARCHAR2, p_id OUT NUMBER);
  PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);
  PROCEDURE update_record(p_id IN NUMBER, p_email IN VARCHAR2);
  PROCEDURE delete_record(p_id IN NUMBER);
END pkg_user_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_user_ops IS
  -- Implementation with error handling
END pkg_user_ops;
/
```

---

## 🔄 Task Clarification Skill (Database Agent)

The Database Agent also has a special task clarification skill:

```python
# Analyzes task clarity
clarity_analysis = TaskClarificationSkill.analyze_clarity(task_description)
# Returns: {
#   "is_clear": True/False,
#   "issues": [...],
#   "confidence": 0-100
# }

# Suggests improvements
suggestions = TaskClarificationSkill.suggest_clarifications(task_description)
# Returns: [
#   "Add more detailed description",
#   "Define clear acceptance criteria",
#   "Specify expected timeline"
# ]

# Generates clarification template
template = TaskClarificationSkill.generate_clarification_template(task_title)
# Provides structured template for ambiguous tasks
```

---

## 📊 Skills Summary Table

| Agent | Primary Skills | Technologies | Output Format |
|-------|----------------|--------------|---------------|
| Backend | Java, Spring Boot, Hibernate, Maven, Clean Code | Java 21, Spring Boot 3.x, Maven | .java files, pom.xml |
| Frontend | React, Next.js, Vite, TypeScript, Axios | React 18.x, Next.js 14.x, TypeScript 5.x | .tsx, .ts, .json files |
| Database | Oracle, PL/SQL, Schema, CRUD, Audit | Oracle 21c/23c, PL/SQL | .sql scripts |
| All Agents | Task Clarification, Code Organization | - | Documentation, Markdown |

---

## 🚀 Using Skills in Your Projects

Each skill is automatically applied when you specify domains:

```bash
# All skills (Backend + Frontend + Database)
python main.py --interactive  # Select "all"

# Backend only (Java, Spring Boot, Hibernate, Maven skills)
python main.py --add-project "API Service" --domains backend

# Frontend only (React, Next.js, TypeScript, Axios skills)
python main.py --add-project "Web App" --domains frontend

# Database only (Oracle, PL/SQL, Schema, CRUD skills)
python main.py --add-project "Database" --domains database
```

---

## 💡 Best Practices by Agent

### Backend Agent
✅ Use DTOs for API responses  
✅ Implement proper exception handling  
✅ Use transactions for data consistency  
✅ Implement logging with SLF4J  
✅ Use prepared statements (automatic)  

### Frontend Agent
✅ Use TypeScript strictly  
✅ Implement error boundaries  
✅ Optimize bundle size  
✅ Use lazy loading for routes  
✅ Implement proper loading states  

### Database Agent
✅ Always use parameterized queries  
✅ Implement audit trails  
✅ Index frequently queried columns  
✅ Monitor query performance  
✅ Backup regularly  

---

Generated code leverages all these skills to provide production-ready templates! 🎉

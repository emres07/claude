# How to Run Agents - Complete Code Generation Guide

This guide explains how to run the multi-agent team to **generate production-ready code** for full-stack applications.

## Prerequisites

1. **Python 3.8+** installed
2. **Virtual environment** created and activated
3. **Dependencies installed** via `pip install -r requirements.txt`
4. **.env file** with `ANTHROPIC_API_KEY`

## Quick Setup

```bash
# Navigate to project folder
cd "c:\DEV\CLAUDE_PROJECTS\New folder"

# Create virtual environment (if not already done)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo ANTHROPIC_API_KEY=your_api_key_here > .env
```

## Running Agents - 4 Methods

### Option 1: Interactive Mode (Recommended) ⭐⭐⭐

```bash
python main.py --interactive
```

**Most user-friendly way to generate code:**

```
🚀 AGENT TEAM PROJECT INPUT
======================================================================

📝 Project name: E-Commerce Platform
📝 Project description: Complete e-commerce with payment processing
⭐ Select priority: 3 (High)
🔧 Select domains: all

✅ Project configured:
   Name: E-Commerce Platform
   Description: Complete e-commerce with payment processing
   Priority: HIGH
   Domains: backend, frontend, database

🚀 Agents will generate code in:
   📁 backend/   - Spring Boot Java code
   📁 frontend/  - React/Next.js TypeScript code
   📁 dbadmin/   - Oracle/PL-SQL scripts
```

**Generated folders:**
- `backend/e_commerce_platform/` - Complete Spring Boot project
- `frontend/e_commerce_platform/` - Complete Next.js project
- `dbadmin/e_commerce_platform/` - Oracle schema & procedures

### Option 2: Use Sample Projects

```bash
python main.py --sample
```

**What it does:**
- Loads 2 pre-built sample projects
- **Generates complete code** in backend/, frontend/, dbadmin/
- Creates task descriptions
- Shows real-time progress

**Output example:**
```
✓ Using sample projects

🚀 STARTING AGENT TEAM PROCESSING FOR 2 PROJECT(S)

Processing Project: User Authentication System
Priority: HIGH

📋 Task Creator Agent is working...
  ✓ Main task created: User Authentication System

🔍 Database Agent is clarifying requirements...
  ✓ Task requirements clarified

🔧 Backend Agent is creating Java/Spring Boot code...
  ✓ Backend API Implementation - User Authentication System
  ✓ Database Schema & Hibernate Mapping - User Authentication System
  ✓ Generated: pom.xml, entities, repositories, services, controllers

🎨 Frontend Agent is creating React/Next.js & TypeScript code...
  ✓ UI Components - User Authentication System
  ✓ Pages - User Authentication System
  ✓ Generated: package.json, tsconfig, components, services, pages

💾 Database Agent is creating Oracle/PL-SQL code...
  ✓ Database Schema - User Authentication System
  ✓ Query Optimization - User Authentication System
  ✓ Generated: schema, tables, CRUD procedures, migrations

✅ Project 'User Authentication System' processing complete!
```

### Option 3: Use projects.json File

```bash
python main.py --projects projects.json
```

**Setup:**
1. Edit `projects.json` with your projects
2. Each project needs:
   - `name`: Project name
   - `description`: What it does
   - `priority`: high/medium/low
   - `domains`: ["backend", "frontend", "database"]

**Example projects.json:**
```json
[
  {
    "name": "My E-Commerce App",
    "description": "Complete e-commerce platform with payments",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  },
  {
    "name": "User Management System",
    "description": "User authentication and authorization",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

### Option 4: Add Project via Command Line

```bash
python main.py --add-project "Project Name" --description "Project description" --priority high
```

**Optional parameters:**
```bash
--domains backend,frontend,database  # default: all three
--priority high|medium|low            # default: medium
```

**Examples:**
```bash
# Full-stack project
python main.py --add-project "Social Media" --description "Social network platform" --priority high

# Backend only
python main.py --add-project "REST API" --description "Microservice API" --priority high --domains backend

# Frontend only  
python main.py --add-project "Dashboard" --description "Analytics dashboard" --domains frontend

# Database only
python main.py --add-project "Data Schema" --description "Multi-tenant schema" --domains database
```

## What Gets Generated

### Agent Workflow

For **each project**, the agents work in this order:

1. **📋 Task Creator Agent**
   - Creates a main task from project description
   - Saves to `tasks/` folder

2. **🔍 Database Agent**
   - Clarifies ambiguous requirements
   - Validates task description

3. **🔧 Backend Agent** (if in domains)
   - Generates complete Spring Boot project structure
   - Creates pom.xml with dependencies
   - Generates JPA Entities with Hibernate annotations
   - Generates Spring Data JPA Repositories
   - Generates Service layer with business logic
   - Generates REST Controllers with CRUD endpoints
   - Generates application.yml configuration
   - **Saves to `backend/[project_name]/`**

4. **🎨 Frontend Agent** (if in domains)
   - Generates Next.js project with TypeScript
   - Creates package.json with all dependencies
   - Generates tsconfig.json and .eslintrc.json
   - Generates React components with hooks
   - Generates Axios API service layer
   - Creates Next.js pages structure
   - **Saves to `frontend/[project_name]/`**

5. **💾 Database Agent** (if in domains)
   - Generates Oracle schema creation script
   - Generates table definitions with indexes
   - Generates CRUD stored procedures
   - Generates PL/SQL packages
   - Generates migration scripts
   - **Saves to `dbadmin/[project_name]/`**

### Output Structure

```
tasks/
├── user_authentication_system_main.md
├── payment_processing_main.md
└── ...

subtasks/
├── backend/
│   ├── user_authentication_system_backend_api_implementation.md
│   ├── user_authentication_system_database_schema_hibernate_mapping.md
│   └── ...
├── frontend/
│   ├── user_authentication_system_ui_components.md
│   ├── user_authentication_system_pages.md
│   └── ...
└── database/
    ├── user_authentication_system_database_schema.md
    ├── user_authentication_system_query_optimization.md
    └── ...

backend/                                    # ← Generated Java/Spring Boot Code
└── [project_name]/
    ├── pom.xml                            # Maven configuration
    ├── src/main/java/com/example/[app]/
    │   ├── entity/User.java               # JPA Entities
    │   ├── repository/UserRepository.java # Spring Data JPA
    │   ├── service/UserService.java       # Business logic
    │   └── controller/UserController.java # REST APIs
    ├── src/main/resources/application.yml # Configuration
    └── setup.sh                           # Maven setup script

frontend/                                   # ← Generated React/Next.js Code
└── [project_name]/
    ├── package.json                       # Node.js dependencies
    ├── tsconfig.json                      # TypeScript config
    ├── .eslintrc.json                     # Linting rules
    ├── src/components/Button.tsx          # React components
    ├── src/pages/[page].tsx               # Next.js pages
    ├── src/services/api.service.ts        # Axios API client
    ├── src/hooks/                         # Custom hooks
    └── setup.sh                           # Node.js setup script

dbadmin/                                    # ← Generated Oracle/PL-SQL Code
└── [project_name]/
    ├── 001_schema_creation.sql            # Schema setup
    ├── tables/02_user_table.sql           # Table definitions
    ├── procedures/03_user_crud.sql        # CRUD procedures
    ├── packages/pkg_user_ops.sql          # PL/SQL packages
    ├── migrations/001_initial.sql         # Migration script
    ├── setup.sh                           # Oracle setup script
    └── README.md                          # Database docs
```

## Using Generated Code

### Backend (Java/Spring Boot)

```bash
cd backend/[project_name]

# View generated files
ls -la src/main/java/com/example/*/

# Setup Maven and run
./setup.sh
mvn clean compile
mvn spring-boot:run

# Server runs on http://localhost:8080
# All CRUD endpoints available at /api/v1/[resource]
```

**Generated includes:**
- ✅ pom.xml with Spring Boot, Hibernate, Lombok dependencies
- ✅ JPA Entities with Hibernate annotations
- ✅ Spring Data JPA repositories
- ✅ Service layer with business logic
- ✅ REST Controllers with all CRUD operations
- ✅ application.yml configuration
- ✅ Maven setup script

### Frontend (React/Next.js/TypeScript)

```bash
cd frontend/[project_name]

# View generated files
cat package.json
cat tsconfig.json
ls -la src/

# Setup Node.js and run
./setup.sh
npm install
npm run dev

# Dev server on http://localhost:3000
# All API calls use Axios with auth interceptor
```

**Generated includes:**
- ✅ package.json with React, Next.js, Axios, TypeScript
- ✅ tsconfig.json with strict type checking
- ✅ .eslintrc.json for code quality
- ✅ React components with hooks
- ✅ Axios API service with interceptors
- ✅ Next.js pages structure
- ✅ TypeScript interfaces for all types
- ✅ Node.js setup script

### Database (Oracle/PL-SQL)

```bash
cd dbadmin/[project_name]

# View generated SQL
cat 001_schema_creation.sql
cat tables/02_user_table.sql
cat procedures/03_user_crud.sql

# Setup Oracle database
./setup.sh
sqlplus /nolog
@001_schema_creation.sql
@tables/02_user_table.sql
@procedures/03_user_crud.sql

# Test CRUD procedures
EXECUTE pkg_user_ops.insert_record('user@email.com', 'password');
```

**Generated includes:**
- ✅ Oracle schema creation with tablespaces
- ✅ Table definitions with indexes and constraints
- ✅ CRUD stored procedures for each table
- ✅ Audit triggers for tracking changes
- ✅ PL/SQL packages for operations
- ✅ Migration scripts for versioning
- ✅ Oracle setup script
- ✅ Database documentation

## Full Example Workflow

### Step 1: Generate Code Interactively

```bash
python main.py --interactive

# Input:
# Project name: Social Network
# Description: Real-time social platform
# Priority: High
# Domains: all
```

### Step 2: Agents Generate Complete Project

```
🚀 Agents will generate code in:
   📁 backend/social_network/   - Spring Boot
   📁 frontend/social_network/  - React/Next.js
   📁 dbadmin/social_network/   - Oracle/PL-SQL
```

### Step 3: Setup Backend

```bash
cd backend/social_network
./setup.sh
mvn spring-boot:run

# Navigate to http://localhost:8080/api/v1
# All endpoints ready
```

### Step 4: Setup Frontend

```bash
cd frontend/social_network
./setup.sh
npm run dev

# Navigate to http://localhost:3000
# Connected to backend via Axios
```

### Step 5: Setup Database

```bash
cd dbadmin/social_network
./setup.sh
sqlplus /nolog
@001_schema_creation.sql
@tables/*.sql
@procedures/*.sql

# Database ready for use
```

### Step 6: Commit to GitHub

```bash
git add backend/ frontend/ dbadmin/ tasks/ subtasks/
git commit -m "Generated full-stack code for Social Network"
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

## Publishing to GitHub

### With Code Generation

```bash
# Generate code and prepare for GitHub
python main.py --interactive --publish --github-repo https://github.com/user/repo.git

# Or with samples
python main.py --sample --publish --github-repo https://github.com/user/repo.git
```

### Manual Push

```bash
# Stage generated code
git add backend/ frontend/ dbadmin/ tasks/ subtasks/

# Commit
git commit -m "Auto-generated full-stack code from agent team"

# Push
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

## Advanced Usage

### Process Multiple Projects

```bash
python main.py --projects projects.json
```

Generates code for all projects in separate folders.

### Use Custom Configuration

```bash
python main.py --config my-config.json --projects my-projects.json
```

### Single Domain Only

```bash
# Backend only
python main.py --interactive --domains backend

# Frontend only
python main.py --interactive --domains frontend

# Database only
python main.py --interactive --domains database
```

## Troubleshooting

### API Key Issues

**Error:** `Missing ANTHROPIC_API_KEY`

**Solution:**
```bash
echo ANTHROPIC_API_KEY=sk-your-key-here > .env
```

### No Code Generated

**Error:** Files in backend/, frontend/, dbadmin/ are empty

**Solution:**
- Ensure API key is valid
- Check that project domains include desired services
- Verify Python path and imports

### Permission Issues

**Error:** `Permission denied` when generating files

**Solution:**
```bash
# Run as administrator (Windows)
# Or ensure write permissions:
chmod 755 backend/ frontend/ dbadmin/
```

### Setup Script Failures

**Error:** `./setup.sh: command not found`

**Solution:**
```bash
# Make scripts executable
chmod +x backend/*/setup.sh
chmod +x frontend/*/setup.sh
chmod +x dbadmin/*/setup.sh

# Then run
./setup.sh
```

## Real-World Examples

### Example 1: Generate and Run Full-Stack App

```bash
# Generate
python main.py --interactive

# Setup Backend
cd backend/myapp && ./setup.sh && mvn spring-boot:run &

# Setup Frontend (in new terminal)
cd frontend/myapp && ./setup.sh && npm run dev &

# Setup Database (in new terminal)
cd dbadmin/myapp && ./setup.sh

# All three components running!
```

### Example 2: Generate Backend API Only

```bash
python main.py --add-project "User API" \
  --description "REST API for user management" \
  --domains backend \
  --priority high

cd backend/user_api
./setup.sh
mvn spring-boot:run
```

### Example 3: Generate Multiple Projects

```bash
# Create projects.json with 3 different apps
python main.py --projects projects.json

# Gets: backend/app1, backend/app2, backend/app3
#       frontend/app1, frontend/app2, frontend/app3
#       dbadmin/app1, dbadmin/app2, dbadmin/app3
```

## File Organization

Each agent stores generated code in dedicated folders:

```
backend/              ← Backend Agent generates here
├── project_1/       ← Each project in separate folder
├── project_2/
└── ...

frontend/             ← Frontend Agent generates here
├── project_1/
├── project_2/
└── ...

dbadmin/              ← Database Agent generates here
├── project_1/
├── project_2/
└── ...

tasks/                ← Task descriptions
subtasks/             ← Subtask documentation
```

## Tech Stack Generated

### Backend
- Java 21
- Spring Boot 3.x
- Hibernate & Spring Data JPA
- Maven
- Lombok

### Frontend
- React 18.x
- Next.js 14.x
- TypeScript 5.x
- Axios
- Tailwind CSS

### Database
- Oracle 21c/23c
- PL/SQL
- CRUD Procedures
- Audit Triggers

## Next Steps

1. ✅ Run agents: `python main.py --interactive`
2. 📁 Check generated code in `backend/`, `frontend/`, `dbadmin/`
3. 🔧 Run setup scripts in each folder
4. 🚀 Start development servers
5. 📝 Customize generated code for your needs
6. 🐙 Push to GitHub

## Tips

- **Start simple**: Use `--sample` first to see generated code
- **Review generated code**: Check quality and structure
- **Customize**: Generated code is a template, adapt as needed
- **Version control**: Commit frequently
- **Each agent**: Works independently but coordinates
- **Reusable**: Regenerate for different projects

## Documentation

- **CODE_GENERATION_GUIDE.md** - Detailed code examples
- **SKILLS_REFERENCE.md** - Complete skills reference
- **QUICKSTART.md** - 5-minute quick start
- **CLAUDE.md** - Full documentation

## Need Help?

- Check CLAUDE.md for detailed documentation
- Read CODE_GENERATION_GUIDE.md for code examples
- Check SKILLS_REFERENCE.md for capabilities
- Review generated code in backend/, frontend/, dbadmin/

---

**Happy full-stack development! 🚀**

Generated code is production-ready and ready for customization!

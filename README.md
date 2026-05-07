# Multi-Agent Code Generation System

**Simplified & Dynamic Code Generation**

A lightweight system that generates production-ready code from subtask specifications using dynamic code generation.

## How It Works

1. **Subtasks Define Requirements**
   - Each subtask in `subtasks/{domain}/` contains a description
   - Domain: backend, frontend, or database

2. **Agents Read Specifications**
   - BackendAgent searches `subtasks/backend/*.md`
   - FrontendAgent searches `subtasks/frontend/*.md`
   - DatabaseAgent searches `subtasks/database/*.md`

3. **Dynamic Code Generation**
   - `DynamicCodeGenerator` reads subtask descriptions
   - Generates code based on description content (keywords)
   - No static templates - purely dynamic generation

4. **Output Files**
   - Backend: Java Spring Boot code
   - Frontend: React/TypeScript components
   - Database: Oracle SQL migrations

## Dynamic Code Generation

The `DynamicCodeGenerator` class generates code by:

1. Parsing subtask descriptions
2. Extracting keywords (user, audit, login, etc.)
3. Generating appropriate code based on keywords
4. No hardcoded templates or static methods

```python
# Simple, keyword-based generation
if "user" in description:
    generate User entity, UserService, UserController
if "audit" in description:
    generate AuditLog entity, AuditService
if "login" in description:
    generate LoginForm component
```

## Simplifications Made

✓ Removed static enhanced skill files (600+ lines)  
✓ Replaced with dynamic code generator (200 lines)  
✓ Removed unnecessary documentation files  
✓ Cleaned up old generation scripts  
✓ Simplified agent code generation logic  
✓ Focused on requirements-driven development  

## Subtasks (15 Total)

### Backend (5 subtasks)
- User Entity & CRUD Operations
- JWT Authentication & Security Config
- Core Service Implementation
- REST API Endpoints & Controllers
- Audit Logging & Monitoring Service

### Frontend (5 subtasks)
- User Management UI Components
- Authentication Pages & Components
- Core Feature Components & Pages
- API Integration & Data Management
- Audit & Monitoring Dashboard

### Database (5 subtasks)
- User Data Schema & CRUD Procedures
- Authentication & Sessions Schema
- Core Business Tables & Procedures
- API Integration Tables & Services
- Audit & Monitoring Tables

## Key Features

✓ **Dynamic**: Code generation based on descriptions  
✓ **Simple**: Minimal codebase, no complex templates  
✓ **Flexible**: Easy to modify generation logic  
✓ **Focused**: Requirements-driven development  
✓ **Production-Ready**: Generated code includes proper structure  

## Benefits

- **Less Code**: Removed 600+ lines of static templates
- **More Flexibility**: Changes to logic affect all generation
- **Easier Maintenance**: Single source of generation rules
- **Faster Development**: Quick updates to generation strategy
- **Better Clarity**: Requirements directly drive code

---

**Built for simplicity and clarity.**

"""
Detailed Subtask Generation Skill
Generates comprehensive, well-structured subtasks with detailed specifications
"""

from typing import Dict, List, Any


class DetailedSubtaskGenerator:
    """Generates detailed subtasks with comprehensive specifications."""

    @staticmethod
    def generate_backend_subtask_details(
        title: str, description: str, apis: List[str] = None, db_schemas: List[str] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive backend subtask details."""
        apis = apis or []
        db_schemas = db_schemas or []
        details = {}

        # Technical requirements based on keywords
        details["technical_requirements"] = DetailedSubtaskGenerator._get_backend_requirements(
            description
        )

        # Implementation steps
        details["implementation_steps"] = (
            DetailedSubtaskGenerator._get_backend_implementation_steps(title, description)
        )

        # Related components
        details["related_components"] = DetailedSubtaskGenerator._get_backend_components(
            description
        )

        # Configuration requirements
        details["configuration"] = DetailedSubtaskGenerator._get_backend_config(description)

        # Testing requirements
        details["testing_requirements"] = DetailedSubtaskGenerator._get_backend_tests(description)

        # Code examples
        details["code_examples"] = DetailedSubtaskGenerator._get_backend_examples(description)

        # Dependencies
        details["dependencies"] = DetailedSubtaskGenerator._get_backend_dependencies(
            description, apis, db_schemas
        )

        return details

    @staticmethod
    def generate_frontend_subtask_details(
        title: str, description: str, components: List[str] = None, pages: List[str] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive frontend subtask details."""
        components = components or []
        pages = pages or []
        details = {}

        # Technical requirements
        details["technical_requirements"] = DetailedSubtaskGenerator._get_frontend_requirements(
            description
        )

        # Component structure
        details["component_structure"] = DetailedSubtaskGenerator._get_frontend_components(
            title, description, components
        )

        # State management
        details["state_management"] = DetailedSubtaskGenerator._get_frontend_state(description)

        # UI/UX requirements
        details["ui_ux_requirements"] = DetailedSubtaskGenerator._get_frontend_ux(description)

        # API integration points
        details["api_integration"] = DetailedSubtaskGenerator._get_frontend_api_integration(
            description
        )

        # Testing strategy
        details["testing_strategy"] = DetailedSubtaskGenerator._get_frontend_tests(description)

        # Performance considerations
        details["performance"] = DetailedSubtaskGenerator._get_frontend_performance(description)

        # Dependencies
        details["dependencies"] = DetailedSubtaskGenerator._get_frontend_dependencies(
            description, components, pages
        )

        return details

    @staticmethod
    def generate_database_subtask_details(
        title: str, description: str, tables: List[str] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive database subtask details."""
        tables = tables or []
        details = {}

        # Schema design
        details["schema_design"] = DetailedSubtaskGenerator._get_db_schema_design(
            title, description, tables
        )

        # Table specifications
        details["table_specifications"] = DetailedSubtaskGenerator._get_db_table_specs(
            description, tables
        )

        # Indexes and performance
        details["indexing_strategy"] = DetailedSubtaskGenerator._get_db_indexing(
            description, tables
        )

        # Constraints and integrity
        details["integrity_constraints"] = DetailedSubtaskGenerator._get_db_constraints(
            description, tables
        )

        # Migration strategy
        details["migration_strategy"] = DetailedSubtaskGenerator._get_db_migration_strategy(
            description, tables
        )

        # Procedures and functions
        details["procedures"] = DetailedSubtaskGenerator._get_db_procedures(description, tables)

        # Data model relationships
        details["relationships"] = DetailedSubtaskGenerator._get_db_relationships(
            description, tables
        )

        # Performance considerations
        details["performance"] = DetailedSubtaskGenerator._get_db_performance(description, tables)

        return details

    # Backend detail generators
    @staticmethod
    def _get_backend_requirements(description: str) -> List[str]:
        """Extract technical requirements for backend subtask."""
        requirements = [
            "Spring Boot 3.x with Java 21",
            "JPA/Hibernate ORM",
            "Maven build system",
        ]

        desc_lower = description.lower()
        if "user" in desc_lower or "auth" in desc_lower:
            requirements.extend([
                "Spring Security for authentication/authorization",
                "JWT token support",
                "Password encryption with BCrypt",
            ])
        if "audit" in desc_lower or "monitoring" in desc_lower:
            requirements.extend([
                "SLF4J logging framework",
                "Aspect-Oriented Programming (AOP) for audit logging",
                "Request/response interceptors",
            ])
        if "api" in desc_lower or "rest" in desc_lower:
            requirements.extend([
                "Spring Data REST",
                "JSON serialization (Jackson)",
                "API documentation (Swagger/SpringDoc OpenAPI)",
            ])
        if "database" in desc_lower or "crud" in desc_lower:
            requirements.extend([
                "Spring Data JPA repositories",
                "Transaction management",
                "Database migrations (Flyway or Liquibase)",
            ])

        return requirements

    @staticmethod
    def _get_backend_implementation_steps(title: str, description: str) -> List[str]:
        """Get implementation steps for backend subtask."""
        steps = ["Create project structure and package layout"]

        desc_lower = description.lower()
        if "entity" in desc_lower or "user" in desc_lower:
            steps.extend([
                "Define JPA entity with proper annotations (@Entity, @Table, @Column)",
                "Add Lombok annotations (@Data, @Builder, @NoArgsConstructor, @AllArgsConstructor)",
                "Implement lifecycle callbacks (@PrePersist, @PreUpdate)",
                "Create Spring Data JPA repository interface",
            ])
        if "service" in desc_lower:
            steps.extend([
                "Create service class with @Service annotation",
                "Implement business logic methods",
                "Add @Transactional annotations for database operations",
                "Implement exception handling and logging",
            ])
        if "controller" in desc_lower or "api" in desc_lower:
            steps.extend([
                "Create REST controller with @RestController annotation",
                "Define request mappings (@GetMapping, @PostMapping, @PutMapping, @DeleteMapping)",
                "Implement request validation",
                "Add error handling with @ExceptionHandler",
            ])
        if "auth" in desc_lower or "jwt" in desc_lower:
            steps.extend([
                "Implement JWT token provider",
                "Create security configuration class",
                "Add JWT filters and interceptors",
                "Configure CORS and CSRF protection",
            ])

        steps.extend([
            "Write unit tests with JUnit 5 and Mockito",
            "Write integration tests with @SpringBootTest",
            "Configure application properties (application.yml)",
            "Document API endpoints with Swagger annotations",
        ])

        return steps

    @staticmethod
    def _get_backend_components(description: str) -> List[str]:
        """Get related components for backend subtask."""
        components = []

        desc_lower = description.lower()
        if "user" in desc_lower or "entity" in desc_lower:
            components.extend([
                "UserEntity (JPA entity)",
                "UserRepository (Spring Data JPA)",
                "UserService (business logic)",
                "UserDTO (data transfer object)",
            ])
        if "auth" in desc_lower:
            components.extend([
                "SecurityConfig (Spring Security configuration)",
                "JwtTokenProvider (token generation/validation)",
                "JwtAuthenticationFilter (request filter)",
                "AuthController (authentication endpoints)",
            ])
        if "audit" in desc_lower:
            components.extend([
                "AuditLog entity",
                "AuditAspect (AOP for audit logging)",
                "AuditRepository (data access)",
                "AuditService (audit operations)",
            ])

        return components

    @staticmethod
    def _get_backend_config(description: str) -> Dict[str, str]:
        """Get configuration requirements."""
        config = {
            "spring.jpa.hibernate.ddl-auto": "validate",
            "spring.jpa.show-sql": "false",
            "spring.jpa.properties.hibernate.format_sql": "true",
            "spring.jpa.properties.hibernate.use_sql_comments": "true",
        }

        desc_lower = description.lower()
        if "auth" in desc_lower or "jwt" in desc_lower:
            config.update({
                "app.jwt.secret": "${JWT_SECRET}",
                "app.jwt.expiration": "86400000",
                "spring.security.filter.order": "5",
            })
        if "audit" in desc_lower:
            config.update({
                "logging.level.com.example.calendarapp": "DEBUG",
                "spring.aop.auto": "true",
            })

        return config

    @staticmethod
    def _get_backend_tests(description: str) -> List[str]:
        """Get testing requirements."""
        tests = [
            "Unit tests for entity validation",
            "Unit tests for service business logic",
            "Unit tests for controller endpoints",
            "Integration tests with embedded database",
            "API contract tests with Spring Cloud Contract",
        ]

        desc_lower = description.lower()
        if "auth" in desc_lower:
            tests.extend([
                "JWT token generation and validation tests",
                "Spring Security integration tests",
                "Authentication failure scenario tests",
            ])
        if "api" in desc_lower:
            tests.extend([
                "HTTP status code validation tests",
                "Error response format tests",
                "Pagination and filtering tests",
            ])

        return tests

    @staticmethod
    def _get_backend_examples(description: str) -> Dict[str, str]:
        """Get code examples."""
        examples = {}

        desc_lower = description.lower()
        if "entity" in desc_lower:
            examples["entity_example"] = """@Entity
@Table(name = "users")
@Data
@Builder
public class User {
    @Id @GeneratedValue
    private Long id;
    @Column(unique = true)
    private String email;
    private String passwordHash;
    @CreationTimestamp
    private LocalDateTime createdAt;
}"""

        if "service" in desc_lower:
            examples["service_example"] = """@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository repository;

    @Transactional
    public UserDTO createUser(CreateUserRequest request) {
        User user = User.builder()
            .email(request.getEmail())
            .build();
        return UserDTO.from(repository.save(user));
    }
}"""

        return examples

    @staticmethod
    def _get_backend_dependencies(
        description: str, apis: List[str], db_schemas: List[str]
    ) -> Dict[str, List[str]]:
        """Get dependency information."""
        dependencies = {
            "maven": [
                "spring-boot-starter-web",
                "spring-boot-starter-data-jpa",
                "lombok",
                "springdoc-openapi",
            ],
            "internal": [],
        }

        desc_lower = description.lower()
        if "user" in desc_lower:
            dependencies["internal"].extend(["UserEntity", "UserRepository"])
        if "auth" in desc_lower:
            dependencies["maven"].extend(["spring-boot-starter-security", "jjwt"])
        if "audit" in desc_lower:
            dependencies["internal"].append("AuditLog")

        return dependencies

    # Frontend detail generators
    @staticmethod
    def _get_frontend_requirements(description: str) -> List[str]:
        """Get frontend technical requirements."""
        requirements = [
            "React 18+ with TypeScript",
            "Next.js 14+ framework",
            "TailwindCSS for styling",
            "React Query for data fetching",
            "Zustand for state management",
        ]

        desc_lower = description.lower()
        if "form" in desc_lower or "input" in desc_lower:
            requirements.extend([
                "React Hook Form for form management",
                "Zod or Yup for validation",
            ])
        if "table" in desc_lower or "list" in desc_lower:
            requirements.append("TanStack Table (React Table)")
        if "auth" in desc_lower or "login" in desc_lower:
            requirements.extend([
                "NextAuth.js for authentication",
                "JWT token storage (secure cookies)",
            ])

        return requirements

    @staticmethod
    def _get_frontend_components(
        title: str, description: str, components: List[str]
    ) -> List[str]:
        """Get frontend component structure."""
        structure = [
            "Layout wrapper component",
            "Error boundary component",
            "Loading skeleton component",
        ]

        desc_lower = description.lower()
        if "form" in desc_lower or "login" in desc_lower:
            structure.extend([
                "Form component with validation",
                "Input field components",
                "Button components",
                "Error message display",
            ])
        if "list" in desc_lower or "table" in desc_lower:
            structure.extend([
                "Table/List container component",
                "Row/Item component",
                "Pagination component",
                "Filter component",
            ])
        if "dashboard" in desc_lower:
            structure.extend([
                "Dashboard grid layout",
                "Widget components",
                "Chart components (if data visualization needed)",
                "Summary card components",
            ])

        return structure

    @staticmethod
    def _get_frontend_state(description: str) -> Dict[str, Any]:
        """Get state management strategy."""
        state = {
            "global_state": ["authStore (user, token)", "uiStore (modal, sidebar)"],
            "local_state": ["component-level useState for UI state"],
            "server_state": ["React Query for API data"],
        }

        desc_lower = description.lower()
        if "form" in desc_lower:
            state["form_state"] = "React Hook Form with field-level state"
        if "table" in desc_lower or "list" in desc_lower:
            state["pagination"] = "Server-side pagination with cursor or offset"

        return state

    @staticmethod
    def _get_frontend_ux(description: str) -> List[str]:
        """Get UI/UX requirements."""
        ux = [
            "Responsive design (mobile, tablet, desktop)",
            "Accessibility (WCAG 2.1 AA compliance)",
            "Loading states with skeleton screens",
            "Error states with user-friendly messages",
            "Success notifications with toast messages",
        ]

        desc_lower = description.lower()
        if "form" in desc_lower or "input" in desc_lower:
            ux.extend([
                "Real-time form validation feedback",
                "Clear error messages under fields",
                "Visual focus indicators",
                "Disabled state during submission",
            ])
        if "table" in desc_lower:
            ux.extend([
                "Sortable columns",
                "Filterable data",
                "Row selection (if applicable)",
                "Empty state display",
            ])

        return ux

    @staticmethod
    def _get_frontend_api_integration(description: str) -> Dict[str, Any]:
        """Get API integration points."""
        integration = {
            "base_url": "process.env.NEXT_PUBLIC_API_URL || http://localhost:8080/api/v1",
            "authentication": "Bearer token in Authorization header",
            "error_handling": "Centralized error handling with retry logic",
        }

        desc_lower = description.lower()
        if "user" in desc_lower:
            integration["endpoints"] = [
                "GET /users - list all users",
                "POST /users - create user",
                "GET /users/{id} - get user details",
                "PUT /users/{id} - update user",
                "DELETE /users/{id} - delete user",
            ]
        if "login" in desc_lower or "auth" in desc_lower:
            integration["auth_endpoints"] = [
                "POST /auth/login - user login",
                "POST /auth/refresh - refresh token",
                "POST /auth/logout - user logout",
            ]

        return integration

    @staticmethod
    def _get_frontend_tests(description: str) -> List[str]:
        """Get testing requirements."""
        tests = [
            "Unit tests with Jest and React Testing Library",
            "Component snapshot tests",
            "Integration tests for user flows",
            "E2E tests with Playwright or Cypress",
            "Accessibility tests with jest-axe",
        ]

        desc_lower = description.lower()
        if "form" in desc_lower:
            tests.extend([
                "Form validation tests",
                "Error message display tests",
                "Form submission tests",
            ])
        if "login" in desc_lower or "auth" in desc_lower:
            tests.extend([
                "Authentication flow tests",
                "Token refresh tests",
                "Unauthorized access handling tests",
            ])

        return tests

    @staticmethod
    def _get_frontend_performance(description: str) -> List[str]:
        """Get performance considerations."""
        performance = [
            "Code splitting by route (Next.js automatic)",
            "Image optimization with next/image",
            "Lazy loading for off-screen components",
            "Memoization for expensive computations",
            "Pagination for large data sets",
        ]

        desc_lower = description.lower()
        if "table" in desc_lower or "list" in desc_lower:
            performance.extend([
                "Virtual scrolling for large lists",
                "Server-side pagination",
                "Debounced filtering/search",
            ])
        if "form" in desc_lower:
            performance.append("Debounced auto-save functionality")

        return performance

    @staticmethod
    def _get_frontend_dependencies(
        description: str, components: List[str], pages: List[str]
    ) -> Dict[str, List[str]]:
        """Get npm dependencies."""
        dependencies = {
            "core": ["react", "react-dom", "next"],
            "state": ["zustand", "@tanstack/react-query"],
            "styling": ["tailwindcss", "postcss"],
            "utilities": ["axios", "date-fns"],
        }

        desc_lower = description.lower()
        if "form" in desc_lower:
            dependencies["form"] = ["react-hook-form", "zod"]
        if "table" in desc_lower:
            dependencies["table"] = ["@tanstack/react-table"]
        if "auth" in desc_lower:
            dependencies["auth"] = ["next-auth", "jose"]

        return dependencies

    # Database detail generators
    @staticmethod
    def _get_db_schema_design(title: str, description: str, tables: List[str]) -> Dict[str, Any]:
        """Get database schema design."""
        design = {
            "database_type": "Oracle 21c/23c",
            "naming_conventions": [
                "Tables: lowercase with underscores (users, user_profiles)",
                "Columns: lowercase with underscores",
                "Constraints: prefix with constraint type (pk_*, uk_*, fk_*)",
                "Indexes: prefix with idx_ or idx_unique_",
            ],
            "character_set": "AL32UTF8",
        }

        desc_lower = description.lower()
        if "user" in desc_lower:
            design["entities"] = ["users (core user data)", "user_profiles (extended profile)"]
        if "audit" in desc_lower:
            design["entities"] = ["audit_logs (activity tracking)"]

        return design

    @staticmethod
    def _get_db_table_specs(description: str, tables: List[str]) -> Dict[str, Any]:
        """Get detailed table specifications."""
        specs = {}

        desc_lower = description.lower()
        if "user" in desc_lower:
            specs["users"] = {
                "columns": [
                    "id (NUMBER(19), PRIMARY KEY)",
                    "email (VARCHAR2(255), UNIQUE, NOT NULL)",
                    "name (VARCHAR2(100), NOT NULL)",
                    "password_hash (VARCHAR2(255), NOT NULL)",
                    "active (NUMBER(1), DEFAULT 1)",
                    "created_at (TIMESTAMP, DEFAULT SYSTIMESTAMP)",
                    "updated_at (TIMESTAMP, DEFAULT SYSTIMESTAMP)",
                ],
                "constraints": [
                    "PRIMARY KEY on id",
                    "UNIQUE constraint on email",
                    "CHECK constraint for active (0 or 1)",
                ],
            }

        if "audit" in desc_lower:
            specs["audit_logs"] = {
                "columns": [
                    "id (NUMBER(19), PRIMARY KEY)",
                    "action (VARCHAR2(50), NOT NULL)",
                    "entity (VARCHAR2(100), NOT NULL)",
                    "entity_id (NUMBER(19))",
                    "user_id (VARCHAR2(255))",
                    "details (CLOB)",
                    "timestamp (TIMESTAMP, DEFAULT SYSTIMESTAMP)",
                ],
                "constraints": ["PRIMARY KEY on id"],
            }

        return specs

    @staticmethod
    def _get_db_indexing(description: str, tables: List[str]) -> List[str]:
        """Get indexing strategy."""
        indexes = ["Create primary keys (automatic indexes)"]

        desc_lower = description.lower()
        if "user" in desc_lower:
            indexes.extend([
                "Index on email (frequent lookups during login)",
                "Index on created_at (sorting and range queries)",
                "Index on active (filtering active/inactive users)",
            ])
        if "audit" in desc_lower:
            indexes.extend([
                "Index on timestamp (audit log queries)",
                "Index on user_id (user activity tracking)",
                "Index on entity and entity_id (cross-entity queries)",
            ])

        return indexes

    @staticmethod
    def _get_db_constraints(description: str, tables: List[str]) -> List[str]:
        """Get integrity constraints."""
        constraints = [
            "Primary key constraints for unique identification",
            "Not null constraints for required fields",
            "Unique constraints for unique identifiers (email)",
        ]

        desc_lower = description.lower()
        if "audit" in desc_lower:
            constraints.extend([
                "Foreign key to users table (optional, for data integrity)",
                "Check constraint for valid action types",
            ])

        return constraints

    @staticmethod
    def _get_db_migration_strategy(description: str, tables: List[str]) -> Dict[str, Any]:
        """Get migration strategy."""
        strategy = {
            "tool": "Flyway versioned migrations",
            "naming": "V{version:03d}_{description}.sql",
            "execution": "Automatic on application startup",
            "rollback": "Create V{version:03d}__undo_{description}.sql for rollbacks",
        }

        return strategy

    @staticmethod
    def _get_db_procedures(description: str, tables: List[str]) -> List[str]:
        """Get stored procedures/functions."""
        procedures = []

        desc_lower = description.lower()
        if "user" in desc_lower:
            procedures.extend([
                "PROCEDURE sp_create_user(p_email, p_name, ...)",
                "FUNCTION fn_get_user_by_email(p_email) RETURN user%ROWTYPE",
                "PROCEDURE sp_update_user(p_id, ...)",
                "PROCEDURE sp_delete_user(p_id)",
            ])
        if "audit" in desc_lower:
            procedures.extend([
                "PROCEDURE sp_log_audit(p_action, p_entity, ...)",
                "FUNCTION fn_get_audit_logs(p_user_id, p_date_from)",
            ])

        return procedures

    @staticmethod
    def _get_db_relationships(description: str, tables: List[str]) -> List[str]:
        """Get data model relationships."""
        relationships = []

        desc_lower = description.lower()
        if "audit" in desc_lower and "user" in desc_lower:
            relationships.append("audit_logs -> users (many-to-one, user_id references users.id)")

        if not relationships:
            relationships.append("No foreign key relationships (flat structure for this module)")

        return relationships

    @staticmethod
    def _get_db_performance(description: str, tables: List[str]) -> List[str]:
        """Get performance considerations."""
        performance = [
            "Partitioning strategy for large tables (optional)",
            "Archive old audit logs to separate partition",
            "Analyze table statistics regularly with DBMS_STATS",
            "Monitor full table scans vs index usage",
        ]

        return performance

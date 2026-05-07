"""
Orchestrator - Dynamically assigns subtasks to appropriate agents
Routes backend subtasks to BackendAgent
Routes frontend subtasks to FrontendAgent
Routes database subtasks to DatabaseAgent
"""

from pathlib import Path
from typing import Dict, List, Any
from skills.code_generator import DynamicCodeGenerator


class TaskOrchestrator:
    """Orchestrates task distribution to appropriate agents based on domain."""

    def __init__(self):
        self.subtasks_dir = Path("subtasks")
        self.domains = ["backend", "frontend", "database"]

    def discover_all_subtasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover and categorize all subtasks by domain."""
        categorized = {
            "backend": [],
            "frontend": [],
            "database": []
        }

        for domain in self.domains:
            domain_path = self.subtasks_dir / domain
            if not domain_path.exists():
                continue

            md_files = sorted(domain_path.glob("*.md"))
            for md_file in md_files:
                if md_file.name in ["README.md", "project_summary.md"]:
                    continue

                spec = DynamicCodeGenerator.parse_subtask(str(md_file))
                if spec.get("title"):
                    subtask = {
                        "file": str(md_file),
                        "domain": domain,
                        "spec": spec
                    }
                    categorized[domain].append(subtask)

        return categorized

    def execute_backend_development(self, subtasks: List[Dict[str, Any]]) -> None:
        """Execute backend agent for all backend subtasks."""
        from agents.backend_agent import BackendAgent

        if not subtasks:
            print("[SKIP] No backend subtasks")
            return

        print(f"\n[BACKEND AGENT] Processing {len(subtasks)} subtasks...\n")

        agent = BackendAgent()
        project_folder = Path("backend/calendar_app")
        base_package = "calendarapp"

        for subtask in subtasks:
            spec = subtask["spec"]
            description = spec.get("description", "").lower()

            print(f"  [{subtask['domain'].upper()}] {spec.get('title', 'Unknown')[:60]}")

            # Generate User-related code
            if "user" in description:
                entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
                service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
                controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"

                entity_dir.mkdir(parents=True, exist_ok=True)
                service_dir.mkdir(parents=True, exist_ok=True)
                controller_dir.mkdir(parents=True, exist_ok=True)

                from skills.code_generator import DynamicCodeGenerator

                user_entity = DynamicCodeGenerator.generate_java_entity(spec, "User")
                entity_path = entity_dir / "User.java"
                entity_path.write_text(user_entity, encoding="utf-8")
                print(f"      [GENERATED] User.java")

                user_service = DynamicCodeGenerator.generate_java_service(spec, "UserService")
                service_path = service_dir / "UserService.java"
                service_path.write_text(user_service, encoding="utf-8")
                print(f"      [GENERATED] UserService.java")

                user_controller = DynamicCodeGenerator.generate_java_controller(spec, "UserController")
                controller_path = controller_dir / "UserController.java"
                controller_path.write_text(user_controller, encoding="utf-8")
                print(f"      [GENERATED] UserController.java")

            # Generate Audit-related code
            if "audit" in description:
                entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
                service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"

                entity_dir.mkdir(parents=True, exist_ok=True)
                service_dir.mkdir(parents=True, exist_ok=True)

                from skills.code_generator import DynamicCodeGenerator

                audit_entity = DynamicCodeGenerator.generate_java_entity(spec, "AuditLog")
                entity_path = entity_dir / "AuditLog.java"
                entity_path.write_text(audit_entity, encoding="utf-8")
                print(f"      [GENERATED] AuditLog.java")

                audit_service = DynamicCodeGenerator.generate_java_service(spec, "AuditService")
                service_path = service_dir / "AuditService.java"
                service_path.write_text(audit_service, encoding="utf-8")
                print(f"      [GENERATED] AuditService.java")

            # Generate Authentication code
            if "auth" in description or "jwt" in description:
                security_dir = project_folder / f"src/main/java/com/example/{base_package}/security"
                security_dir.mkdir(parents=True, exist_ok=True)

                from skills.code_generator import DynamicCodeGenerator

                jwt_code = DynamicCodeGenerator.generate_java_service(spec, "JwtTokenProvider")
                jwt_path = security_dir / "JwtTokenProvider.java"
                jwt_path.write_text(jwt_code, encoding="utf-8")
                print(f"      [GENERATED] JwtTokenProvider.java")

    def execute_frontend_development(self, subtasks: List[Dict[str, Any]]) -> None:
        """Execute frontend agent for all frontend subtasks."""
        from agents.frontend_agent import FrontendAgent

        if not subtasks:
            print("[SKIP] No frontend subtasks")
            return

        print(f"\n[FRONTEND AGENT] Processing {len(subtasks)} subtasks...\n")

        agent = FrontendAgent()
        project_folder = Path("frontend/calendar_app")

        for subtask in subtasks:
            spec = subtask["spec"]
            description = spec.get("description", "").lower()

            print(f"  [{subtask['domain'].upper()}] {spec.get('title', 'Unknown')[:60]}")

            components_dir = project_folder / "src/components"
            pages_dir = project_folder / "src/pages"
            services_dir = project_folder / "src/services"

            components_dir.mkdir(parents=True, exist_ok=True)
            pages_dir.mkdir(parents=True, exist_ok=True)
            services_dir.mkdir(parents=True, exist_ok=True)

            from skills.code_generator import DynamicCodeGenerator

            # Generate Authentication components
            if "login" in description or "auth" in description:
                login_code = DynamicCodeGenerator.generate_react_component(spec, "LoginForm")
                login_path = components_dir / "LoginForm.tsx"
                login_path.write_text(login_code, encoding="utf-8")
                print(f"      [GENERATED] LoginForm.tsx")

            # Generate User Management components
            if "user" in description:
                if "list" in description or "management" in description:
                    userlist_code = DynamicCodeGenerator.generate_react_component(spec, "UserList")
                    userlist_path = components_dir / "UserList.tsx"
                    userlist_path.write_text(userlist_code, encoding="utf-8")
                    print(f"      [GENERATED] UserList.tsx")

            # Generate Dashboard
            if "dashboard" in description:
                dashboard_code = DynamicCodeGenerator.generate_react_component(spec, "Dashboard")
                dashboard_path = pages_dir / "dashboard.tsx"
                dashboard_path.write_text(dashboard_code, encoding="utf-8")
                print(f"      [GENERATED] dashboard.tsx")

            # Generate API Service
            if "api" in description or "service" in description.lower():
                api_code = DynamicCodeGenerator.generate_react_component(spec, "ApiService")
                api_path = services_dir / "api.service.ts"
                api_path.write_text(api_code, encoding="utf-8")
                print(f"      [GENERATED] api.service.ts")

    def execute_database_development(self, subtasks: List[Dict[str, Any]]) -> None:
        """Execute database agent for all database subtasks."""
        from agents.database_agent import DatabaseAgent

        if not subtasks:
            print("[SKIP] No database subtasks")
            return

        print(f"\n[DATABASE AGENT] Processing {len(subtasks)} subtasks...\n")

        agent = DatabaseAgent()
        project_folder = Path("dbadmin/calendar_app")
        migrations_dir = project_folder / "migrations"
        migrations_dir.mkdir(parents=True, exist_ok=True)

        version = 1

        for subtask in subtasks:
            spec = subtask["spec"]
            description = spec.get("description", "").lower()

            print(f"  [{subtask['domain'].upper()}] {spec.get('title', 'Unknown')[:60]}")

            from skills.code_generator import DynamicCodeGenerator

            # Generate User table
            if "user" in description:
                migration_sql = DynamicCodeGenerator.generate_sql_migration(spec, version, "users")
                migration_path = migrations_dir / f"V{version:03d}_create_users_table.sql"
                migration_path.write_text(migration_sql, encoding="utf-8")
                print(f"      [GENERATED] V{version:03d}_create_users_table.sql")
                version += 1

            # Generate Audit tables
            if "audit" in description:
                migration_sql = DynamicCodeGenerator.generate_sql_migration(spec, version, "audit_logs")
                migration_path = migrations_dir / f"V{version:03d}_create_audit_logs_table.sql"
                migration_path.write_text(migration_sql, encoding="utf-8")
                print(f"      [GENERATED] V{version:03d}_create_audit_logs_table.sql")
                version += 1

            # Generate Session tables
            if "session" in description or "auth" in description:
                migration_sql = DynamicCodeGenerator.generate_sql_migration(spec, version, "sessions")
                migration_path = migrations_dir / f"V{version:03d}_create_sessions_table.sql"
                migration_path.write_text(migration_sql, encoding="utf-8")
                print(f"      [GENERATED] V{version:03d}_create_sessions_table.sql")
                version += 1

            # Generate Integration tables
            if "integration" in description:
                migration_sql = DynamicCodeGenerator.generate_sql_migration(spec, version, "integrations")
                migration_path = migrations_dir / f"V{version:03d}_create_integrations_table.sql"
                migration_path.write_text(migration_sql, encoding="utf-8")
                print(f"      [GENERATED] V{version:03d}_create_integrations_table.sql")
                version += 1

    def orchestrate(self) -> None:
        """Main orchestration - discover subtasks and route to agents."""
        print("\n" + "="*70)
        print("DYNAMIC TASK ORCHESTRATION - ROUTING SUBTASKS TO AGENTS")
        print("="*70)

        # Discover all subtasks
        categorized = self.discover_all_subtasks()

        print("\n[DISCOVERY]")
        print(f"  Backend subtasks: {len(categorized['backend'])}")
        print(f"  Frontend subtasks: {len(categorized['frontend'])}")
        print(f"  Database subtasks: {len(categorized['database'])}")
        print(f"  Total: {sum(len(v) for v in categorized.values())}")

        # Route to appropriate agents
        self.execute_backend_development(categorized["backend"])
        self.execute_frontend_development(categorized["frontend"])
        self.execute_database_development(categorized["database"])

        # Summary
        print("\n" + "="*70)
        print("ORCHESTRATION COMPLETE")
        print("="*70)
        print(f"  Backend: {len(categorized['backend'])} subtasks processed")
        print(f"  Frontend: {len(categorized['frontend'])} subtasks processed")
        print(f"  Database: {len(categorized['database'])} subtasks processed")
        print("="*70 + "\n")


if __name__ == "__main__":
    orchestrator = TaskOrchestrator()
    orchestrator.orchestrate()

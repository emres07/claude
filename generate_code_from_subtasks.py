"""
Code Generation from Subtask Specifications
Reads subtask MD files and generates production-ready code based on their descriptions.
"""

import os
from pathlib import Path
from skills.backend_skills_enhanced import EnhancedBackendSkill
from skills.frontend_skills_enhanced import EnhancedFrontendSkill
from skills.database_skills_enhanced import EnhancedDatabaseSkill


class SubtaskCodeGenerator:
    """Generates code from subtask MD file specifications."""

    def __init__(self):
        self.backend_dir = Path("subtasks/backend")
        self.frontend_dir = Path("subtasks/frontend")
        self.database_dir = Path("subtasks/database")
        self.generated_files = []

    def generate_all(self):
        """Generate code for all subtasks."""
        print("\n" + "="*70)
        print("GENERATING CODE FROM SUBTASK SPECIFICATIONS")
        print("="*70 + "\n")

        # Generate backend code
        print("[BACKEND] Generating code from subtask specifications...")
        self._generate_backend_code()

        # Generate frontend code
        print("\n[FRONTEND] Generating code from subtask specifications...")
        self._generate_frontend_code()

        # Generate database migrations
        print("\n[DATABASE] Generating migrations from subtask specifications...")
        self._generate_database_code()

        # Summary
        self._print_summary()

    def _generate_backend_code(self):
        """Generate backend code from subtask MD files."""
        if not self.backend_dir.exists():
            print("  [SKIP] Backend subtasks directory not found")
            return

        project_folder = Path("backend/calendar_app")
        base_package = "calendarapp"

        for md_file in sorted(self.backend_dir.glob("*.md")):
            if md_file.name != "README.md":
                spec = EnhancedBackendSkill.parse_readme(str(md_file))
                if not spec or not spec.get("title"):
                    continue

                print(f"\n  [{md_file.stem}]")
                print(f"    Title: {spec['title']}")
                print(f"    Description: {spec['description'][:70]}...")

                # Generate based on business process
                business_process = self._extract_business_process(spec['title'])

                if "user" in spec['description'].lower() and "entity" in spec['description'].lower():
                    self._generate_user_entity(project_folder, base_package, spec)
                    print(f"    [GENERATED] User.java (Entity)")
                    self._generate_user_repository(project_folder, base_package, spec)
                    print(f"    [GENERATED] UserRepository.java")
                    self._generate_user_service(project_folder, base_package, spec)
                    print(f"    [GENERATED] UserService.java (Service)")

                if "audit" in spec['description'].lower():
                    self._generate_audit_service(project_folder, base_package, spec)
                    print(f"    [GENERATED] AuditService.java")

                if "jwt" in spec['description'].lower() or "authentication" in spec['description'].lower():
                    self._generate_jwt_provider(project_folder, base_package, spec)
                    print(f"    [GENERATED] JwtTokenProvider.java")

                if "rest api" in spec['description'].lower() or "controller" in spec['description'].lower():
                    self._generate_user_controller(project_folder, base_package, spec)
                    print(f"    [GENERATED] UserController.java (REST Endpoints)")

    def _generate_frontend_code(self):
        """Generate frontend code from subtask MD files."""
        if not self.frontend_dir.exists():
            print("  [SKIP] Frontend subtasks directory not found")
            return

        project_folder = Path("frontend/calendar_app")

        for md_file in sorted(self.frontend_dir.glob("*.md")):
            if md_file.name != "README.md":
                spec = EnhancedFrontendSkill.parse_readme(str(md_file))
                if not spec or not spec.get("title"):
                    continue

                print(f"\n  [{md_file.stem}]")
                print(f"    Title: {spec['title']}")
                print(f"    Description: {spec['description'][:70]}...")

                components_dir = project_folder / "src/components"
                pages_dir = project_folder / "src/pages"
                services_dir = project_folder / "src/services"

                components_dir.mkdir(parents=True, exist_ok=True)
                pages_dir.mkdir(parents=True, exist_ok=True)
                services_dir.mkdir(parents=True, exist_ok=True)

                if "login" in spec['description'].lower():
                    login_path = components_dir / "LoginForm.tsx"
                    login_path.write_text(
                        EnhancedFrontendSkill.generate_login_component_from_spec(spec),
                        encoding='utf-8'
                    )
                    print(f"    [GENERATED] LoginForm.tsx")
                    self.generated_files.append(str(login_path))

                if "api" in spec['description'].lower() and "service" in spec['description'].lower():
                    api_path = services_dir / "api.service.ts"
                    api_path.write_text(
                        EnhancedFrontendSkill.generate_api_service_from_spec(spec),
                        encoding='utf-8'
                    )
                    print(f"    [GENERATED] api.service.ts (API Client)")
                    self.generated_files.append(str(api_path))

                if "user" in spec['description'].lower() and "list" in spec['description'].lower():
                    userlist_path = components_dir / "UserList.tsx"
                    userlist_path.write_text(
                        EnhancedFrontendSkill.generate_user_list_component_from_spec(spec),
                        encoding='utf-8'
                    )
                    print(f"    [GENERATED] UserList.tsx (Component)")
                    self.generated_files.append(str(userlist_path))

                if "dashboard" in spec['description'].lower():
                    dashboard_path = pages_dir / "dashboard.tsx"
                    dashboard_path.write_text(
                        EnhancedFrontendSkill.generate_dashboard_page_from_spec(spec),
                        encoding='utf-8'
                    )
                    print(f"    [GENERATED] dashboard.tsx (Page)")
                    self.generated_files.append(str(dashboard_path))

                if "registration" in spec['description'].lower():
                    register_path = pages_dir / "register.tsx"
                    register_path.write_text(
                        EnhancedFrontendSkill.generate_user_registration_page_from_spec(spec),
                        encoding='utf-8'
                    )
                    print(f"    [GENERATED] register.tsx (Page)")
                    self.generated_files.append(str(register_path))

    def _generate_database_code(self):
        """Generate database migrations from subtask MD files."""
        if not self.database_dir.exists():
            print("  [SKIP] Database subtasks directory not found")
            return

        project_folder = Path("dbadmin/calendar_app")
        migrations_dir = project_folder / "migrations"
        migrations_dir.mkdir(parents=True, exist_ok=True)

        version = 1

        for md_file in sorted(self.database_dir.glob("*.md")):
            if md_file.name in ["README.md", "project_summary.md"]:
                continue

            spec = EnhancedDatabaseSkill.parse_readme(str(md_file))
            if not spec or not spec.get("title"):
                continue

            print(f"\n  [{md_file.stem}]")
            print(f"    Title: {spec['title']}")
            print(f"    Description: {spec['description'][:70]}...")

            if "user" in spec['description'].lower():
                migration_path = migrations_dir / f"V{version:03d}_create_users_table.sql"
                migration_path.write_text(
                    EnhancedDatabaseSkill.generate_user_migration_from_spec(spec),
                    encoding='utf-8'
                )
                print(f"    [GENERATED] V{version:03d}_create_users_table.sql")
                self.generated_files.append(str(migration_path))
                version += 1

            if "audit" in spec['description'].lower():
                migration_path = migrations_dir / f"V{version:03d}_create_audit_logs_table.sql"
                migration_path.write_text(
                    EnhancedDatabaseSkill.generate_audit_logs_migration_from_spec(spec),
                    encoding='utf-8'
                )
                print(f"    [GENERATED] V{version:03d}_create_audit_logs_table.sql")
                self.generated_files.append(str(migration_path))
                version += 1

            if "activity" in spec['description'].lower():
                migration_path = migrations_dir / f"V{version:03d}_create_activity_logs_table.sql"
                migration_path.write_text(
                    EnhancedDatabaseSkill.generate_activity_logs_migration_from_spec(spec),
                    encoding='utf-8'
                )
                print(f"    [GENERATED] V{version:03d}_create_activity_logs_table.sql")
                self.generated_files.append(str(migration_path))
                version += 1

            if "session" in spec['description'].lower():
                migration_path = migrations_dir / f"V{version:03d}_create_sessions_table.sql"
                migration_path.write_text(
                    EnhancedDatabaseSkill.generate_sessions_migration_from_spec(spec),
                    encoding='utf-8'
                )
                print(f"    [GENERATED] V{version:03d}_create_sessions_table.sql")
                self.generated_files.append(str(migration_path))
                version += 1

            if "integration" in spec['description'].lower():
                migration_path = migrations_dir / f"V{version:03d}_create_integration_tables.sql"
                migration_path.write_text(
                    EnhancedDatabaseSkill.generate_integration_tables_migration_from_spec(spec),
                    encoding='utf-8'
                )
                print(f"    [GENERATED] V{version:03d}_create_integration_tables.sql")
                self.generated_files.append(str(migration_path))
                version += 1

    def _generate_user_entity(self, project_folder, base_package, spec):
        """Generate User entity."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)

        entity_path = entity_dir / "User.java"
        entity_path.write_text(
            EnhancedBackendSkill.generate_user_entity_from_spec(spec),
            encoding='utf-8'
        )
        self.generated_files.append(str(entity_path))

    def _generate_user_repository(self, project_folder, base_package, spec):
        """Generate User repository."""
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
        repo_dir.mkdir(parents=True, exist_ok=True)

        # Generate simple repository interface
        repo_code = """package com.example.calendarapp.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.example.calendarapp.entity.User;
import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    Page<User> findByActiveTrue(Pageable pageable);
}
"""
        repo_path = repo_dir / "UserRepository.java"
        repo_path.write_text(repo_code, encoding='utf-8')
        self.generated_files.append(str(repo_path))

    def _generate_user_service(self, project_folder, base_package, spec):
        """Generate User service."""
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)

        service_path = service_dir / "UserService.java"
        service_path.write_text(
            EnhancedBackendSkill.generate_user_service_from_spec(spec),
            encoding='utf-8'
        )
        self.generated_files.append(str(service_path))

    def _generate_audit_service(self, project_folder, base_package, spec):
        """Generate Audit service."""
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)

        service_path = service_dir / "AuditService.java"
        service_path.write_text(
            EnhancedBackendSkill.generate_audit_service_from_spec(spec),
            encoding='utf-8'
        )
        self.generated_files.append(str(service_path))

    def _generate_jwt_provider(self, project_folder, base_package, spec):
        """Generate JWT token provider."""
        security_dir = project_folder / f"src/main/java/com/example/{base_package}/security"
        security_dir.mkdir(parents=True, exist_ok=True)

        jwt_path = security_dir / "JwtTokenProvider.java"
        jwt_path.write_text(
            EnhancedBackendSkill.generate_jwt_util_from_spec(spec),
            encoding='utf-8'
        )
        self.generated_files.append(str(jwt_path))

    def _generate_user_controller(self, project_folder, base_package, spec):
        """Generate User controller."""
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        controller_dir.mkdir(parents=True, exist_ok=True)

        controller_path = controller_dir / "UserController.java"
        controller_path.write_text(
            EnhancedBackendSkill.generate_user_controller_from_spec(spec),
            encoding='utf-8'
        )
        self.generated_files.append(str(controller_path))

    def _extract_business_process(self, title: str) -> str:
        """Extract business process from title."""
        return title.split(" - ")[1] if " - " in title else ""

    def _print_summary(self):
        """Print generation summary."""
        print("\n" + "="*70)
        print("GENERATION SUMMARY")
        print("="*70)
        print(f"\nTotal files generated: {len(self.generated_files)}")
        print("\nGenerated files:")
        for file_path in self.generated_files:
            rel_path = Path(file_path).relative_to(Path.cwd()) if Path(file_path).is_absolute() else file_path
            print(f"  [OK] {rel_path}")

        print("\n" + "="*70)
        print("[SUCCESS] Code generation from subtask specifications complete!")
        print("="*70 + "\n")


if __name__ == "__main__":
    generator = SubtaskCodeGenerator()
    generator.generate_all()

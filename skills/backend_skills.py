"""Backend Skills - Specialized capabilities for backend development."""


class BackendSkill:
    """Skills for backend development."""

    name = "backend"
    description = "Backend architecture, API design, and database planning"

    COMMON_ARCHITECTURES = [
        "REST API",
        "GraphQL API",
        "WebSocket API",
        "gRPC Service",
    ]

    COMMON_FRAMEWORKS = [
        "Django",
        "FastAPI",
        "Flask",
        "Node.js/Express",
        "Go/Gin",
        "Rust/Actix",
    ]

    @staticmethod
    def design_api_endpoints(feature: str) -> list:
        """Design API endpoints for a feature."""
        base_resource = feature.lower().replace(" ", "_")
        return [
            f"POST /api/v1/{base_resource}",
            f"GET /api/v1/{base_resource}",
            f"GET /api/v1/{base_resource}/{{id}}",
            f"PUT /api/v1/{base_resource}/{{id}}",
            f"DELETE /api/v1/{base_resource}/{{id}}",
        ]

    @staticmethod
    def design_database_schema(entity: str) -> dict:
        """Design database schema for an entity."""
        return {
            "table_name": entity.lower() + "s",
            "fields": [
                {"name": "id", "type": "UUID", "primary_key": True},
                {"name": "created_at", "type": "TIMESTAMP", "default": "now()"},
                {"name": "updated_at", "type": "TIMESTAMP", "default": "now()"},
                {"name": "data", "type": "JSON"},
            ],
            "indexes": [
                f"idx_{entity.lower()}_created_at",
                f"idx_{entity.lower()}_updated_at",
            ],
        }

    @staticmethod
    def generate_authentication_flow() -> str:
        """Generate authentication flow documentation."""
        return (
            "## Authentication Flow\n\n"
            "1. User logs in with credentials\n"
            "2. Backend validates credentials\n"
            "3. Backend generates JWT token\n"
            "4. Token is returned to client\n"
            "5. Client includes token in subsequent requests\n"
            "6. Backend validates token on each request\n"
        )

    @staticmethod
    def suggest_middleware() -> list:
        """Suggest middleware for backend."""
        return [
            "Authentication Middleware",
            "CORS Middleware",
            "Request Logging Middleware",
            "Error Handling Middleware",
            "Rate Limiting Middleware",
            "Request Validation Middleware",
        ]

    @staticmethod
    def generate_implementation_checklist(feature: str) -> list:
        """Generate implementation checklist for a feature."""
        return [
            f"Design API endpoints for {feature}",
            f"Design database schema for {feature}",
            f"Implement authentication/authorization",
            f"Implement API endpoints",
            f"Implement database queries",
            f"Implement error handling",
            f"Add input validation",
            f"Add logging",
            f"Write unit tests",
            f"Write integration tests",
        ]

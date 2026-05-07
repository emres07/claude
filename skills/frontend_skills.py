"""Frontend Skills - Specialized capabilities for frontend development."""


class FrontendSkill:
    """Skills for frontend development."""

    name = "frontend"
    description = "UI/UX design, component architecture, state management"

    COMMON_FRAMEWORKS = [
        "React",
        "Vue.js",
        "Angular",
        "Svelte",
        "Next.js",
        "Nuxt.js",
    ]

    COMMON_UI_FRAMEWORKS = [
        "Tailwind CSS",
        "Bootstrap",
        "Material UI",
        "Ant Design",
        "Chakra UI",
    ]

    @staticmethod
    def design_component_hierarchy(feature: str) -> dict:
        """Design component hierarchy for a feature."""
        return {
            "parent_component": f"{feature}Container",
            "children": [
                f"{feature}Header",
                f"{feature}Content",
                f"{feature}Footer",
            ],
            "shared_components": [
                "Button",
                "Form",
                "Card",
                "Modal",
            ],
        }

    @staticmethod
    def design_pages(feature: str) -> list:
        """Design pages for a feature."""
        base_name = feature.lower().replace(" ", "-")
        return [
            {
                "name": f"{base_name}-list",
                "path": f"/{base_name}",
                "description": f"List all {feature}",
            },
            {
                "name": f"{base_name}-detail",
                "path": f"/{base_name}/{{id}}",
                "description": f"View {feature} details",
            },
            {
                "name": f"{base_name}-create",
                "path": f"/{base_name}/create",
                "description": f"Create new {feature}",
            },
            {
                "name": f"{base_name}-edit",
                "path": f"/{base_name}/{{id}}/edit",
                "description": f"Edit {feature}",
            },
        ]

    @staticmethod
    def suggest_state_management() -> list:
        """Suggest state management solutions."""
        return [
            "Redux",
            "Zustand",
            "Jotai",
            "Recoil",
            "Context API",
            "MobX",
        ]

    @staticmethod
    def generate_responsive_breakpoints() -> dict:
        """Generate responsive design breakpoints."""
        return {
            "mobile": "0px - 640px",
            "tablet": "641px - 1024px",
            "desktop": "1025px+",
            "breakpoints": {
                "sm": "640px",
                "md": "1024px",
                "lg": "1280px",
                "xl": "1536px",
            },
        }

    @staticmethod
    def generate_accessibility_checklist() -> list:
        """Generate accessibility checklist."""
        return [
            "[ ] Semantic HTML used",
            "[ ] ARIA labels added",
            "[ ] Keyboard navigation works",
            "[ ] Color contrast sufficient",
            "[ ] Focus indicators visible",
            "[ ] Screen reader compatible",
            "[ ] Touch targets adequate",
            "[ ] Mobile responsive",
        ]

    @staticmethod
    def generate_implementation_checklist(feature: str) -> list:
        """Generate implementation checklist for a feature."""
        return [
            f"Design component hierarchy for {feature}",
            f"Create {feature} pages",
            f"Implement components",
            f"Set up state management",
            f"Connect to backend APIs",
            f"Implement forms and validation",
            f"Add responsive design",
            f"Implement error handling",
            f"Write component tests",
            f"Test accessibility",
            f"Performance optimization",
        ]

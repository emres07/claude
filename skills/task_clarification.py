"""Task Clarification Skill - Used to clarify ambiguous requirements."""


class TaskClarificationSkill:
    """Skill for clarifying task descriptions and requirements."""

    name = "task_clarification"
    description = "Clarifies ambiguous task descriptions and requirements"

    @staticmethod
    def analyze_clarity(task_description: str) -> dict:
        """Analyze clarity of a task description."""
        issues = []

        if len(task_description.strip()) < 20:
            issues.append("Description too brief")

        if "?" in task_description and task_description.count("?") > 3:
            issues.append("Too many open questions")

        if any(
            word in task_description.lower()
            for word in ["vague", "unclear", "sometime", "maybe", "perhaps"]
        ):
            issues.append("Ambiguous language detected")

        return {
            "is_clear": len(issues) == 0,
            "issues": issues,
            "confidence": max(0, 100 - (len(issues) * 25)),
        }

    @staticmethod
    def suggest_clarifications(task_description: str) -> list:
        """Suggest clarifications for a task."""
        suggestions = []

        if len(task_description.split()) < 50:
            suggestions.append("Add more detailed description of requirements")

        if "acceptance criteria" not in task_description.lower():
            suggestions.append("Define clear acceptance criteria")

        if "timeline" not in task_description.lower():
            suggestions.append("Specify expected timeline")

        return suggestions

    @staticmethod
    def generate_clarification_template(title: str) -> str:
        """Generate a clarification template for a task."""
        return (
            f"# Clarification for: {title}\n\n"
            f"## What is the main goal?\n"
            f"[Clarify the primary objective]\n\n"
            f"## What are the constraints?\n"
            f"[List any constraints or limitations]\n\n"
            f"## What are the acceptance criteria?\n"
            f"- [ ] Criterion 1\n"
            f"- [ ] Criterion 2\n\n"
            f"## What dependencies exist?\n"
            f"[List any related tasks or dependencies]\n\n"
            f"## What is the expected timeline?\n"
            f"[Specify timeline expectations]\n"
        )

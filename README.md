# Multi-Agent Task Management System

A sophisticated Claude Code project featuring a team of four specialized agents that collaborate to create and manage tasks across backend, frontend, and database domains.

## Quick Start

### 1. Setup

```bash
# Clone or navigate to the project
cd "path/to/New folder"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your Claude API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Run the Agent Team

```bash
# Run with default configuration
python main.py

# Run with GitHub publishing ready
python main.py --publish

# Run with specific GitHub repo
python main.py --github-repo https://github.com/yourusername/your-repo.git
```

## Project Structure

```
.
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Base agent class
│   ├── task_creator.py         # Creates main tasks
│   ├── backend_agent.py        # Backend development
│   ├── frontend_agent.py       # Frontend development
│   └── database_agent.py       # Database development
├── skills/                      # Specialized skills
│   ├── __init__.py
│   ├── task_clarification.py   # Task clarification skill
│   ├── backend_skills.py       # Backend-specific skills
│   ├── frontend_skills.py      # Frontend-specific skills
│   └── database_skills.py      # Database-specific skills
├── tasks/                       # Generated tasks
│   └── .gitkeep
├── subtasks/                    # Generated subtasks
│   ├── backend/
│   ├── frontend/
│   └── database/
├── agent_team_config.json      # Team configuration
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── CLAUDE.md                    # Project documentation
└── README.md                    # This file
```

## How It Works

### Agent Team Workflow

1. **Task Creator Agent** → Creates main tasks from requirements
2. **Backend Agent** → Generates backend subtasks
3. **Frontend Agent** → Generates frontend subtasks  
4. **Database Agent** → Generates database subtasks + manages organization

### Skill System

Each agent has specialized skills:

- **Backend**: API design, database schema planning, authentication
- **Frontend**: UI/UX design, component architecture, state management
- **Database**: Schema design, query optimization, monitoring setup
- **Clarification**: Ambiguity detection and task refinement

## Agents

### Task Creator Agent
- Creates main tasks from project requirements
- Distributes work to specialized agents
- Manages task scope and priority

### Backend Agent
- Designs REST/GraphQL APIs
- Plans database schemas
- Suggests middleware and authentication flows
- Generates implementation checklists

### Frontend Agent
- Designs component hierarchies
- Plans page structures
- Recommends state management solutions
- Provides accessibility and responsive design checklists

### Database Agent
- Designs normalized schemas
- Plans indexes and optimization strategies
- Creates migration templates
- Manages backup and recovery procedures
- **Bonus**: Clarifies ambiguous tasks and organizes all outputs

## Features

✨ **Multi-Agent Collaboration**
- Agents work independently but coordinate through a central orchestrator
- Each agent focuses on their domain expertise

🎯 **Skill-Based Execution**
- Skills are modular and reusable
- Each agent has specialized skills matching their role

📁 **Organized Output**
- Tasks and subtasks saved as Markdown files
- Clear folder structure for different domains
- Project summary for quick overview

🔗 **GitHub Ready**
- Easy publishing to GitHub repositories
- Automatic commit preparation
- Full version control integration

## Configuration

Edit `agent_team_config.json` to customize:
- Agent models and priorities
- Task flow and collaboration strategy
- GitHub integration settings
- Clarification triggers

## Example Usage

### Create a Single Task

```python
from agents import TaskCreatorAgent

creator = TaskCreatorAgent()
task = creator.create_main_task(
    title="Add Payment Processing",
    description="Implement Stripe payment integration",
    priority="high",
    domains=["backend", "frontend", "database"]
)

creator.save_task(task)
```

### Generate Backend Subtasks

```python
from agents import BackendAgent

backend = BackendAgent()
subtasks = backend.create_subtasks_from_task(
    task_id="add_payment_processing",
    task_title="Add Payment Processing"
)

for subtask in subtasks:
    backend.save_subtask(subtask)
```

## Output Examples

### Main Task File

```markdown
# Add Payment Processing

**Created by**: Task Creator Agent
**Date**: 2026-05-07 10:30:00

## Description
Implement Stripe payment integration with support for cards and digital wallets.

## Priority
HIGH

## Domains
- backend
- frontend
- database

## Acceptance Criteria
- [ ] Stripe account setup
- [ ] Payment API integration
- [ ] Webhook handling
- [ ] UI implementation
- [ ] Testing complete
```

### Subtask File

```markdown
# Backend API Implementation - Add Payment Processing

**Created by**: Backend Agent

## Domain
Backend

## Parent Task
add_payment_processing

## APIs to Implement
- POST /api/v1/payments
- GET /api/v1/payments/{id}
- POST /api/v1/payments/{id}/refund

## Acceptance Criteria
- [ ] API endpoints implemented
- [ ] Database integration complete
- [ ] Error handling implemented
```

## Requirements

- Python 3.8+
- Claude API access
- Git (for GitHub integration)

## GitHub Integration

### Setup

```bash
git init
git add .
git commit -m "Initial agent team setup"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### Auto-Update

Tasks and subtasks are automatically ready to commit:

```bash
git add tasks/ subtasks/
git commit -m "Auto-generated tasks and subtasks from agent team"
git push
```

## Customization

### Add New Skills

Create a new skill file in `skills/`:

```python
class CustomSkill:
    name = "custom"
    description = "Custom skill description"
    
    @staticmethod
    def custom_method():
        pass
```

### Extend Agents

Subclass base agents and add custom methods:

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="custom",
            name="Custom Agent",
            role="custom_role",
            output_folder="custom_output"
        )
```

## Environment Variables

Create `.env`:

```env
ANTHROPIC_API_KEY=sk-...
DEBUG=false
LOG_LEVEL=INFO
```

## Troubleshooting

### Agents not creating files
- Check that folder permissions allow writing
- Ensure output folders exist
- Check Python path and imports

### GitHub push fails
- Verify GitHub credentials are configured
- Check repository exists and is accessible
- Ensure `.gitignore` is configured properly

## Next Steps

1. ✅ Run the sample task: `python main.py`
2. 📝 Review generated tasks in `tasks/` and `subtasks/`
3. 🔧 Customize `agent_team_config.json`
4. 🚀 Push to GitHub: `git push origin main`

## License

This project is open source and available for educational and commercial use.

## Support

For issues and questions:
- Check CLAUDE.md for detailed documentation
- Review agent implementations for examples
- Check skills for available capabilities

Happy task creation! 🚀

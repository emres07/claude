# Claude Code Multi-Agent Project Management System

## Overview
This project implements a multi-agent team system for task and subtask management. Four specialized agents collaborate to create, clarify, and organize tasks across backend, frontend, and database development domains.

## Project Structure

```
.
├── agents/
│   ├── __init__.py
│   ├── task_creator.py          # Creates main tasks
│   ├── backend_agent.py         # Creates backend subtasks
│   ├── frontend_agent.py        # Creates frontend subtasks
│   └── database_agent.py        # Creates database subtasks & organizes files
├── skills/
│   ├── __init__.py
│   ├── task_clarification.py    # Skill for clarifying task descriptions
│   ├── backend_skills.py        # Backend-specific skills
│   ├── frontend_skills.py       # Frontend-specific skills
│   └── database_skills.py       # Database-specific skills
├── tasks/
│   └── .gitkeep
├── subtasks/
│   ├── backend/
│   ├── frontend/
│   └── database/
├── agent_team_config.json       # Agent team configuration
├── main.py                      # Entry point for agent team
└── README.md                    # Project documentation

```

## Agent Team

### 1. Task Creator Agent
- **Purpose**: Creates main tasks from project requirements
- **Skills**: Task definition, scope management
- **Output**: Task files in `tasks/` folder

### 2. Backend Agent
- **Purpose**: Creates backend subtasks and implementation plans
- **Skills**: Backend architecture, API design, database schema planning
- **Output**: Backend subtask files in `subtasks/backend/`

### 3. Frontend Agent
- **Purpose**: Creates frontend subtasks and UI implementation plans
- **Skills**: UI/UX design, component structure, state management
- **Output**: Frontend subtask files in `subtasks/frontend/`

### 4. Database Agent
- **Purpose**: Creates database subtasks and organizes all outputs
- **Skills**: Database design, query optimization, schema design
- **Extra**: Clarifies task descriptions, manages file organization
- **Output**: Database subtask files in `subtasks/database/`, publishes to GitHub

## How Agent Team Works

1. **Task Creation**: Task Creator Agent generates main tasks
2. **Subtask Generation**: Each specialized agent creates domain-specific subtasks
3. **Clarification**: Database Agent clarifies ambiguous task descriptions
4. **Organization**: All tasks/subtasks organized and saved to respective folders
5. **Publishing**: Ready for GitHub repository sync

## Configuration

### Enable Agent Team Experimental
To use the experimental agent team features, ensure `settings.json` has:
```json
{
  "agent_team": {
    "enabled": true,
    "experimental": true
  }
}
```

## Skills System

Each agent has specialized skills that define their capabilities:

- **Task Clarification Skill**: Understanding and clarifying ambiguous requirements
- **Backend Skills**: API design, authentication, database integration
- **Frontend Skills**: Component design, state management, UI patterns
- **Database Skills**: Schema design, query optimization, data modeling

## Usage

### Create a Task
```python
from agents.task_creator import TaskCreatorAgent

creator = TaskCreatorAgent()
task = creator.create_task(
    title="New Feature Implementation",
    description="Implement user authentication system",
    priority="high"
)
```

### Generate Subtasks
```python
from agents.backend_agent import BackendAgent

backend = BackendAgent()
subtasks = backend.create_subtasks(task)
```

## Output Format

### Task Files (tasks/)
```markdown
# Task: [Task Title]

## Description
[Detailed description]

## Priority
[high/medium/low]

## Status
[pending/in_progress/completed]

## Related Subtasks
- [Link to subtask]
```

### Subtask Files (subtasks/{domain}/)
```markdown
# Subtask: [Subtask Title]

## Domain
[backend/frontend/database]

## Task ID
[Parent task ID]

## Description
[Implementation details]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Status
[pending/in_progress/completed]
```

## GitHub Integration

Tasks and subtasks can be published directly to your GitHub repository:

```bash
python main.py --publish-to-github --repo [your-repo-url]
```

## Requirements
- Python 3.8+
- Claude API access (for agent functionality)
- Git (for GitHub integration)

## Getting Started

1. Initialize git repository: `git init`
2. Configure agent team: Edit `agent_team_config.json`
3. Run agents: `python main.py`
4. Review generated tasks in `tasks/` and `subtasks/` folders
5. Publish to GitHub

## Notes

- Each agent operates independently but coordinates through the agent team manager
- Skills are modular and can be extended per agent
- Task/subtask structure follows standard conventions for tool integration
- All outputs are stored as Markdown files for easy version control

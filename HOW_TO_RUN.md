# How to Run Agents with Projects

This guide explains how to run the multi-agent team to process your projects.

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

## Running Agents

### Option 1: Use Sample Projects (Easiest) ⭐

```bash
python main.py --sample
```

**What it does:**
- Loads 2 pre-built sample projects
- All agents process each project
- Creates tasks and subtasks in respective folders
- Shows real-time progress

**Output:**
```
✓ Using sample projects

==================================================================
🚀 STARTING AGENT TEAM PROCESSING FOR 2 PROJECT(S)
==================================================================

==============================================================
Processing Project: User Authentication System
Priority: HIGH
==============================================================

📋 Task Creator Agent is working...
  ✓ Main task created: User Authentication System

🔍 Database Agent is clarifying requirements...
  ✓ Task requirements clarified

🔧 Backend Agent is creating subtasks...
  ✓ Backend API Implementation - User Authentication System
  ✓ Database Schema - User Authentication System

🎨 Frontend Agent is creating subtasks...
  ✓ UI Components - User Authentication System
  ✓ Pages - User Authentication System

💾 Database Agent is creating subtasks...
  ✓ Database Schema - User Authentication System
  ✓ Query Optimization - User Authentication System
```

### Option 2: Use projects.json File

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
    "name": "My First Project",
    "description": "Project description here",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  },
  {
    "name": "My Second Project",
    "description": "Another project",
    "priority": "medium",
    "domains": ["backend", "frontend"]
  }
]
```

### Option 3: Add Project via Command Line

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
# Simple project
python main.py --add-project "User Login" --description "Add login feature"

# High priority project with specific domains
python main.py --add-project "API Integration" --description "Connect to external API" --priority high --domains backend,database

# Frontend only project
python main.py --add-project "Dark Mode" --description "Add dark theme" --priority medium --domains frontend
```

## What Happens When You Run

### Agent Workflow

For **each project**, the agents work in this order:

1. **📋 Task Creator Agent**
   - Creates a main task from the project
   - Saves it to `tasks/` folder

2. **🔍 Database Agent**
   - Clarifies ambiguous requirements
   - Validates task description

3. **🔧 Backend Agent** (if in domains)
   - Creates backend subtasks
   - Designs APIs and database schemas
   - Saves to `subtasks/backend/`

4. **🎨 Frontend Agent** (if in domains)
   - Creates frontend subtasks
   - Designs UI components and pages
   - Saves to `subtasks/frontend/`

5. **💾 Database Agent** (if in domains)
   - Creates database subtasks
   - Designs schemas and optimization
   - Saves to `subtasks/database/`

### Output Structure

```
tasks/
├── user_authentication_system_main.md
├── payment_processing_integration_main.md
└── ...

subtasks/
├── backend/
│   ├── user_authentication_system_backend_api_implementation.md
│   ├── user_authentication_system_database_schema.md
│   └── ...
├── frontend/
│   ├── user_authentication_system_ui_components.md
│   ├── user_authentication_system_pages.md
│   └── ...
└── database/
    ├── user_authentication_system_database_schema.md
    ├── user_authentication_system_query_optimization.md
    └── ...
```

## Publishing to GitHub

### Prepare for GitHub Publish

```bash
# Prepare without pushing
python main.py --sample --publish

# Prepare with GitHub repo URL
python main.py --sample --publish --github-repo https://github.com/yourusername/your-repo.git
```

### Push to GitHub

Once agents have processed projects:

```bash
# Stage all generated files
git add tasks/ subtasks/

# Commit with auto-generated message
git commit -m "Auto-generated tasks and subtasks from agent team"

# Add remote (if not already added)
git remote add origin https://github.com/yourusername/your-repo.git

# Push to GitHub
git push -u origin main
```

## Advanced Usage

### Process Multiple Projects with GitHub

```bash
python main.py --projects projects.json --publish --github-repo https://github.com/yourusername/repo.git
```

### Use Custom Configuration

```bash
python main.py --config my-config.json --projects my-projects.json
```

### Check Current Projects

View `projects.json` to see all available projects:

```bash
# Windows
type projects.json

# Mac/Linux
cat projects.json
```

## Troubleshooting

### API Key Issues

**Error:** `Missing ANTHROPIC_API_KEY`

**Solution:**
```bash
# Create .env file
echo ANTHROPIC_API_KEY=sk-your-key-here > .env

# Or set as environment variable
$env:ANTHROPIC_API_KEY="sk-your-key-here"  # PowerShell
export ANTHROPIC_API_KEY="sk-your-key-here"  # Bash
```

### No Projects Found

**Error:** `No projects to process!`

**Solution:**
- Use `--sample` flag: `python main.py --sample`
- Or create `projects.json` with project definitions
- Or use `--add-project` flag

### Permission Issues

**Error:** `Permission denied` when writing files

**Solution:**
- Ensure folders have write permissions
- Try running as administrator (Windows)
- Check that `tasks/` and `subtasks/` folders exist

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'agents'`

**Solution:**
```bash
# Ensure you're in the correct directory
cd "c:\DEV\CLAUDE_PROJECTS\New folder"

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

## Real-World Examples

### Example 1: Process Sample Projects

```bash
python main.py --sample
```

### Example 2: Process Your Own Projects

```bash
# 1. Edit projects.json with your projects
# 2. Run with projects
python main.py --projects projects.json

# 3. Review generated tasks in tasks/ and subtasks/
# 4. Push to GitHub
git add .
git commit -m "Agent team generated tasks"
git push origin main
```

### Example 3: Add Single Project and Process

```bash
python main.py --add-project "Email Notifications" --description "Add email notification system" --priority high
```

### Example 4: Process Backend-Only Project

```bash
python main.py --add-project "API Documentation" --description "Create API documentation" --domains backend --priority medium
```

## Understanding Agent Output

Each task file contains:

```markdown
# Task Title

**Created by**: [Agent Name]
**Agent Role**: [Agent Role]
**Date**: [Creation Date]
**Agent ID**: [Agent ID]

## Description
[Project description]

## Priority
[HIGH/MEDIUM/LOW]

## Domains
- backend
- frontend
- database

## Subtasks
- [backend] Task 1
- [frontend] Task 2
- [database] Task 3

## Status
pending
```

Subtask files contain detailed implementation info:
- APIs to implement (backend)
- Components to build (frontend)
- Schemas to design (database)
- Acceptance criteria for each

## Next Steps

1. ✅ Run agents: `python main.py --sample`
2. 📁 Check output in `tasks/` and `subtasks/`
3. 📝 Edit `projects.json` with your projects
4. 🔄 Re-run agents: `python main.py --projects projects.json`
5. 🚀 Push to GitHub: `git push origin main`

## Tips

- **Start simple**: Use `--sample` first to understand the workflow
- **Review output**: Check generated files to understand task structure
- **Iterate**: Edit projects.json and re-run to refine tasks
- **Version control**: Commit frequently as tasks evolve
- **Team sync**: Share GitHub repo with team to review generated tasks

## Need Help?

- Check CLAUDE.md for detailed documentation
- Review agent source code in `agents/` folder
- Check skills in `skills/` folder for available capabilities
- Read the generated task files for examples

---

Happy task management! 🚀

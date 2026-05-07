# Quick Start Guide

## ⚡ 5-Minute Setup

```bash
# 1. Navigate to project
cd "c:\DEV\CLAUDE_PROJECTS\New folder"

# 2. Activate environment (if needed)
venv\Scripts\activate

# 3. Run with sample projects
python main.py --sample
```

That's it! ✨

## 📊 Common Commands

### Run with Sample Projects (Recommended Start)
```bash
python main.py --sample
```

### Use Your Own Projects File
```bash
python main.py --projects projects.json
```

### Add Single Project
```bash
python main.py --add-project "Feature Name" --description "Feature description"
```

### Publish to GitHub
```bash
python main.py --sample --publish --github-repo https://github.com/user/repo.git
```

## 🎯 How It Works

```
Your Project(s)
       ↓
   ┌───┴───┬─────────┬─────────┐
   ↓       ↓         ↓         ↓
Backend  Frontend  Database  Clarify
Agent    Agent     Agent     Descriptions
   ↓       ↓         ↓         ↓
   └───┬───┴────┬────┴─────────┘
       ↓        ↓
    tasks/   subtasks/
       ↓        ↓
   Tasks    Backend/Frontend/Database
            Subtasks
       ↓
     GitHub
```

## 📁 What Gets Created

```
tasks/                          → Main project tasks
subtasks/
  ├── backend/                 → Backend implementation tasks
  ├── frontend/                → Frontend UI/UX tasks
  └── database/                → Database design tasks
```

## 🔧 Each Agent Does This

| Agent | Creates | Saves To |
|-------|---------|----------|
| **Task Creator** | Main tasks from projects | `tasks/` |
| **Backend** | API & database subtasks | `subtasks/backend/` |
| **Frontend** | UI & component subtasks | `subtasks/frontend/` |
| **Database** | Schema & optimization subtasks | `subtasks/database/` |

*Database Agent also clarifies requirements and organizes all outputs*

## 🎬 Example Run

```bash
# Run with sample projects
$ python main.py --sample

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

✅ Project 'User Authentication System' processing complete!

[... repeats for other projects ...]
```

## 📝 Edit projects.json

```json
[
  {
    "name": "Your Project Name",
    "description": "What your project does",
    "priority": "high",
    "domains": ["backend", "frontend", "database"]
  }
]
```

## 🚀 Push to GitHub

```bash
# After running agents
git add tasks/ subtasks/
git commit -m "Auto-generated tasks and subtasks"
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

## ❓ Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run: `pip install -r requirements.txt` |
| `ANTHROPIC_API_KEY not found` | Create `.env` with `ANTHROPIC_API_KEY=your_key` |
| `No projects to process` | Run: `python main.py --sample` |
| `Permission denied` | Ensure write access to folders |

## 📚 Next Steps

1. **Start**: `python main.py --sample`
2. **Review**: Check `tasks/` and `subtasks/` folders
3. **Customize**: Edit `projects.json`
4. **Run again**: `python main.py --projects projects.json`
5. **Share**: Push to GitHub

## 🔗 Quick Links

- **Setup Details**: See `HOW_TO_RUN.md`
- **Full Documentation**: See `CLAUDE.md`
- **Full README**: See `README.md`
- **Agent Code**: See `agents/` folder
- **Skills**: See `skills/` folder

---

**All ready!** Run `python main.py --sample` to see agents in action 🚀

# 🖥️ Tmux Agent Monitoring Guide

Real-time monitoring of agent team work in separate terminal panes.

## Installation

### Linux/Mac
```bash
# Ubuntu/Debian
sudo apt-get install tmux

# macOS
brew install tmux
```

### Windows
```bash
# Using Chocolatey
choco install tmux

# Or using Windows Terminal with WSL2
# Run the Linux commands in your WSL terminal
```

## Quick Start

### 1. Run with Projects File
```bash
python run_with_tmux.py --projects projects.json
```

### 2. Run Interactive Mode
```bash
python run_with_tmux.py --interactive
```

### 3. Attach to Session
```bash
tmux attach-session -t agent_team
```

Or automatically attach after starting:
```bash
python run_with_tmux.py --projects projects.json --attach
```

## Tmux Layout

When you attach to the session, you'll see 5 panes:

```
┌─────────────────────────┬─────────────────────────┐
│                         │                         │
│   Orchestrator          │   Task Creator          │
│   (Main Execution)      │   (Task Creation)       │
│                         │                         │
├─────────────────────────┼─────────────────────────┤
│                         │                         │
│   Backend Agent         │   Frontend Agent        │
│   (Java/Spring)         │   (React/Next.js)       │
│                         │                         │
├─────────────────────────┴─────────────────────────┤
│                                                   │
│   Database Agent                                  │
│   (Oracle/PL-SQL)                                 │
│                                                   │
└───────────────────────────────────────────────────┘
```

## Tmux Commands

### Attach/Detach
```bash
# Attach to session
tmux attach-session -t agent_team

# Detach (while inside tmux)
Ctrl+B → D
```

### Navigate Panes
```bash
# Move between panes
Ctrl+B → ← → ↑ ↓      (Arrow keys)
Ctrl+B → o             (Cycle through panes)

# Go to specific pane
Ctrl+B → 0             (First pane)
Ctrl+B → 1             (Second pane)
Ctrl+B → ;             (Last active pane)
```

### View/Control Panes
```bash
# Zoom pane (view full screen)
Ctrl+B → Z

# Kill current pane
Ctrl+B → X

# Resize pane
Ctrl+B → : resize-pane -D 10   (Down 10 lines)
```

### Scrolling & Search
```bash
# Enter scroll mode
Ctrl+B → [

# In scroll mode:
# - Arrow keys or Page Up/Down to scroll
# - / to search
# - n to find next
# - Escape to exit

# Exit scroll mode
Ctrl+B → ]
```

## Session Management

### List Sessions
```bash
tmux list-sessions
```

### List Panes in Session
```bash
tmux list-panes -t agent_team -a
```

### Kill Session
```bash
# Option 1: Command line
tmux kill-session -t agent_team

# Option 2: Using Python script
python run_with_tmux.py --kill
```

### Rename Pane
```bash
Ctrl+B → ,    (Then type new name)
```

## View Logs

### View All Logs
```bash
python run_with_tmux.py --logs
```

### View Specific Agent Log
```bash
tail -f .agent_logs/backend_agent.log
tail -f .agent_logs/frontend_agent.log
tail -f .agent_logs/database_agent.log
tail -f .agent_logs/task_creator.log
tail -f .agent_logs/orchestrator.log
```

### Follow Log in Real-time
```bash
# Watch backend agent work
watch -n 1 'tail -20 .agent_logs/backend_agent.log'

# Or just tail
tail -f .agent_logs/backend_agent.log
```

## Tips & Tricks

### 1. Create Custom Layout
```bash
# After attaching, create custom layout
Ctrl+B → Space      (Cycle through default layouts)
Ctrl+B → :
layout new-window   (Save current layout)
```

### 2. Send Command to Specific Pane
```bash
# While in tmux, you can type in each pane
# Click/navigate to pane, then type

# Or from command line
tmux send-keys -t agent_team.0 "clear" Enter
```

### 3. Copy/Paste in Tmux
```bash
# Enter copy mode
Ctrl+B → [

# Select text (use arrow keys and shift)
# Copy selection
Ctrl+B → w    (or Alt+W)

# Paste
Ctrl+B → ]
```

### 4. Split Pane Further
```bash
# Split current pane vertically
Ctrl+B → %

# Split current pane horizontally
Ctrl+B → "

# Balance all panes
Ctrl+B → =
```

## Troubleshooting

### Tmux not found
```bash
# Check if tmux is installed
which tmux

# If not installed, install it first
sudo apt-get install tmux  # Linux
brew install tmux          # macOS
```

### Session already exists
```bash
# Kill old session
tmux kill-session -t agent_team

# Or use different session name
python run_with_tmux.py --session my_agents --projects projects.json
```

### Can't see logs
```bash
# Check if log directory exists
ls -la .agent_logs/

# Check if log files have content
wc -l .agent_logs/*.log
```

### Panes not visible
```bash
# Resize terminal window
# Tmux should auto-layout

# Or manually balance panes
Ctrl+B → =
```

## Advanced Usage

### Create Custom Configuration
Create `~/.tmux.conf`:
```bash
# Mouse support
set -g mouse on

# Set color support
set -g default-terminal "screen-256color"

# Vi keybindings
setw -g mode-keys vi

# Faster escape key
set -sg escape-time 0

# Increase scrollback
set -g history-limit 10000
```

Then load it:
```bash
tmux source-file ~/.tmux.conf
```

### Monitor Multiple Sessions
```bash
# In one terminal
tmux attach-session -t agent_team

# In another terminal
watch 'tmux list-panes -t agent_team -a'
```

### Log All Output
```bash
# Capture entire pane to file
Ctrl+B → :
capture-pane -t agent_team.0 -p > pane_output.txt

# Or pipe everything to script
python run_with_tmux.py --projects projects.json 2>&1 | tee session.log
```

## Common Workflows

### Workflow 1: Monitor One Agent Closely
```bash
# Start agents
python run_with_tmux.py --projects projects.json

# In another terminal, watch specific agent
tail -f .agent_logs/backend_agent.log | grep -i error

# In tmux, zoom the backend pane
Ctrl+B → z
```

### Workflow 2: Parallel Work
```bash
# Start agents in tmux
python run_with_tmux.py --projects projects.json --attach

# While they run in background, open another terminal
# Work on next project while current runs
python run_with_tmux.py --session agents_v2 --projects projects_v2.json
```

### Workflow 3: Debug Specific Agent
```bash
# Start agents
python run_with_tmux.py --projects projects.json

# Navigate to agent pane
Ctrl+B → 1    (Frontend agent)

# Scroll up to see history
Ctrl+B → [
Ctrl+B → PageUp

# Search for errors
/error
n    (next match)
```

## Performance Notes

- Tmux runs agents in separate panes but **sequentially** in main orchestrator
- Each agent logs independently to its own file
- Logs rotate after 10MB to save space
- You can safely detach and reattach without stopping agents

---

**Enjoy monitoring your agents in real-time!** 🚀

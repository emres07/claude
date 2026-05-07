#!/usr/bin/env python3
"""
Run agent team with tmux for real-time monitoring of each agent's work.
Each agent's work is displayed in a separate tmux pane.
"""

import os
import sys
import subprocess
import time
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


class TmuxAgentMonitor:
    """Manages tmux session for agent team monitoring."""

    def __init__(self, session_name: str = "agent_team"):
        """Initialize tmux monitor."""
        self.session_name = session_name
        self.log_dir = Path(".agent_logs")
        self.log_dir.mkdir(exist_ok=True)

        # Create log files for each agent
        self.logs = {
            "task_creator": self.log_dir / "task_creator.log",
            "backend": self.log_dir / "backend_agent.log",
            "frontend": self.log_dir / "frontend_agent.log",
            "database": self.log_dir / "database_agent.log",
            "orchestrator": self.log_dir / "orchestrator.log",
        }

        for log_file in self.logs.values():
            log_file.touch()

    def check_tmux(self) -> bool:
        """Check if tmux is available."""
        try:
            subprocess.run(["tmux", "-V"], capture_output=True, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def kill_session(self) -> None:
        """Kill existing tmux session."""
        try:
            subprocess.run(
                ["tmux", "kill-session", "-t", self.session_name],
                capture_output=True
            )
        except Exception:
            pass

    def create_session(self) -> None:
        """Create tmux session with panes for each agent."""
        print(f"🚀 Creating tmux session '{self.session_name}'...")

        # Create new session with first window
        subprocess.run(
            ["tmux", "new-session", "-d", "-s", self.session_name, "-x", "240", "-y", "50",
             "-c", os.getcwd()],
            check=True
        )

        # Create panes for each agent
        panes = [
            ("Orchestrator", 0, self.logs["orchestrator"]),
            ("Task Creator", 1, self.logs["task_creator"]),
            ("Backend Agent", 1, self.logs["backend"]),
            ("Frontend Agent", 1, self.logs["frontend"]),
            ("Database Agent", 1, self.logs["database"]),
        ]

        for idx, (name, split_type, log_file) in enumerate(panes):
            if idx == 0:
                # First pane already exists, just send command
                self._send_to_pane(0, name, log_file)
            else:
                # Create new pane
                if split_type == 0:
                    subprocess.run(
                        ["tmux", "split-window", "-h", "-t", f"{self.session_name}"],
                        check=True
                    )
                else:
                    subprocess.run(
                        ["tmux", "split-window", "-v", "-t", f"{self.session_name}"],
                        check=True
                    )
                # Balance panes
                subprocess.run(
                    ["tmux", "select-layout", "-t", self.session_name, "tiled"],
                    check=True
                )
                self._send_to_pane(idx, name, log_file)

    def _send_to_pane(self, pane_idx: int, pane_name: str, log_file: Path) -> None:
        """Send initialization command to a pane."""
        pane_target = f"{self.session_name}.{pane_idx}"

        # Set pane title
        subprocess.run(
            ["tmux", "send-keys", "-t", pane_target, f"# {pane_name}", "Enter"],
            check=True
        )

        # Start tailing the log file
        time.sleep(0.5)
        subprocess.run(
            ["tmux", "send-keys", "-t", pane_target,
             f"tail -f {log_file} 2>/dev/null || echo 'Waiting for logs...'", "Enter"],
            check=True
        )

    def run_agents(self, projects_file: str = None, interactive: bool = False) -> None:
        """Run agent team with logging."""
        print("\n" + "="*70)
        print("🤖 AGENT TEAM ORCHESTRATOR")
        print("="*70 + "\n")

        # Build command
        cmd = ["python", "main.py"]

        if interactive:
            cmd.append("--interactive")
        elif projects_file:
            cmd.extend(["--projects", projects_file])
        else:
            cmd.append("--projects")
            cmd.append("projects.json")

        # Run orchestrator in main pane
        pane_target = f"{self.session_name}.0"

        log_cmd = f"{' '.join(cmd)} 2>&1 | tee {self.logs['orchestrator']}"

        print(f"📋 Running: {log_cmd}\n")

        subprocess.run(
            ["tmux", "send-keys", "-t", pane_target, log_cmd, "Enter"],
            check=True
        )

        print("✅ Agents started in tmux panes!")
        print("\n📊 Monitor Status:")
        print(f"  • Session: {self.session_name}")
        print(f"  • Logs: {self.log_dir}/")
        print(f"  • Commands:")
        print(f"    - Attach: tmux attach-session -t {self.session_name}")
        print(f"    - Kill: tmux kill-session -t {self.session_name}")
        print(f"    - List panes: tmux list-panes -t {self.session_name} -a")
        print()

    def attach(self) -> None:
        """Attach to tmux session."""
        print(f"\n📺 Attaching to session '{self.session_name}'...")
        print("   Press Ctrl+B then D to detach\n")
        time.sleep(1)

        subprocess.run(["tmux", "attach-session", "-t", self.session_name])

    def show_logs(self) -> None:
        """Show all log files."""
        print("\n" + "="*70)
        print("📋 AGENT LOGS")
        print("="*70 + "\n")

        for agent, log_file in self.logs.items():
            if log_file.exists() and log_file.stat().st_size > 0:
                print(f"\n{'─'*70}")
                print(f"📌 {agent.upper()}")
                print(f"{'─'*70}")
                try:
                    with open(log_file) as f:
                        content = f.read()
                        if content.strip():
                            print(content[-2000:])  # Last 2000 chars
                        else:
                            print("  (No logs yet)")
                except Exception as e:
                    print(f"  Error reading log: {e}")

    def start(self) -> None:
        """Start tmux monitoring."""
        if not self.check_tmux():
            print("❌ tmux is not installed!")
            print("   Install with: sudo apt-get install tmux")
            sys.exit(1)

        print("🔄 Cleaning up previous session...")
        self.kill_session()
        time.sleep(1)

        print("🛠️  Setting up tmux session...\n")
        self.create_session()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run agent team with tmux for real-time monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_with_tmux.py --projects projects.json        # Load from file
  python run_with_tmux.py --interactive                   # Interactive mode
  python run_with_tmux.py --projects projects.json --attach  # Attach after start
  python run_with_tmux.py --logs                          # Show log files

Tmux Commands:
  tmux attach-session -t agent_team    # Attach to session
  tmux kill-session -t agent_team      # Kill session
  tmux list-panes -t agent_team        # List all panes

Pane Navigation (while attached):
  Ctrl+B → Arrow keys: Navigate between panes
  Ctrl+B → Z:         Zoom pane
  Ctrl+B → X:         Kill pane
  Ctrl+B → D:         Detach session
        """,
    )

    parser.add_argument(
        "--projects",
        help="Path to projects JSON file",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode - enter project details",
    )
    parser.add_argument(
        "--session",
        default="agent_team",
        help="Tmux session name (default: agent_team)",
    )
    parser.add_argument(
        "--attach",
        action="store_true",
        help="Attach to tmux session after starting",
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Show log files and exit",
    )
    parser.add_argument(
        "--kill",
        action="store_true",
        help="Kill existing tmux session and exit",
    )

    args = parser.parse_args()

    monitor = TmuxAgentMonitor(session_name=args.session)

    if args.kill:
        print(f"🔴 Killing session '{args.session}'...")
        monitor.kill_session()
        print("✅ Session killed")
        return

    if args.logs:
        monitor.show_logs()
        return

    # Start monitoring
    monitor.start()

    # Run agents
    projects_file = args.projects or "projects.json"
    monitor.run_agents(
        projects_file=projects_file if not args.interactive else None,
        interactive=args.interactive
    )

    if args.attach:
        monitor.attach()
    else:
        print("💡 To attach to the session, run:")
        print(f"   tmux attach-session -t {args.session}")


if __name__ == "__main__":
    main()

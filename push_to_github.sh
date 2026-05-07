#!/bin/bash

# GitHub Publishing Script
# Automatically initializes git, commits, and pushes changes to GitHub

set -e  # Exit on error

REPO_URL="$1"
COMMIT_MESSAGE="${2:-Auto-generated tasks and subtasks from agent team}"

echo "========================================"
echo "GitHub Publishing Script"
echo "========================================"
echo ""

# Check if repo URL is provided
if [ -z "$REPO_URL" ]; then
    echo "[ERROR] Repository URL is required!"
    echo "Usage: ./push_to_github.sh <REPO_URL> [COMMIT_MESSAGE]"
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed!"
    exit 1
fi

echo "[*] Initializing git repository..."
if [ ! -d ".git" ]; then
    git init
    echo "[OK] Git repository initialized"
else
    echo "[OK] Git repository already exists"
fi

echo ""
echo "[*] Configuring git user..."
git config user.email "bot@agentteam.local" 2>/dev/null || true
git config user.name "Agent Team Bot" 2>/dev/null || true
echo "[OK] Git user configured"

echo ""
echo "[*] Staging all files..."
git add .
echo "[OK] All files staged"

echo ""
echo "[*] Creating commit..."
git commit -m "$COMMIT_MESSAGE" 2>/dev/null || {
    echo "[WARN] No changes to commit"
}
echo "[OK] Commit created"

echo ""
echo "[*] Checking remote origin..."
if git remote get-url origin &>/dev/null; then
    echo "[OK] Remote origin already configured"
    git remote set-url origin "$REPO_URL"
else
    echo "[*] Adding remote origin..."
    git remote add origin "$REPO_URL"
    echo "[OK] Remote origin added"
fi

echo ""
echo "[*] Pushing to GitHub..."
git branch -M main 2>/dev/null || true
git push -u origin main
echo "[OK] Successfully pushed to GitHub!"

echo ""
echo "========================================"
echo "[SUCCESS] GitHub publishing complete!"
echo "========================================"
echo ""
echo "Repository: $REPO_URL"
echo "Branch: main"
echo ""

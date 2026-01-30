"""
Auto-commit and push changes to GitHub
Run this after making any changes to automatically sync with repository
"""

import subprocess
import os
from datetime import datetime

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def auto_commit_and_push():
    """Automatically add, commit, and push changes"""
    print("🔄 Auto-committing and pushing changes...")
    
    # Get current directory
    current_dir = os.getcwd()
    
    # Check if we're in a git repository
    success, _, _ = run_command("git status", current_dir)
    if not success:
        print("❌ Not in a Git repository")
        return False
    
    # Check for changes
    success, output, _ = run_command("git status --porcelain", current_dir)
    if not success or not output.strip():
        print("✅ No changes to commit")
        return True
    
    print(f"📝 Changes detected:\n{output}")
    
    # Add all changes
    print("➕ Adding all changes...")
    success, stdout, stderr = run_command("git add .", current_dir)
    if not success:
        print(f"❌ Failed to add changes: {stderr}")
        return False
    print("✅ Changes added")
    
    # Commit changes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Auto-update - {timestamp}"
    print(f"💾 Committing changes: {commit_message}")
    success, stdout, stderr = run_command(f'git commit -m "{commit_message}"', current_dir)
    if not success:
        print(f"❌ Failed to commit: {stderr}")
        return False
    print("✅ Changes committed")
    
    # Push changes
    print("📤 Pushing to GitHub...")
    success, stdout, stderr = run_command("git push", current_dir)
    if not success:
        print(f"❌ Failed to push: {stderr}")
        return False
    print("✅ Changes pushed to GitHub")
    
    print(f"\n🎉 All changes successfully synced at {timestamp}")
    return True

def main():
    """Main function"""
    print("=" * 50)
    print("🚀 AUTO COMMIT & PUSH")
    print("=" * 50)
    
    success = auto_commit_and_push()
    
    if success:
        print("\n✅ Repository is up to date!")
    else:
        print("\n❌ Failed to sync repository")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

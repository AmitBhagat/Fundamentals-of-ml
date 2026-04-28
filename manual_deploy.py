import os
import subprocess
import shutil

# Config
REPO_URL = "https://github.com/AmitBhagat/Fundamentals-of-ml.git"
BUILD_DIR = "out"
BRANCH = "gh-pages"

def run_cmd(cmd, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def deploy():
    # 1. Build
    print("Step 1: Building project...")
    if not run_cmd("npm run build"):
        return

    # 2. Prepare out directory
    print("Step 2: Preparing deployment folder...")
    dot_git = os.path.join(BUILD_DIR, ".git")
    if os.path.exists(dot_git):
        shutil.rmtree(dot_git)
    
    # 3. Git operations in 'out'
    print("Step 3: Initializing temporary git repo in 'out'...")
    if not run_cmd("git init", cwd=BUILD_DIR): return
    if not run_cmd(f"git remote add origin {REPO_URL}", cwd=BUILD_DIR): return
    
    # We use a temporary branch name and force push to the target branch
    if not run_cmd("git add .", cwd=BUILD_DIR): return
    if not run_cmd('git commit -m "Manual Deploy: Logical Overhaul Fix"', cwd=BUILD_DIR): return
    
    print(f"Step 4: Force pushing to {BRANCH}...")
    if not run_cmd(f"git push -f origin master:{BRANCH}", cwd=BUILD_DIR):
        # Try 'main' if 'master' is default
        if not run_cmd(f"git push -f origin main:{BRANCH}", cwd=BUILD_DIR):
            print("Failed to push. Ensure you have git permissions.")
            return

    print("Success! Deployed to GitHub Pages.")

if __name__ == "__main__":
    deploy()

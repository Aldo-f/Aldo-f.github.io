#!/usr/bin/env python3
"""
Documentation Update Watcher for aldo-f.github.io
Automatically detects and integrates documentation changes from source repositories
"""

import os
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
import hashlib
import yaml

# Configuration
REPO_ROOT = Path("/home/aldo/dev")
APPS_DIR = REPO_ROOT  # Apps are directly in dev directory
DOCS_SITE = REPO_ROOT / "06-apps-aldo-f-github-io"
STATE_FILE = DOCS_SITE / ".doc_watcher_state.json"
CHECK_INTERVAL = 300  # 5 minutes

# Documentation patterns to watch
DOC_PATTERNS = [
    "docs/**/*.md",
    "website/docs/**/*.md", 
    "*.md",  # README, etc. at repo root
]

EXCLUDE_PATTERNS = [
    "*/node_modules/**",
    "*/.git/**",
    "*/__pycache__/**",
    "*/dist/**",
    "*/build/**",
    "*legacy*",
    "*archive*",
]

class DocWatcher:
    def __init__(self):
        self.state = self.load_state()
        self.ensure_directories()
    
    def load_state(self):
        """Load the last known state of documentation files"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading state: {e}")
                return {}
        return {}
    
    def save_state(self):
        """Save current state for next comparison"""
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def ensure_directories(self):
        """Ensure necessary directories exist"""
        (DOCS_SITE / "documentation_watcher").mkdir(exist_ok=True)
        (DOCS_SITE / "agent_api").mkdir(exist_ok=True)
    
    def get_repo_docs_path(self, repo_path):
        """Get the documentation path within a repo"""
        repo_path = Path(repo_path)
        
        # Check for standard docs folder
        if (repo_path / "docs").exists():
            return repo_path / "docs"
        
        # Check for website/docs (like thuis v4/v5)
        if (repo_path / "website" / "docs").exists():
            return repo_path / "website" / "docs"
        
        # Check for root level markdown files
        md_files = list(repo_path.glob("*.md"))
        if md_files:
            return repo_path
            
        return None
    
    def should_include_file(self, file_path):
        """Check if a file should be included based on patterns"""
        # Convert to relative path for pattern matching
        try:
            rel_path = str(file_path.relative_to(REPO_ROOT))
        except ValueError:
            # File is outside REPO_ROOT, use absolute
            rel_path = str(file_path)
        
        # Check exclusions first
        for pattern in EXCLUDE_PATTERNS:
            if "*" in pattern:
                # Simple glob matching
                import fnmatch
                if fnmatch.fnmatch(rel_path, pattern):
                    return False
            elif pattern in rel_path:
                return False
        
        # Check inclusions
        for pattern in DOC_PATTERNS:
            if "*" in pattern:
                import fnmatch
                if fnmatch.fnmatch(rel_path, pattern):
                    return True
            elif pattern in rel_path:
                return True
                
        return False
    
    def get_file_hash(self, file_path):
        """Get hash of file contents"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None
    
    def scan_repository(self, repo_path):
        """Scan a repository for documentation changes"""
        repo_path = Path(repo_path)
        repo_name = repo_path.name
        
        print(f"Scanning {repo_name}...")
        
        docs_path = self.get_repo_docs_path(repo_path)
        if not docs_path:
            print(f"  No documentation found in {repo_name}")
            return []
        
        changes = []
        
        # Scan for markdown files
        for md_file in docs_path.rglob("*.md"):
            if not self.should_include_file(md_file):
                continue
                
            file_hash = self.get_file_hash(md_file)
            if file_hash is None:
                continue
            
            # Get relative path within docs for storage
            try:
                rel_path = md_file.relative_to(docs_path)
            except ValueError:
                rel_path = md_file.name
            
            # Create unique identifier
            file_id = f"{repo_name}:{rel_path}"
            
            # Check if changed
            last_hash = self.state.get(file_id, {}).get('hash')
            if last_hash != file_hash:
                changes.append({
                    'repo': repo_name,
                    'file': str(rel_path),
                    'full_path': str(md_file),
                    'old_hash': last_hash,
                    'new_hash': file_hash,
                    'timestamp': datetime.now().isoformat()
                })
                print(f"  Change detected: {rel_path}")
        
        return changes
    
    def scan_all_repositories(self):
        """Scan all application repositories for documentation changes"""
        all_changes = []
        
        # Get all app directories
        if not APPS_DIR.exists():
            print(f"Apps directory not found: {APPS_DIR}")
            return all_changes
            
        for item in APPS_DIR.iterdir():
            if item.is_dir() and item.name.startswith("06-apps-"):
                changes = self.scan_repository(item)
                all_changes.extend(changes)
        
        return all_changes
    
    def integrate_changes(self, changes):
        """Integrate documentation changes into the site"""
        if not changes:
            print("No documentation changes to integrate")
            return False
        
        print(f"Integrating {len(changes)} documentation changes...")
        
        integrated = False
        
        for change in changes:
            repo_name = change['repo']
            rel_file = change['file']
            src_path = Path(change['full_path'])
            
            # Determine destination path
            # For now, we'll integrate into a staged area for review
            # In a full implementation, this would update the multirepo config
            # and trigger appropriate imports
            
            # Example: Thuis documentation goes to docs/thuis/
            if repo_name.startswith("06-apps-thuis"):
                # Extract version from repo name if present
                if "thuis-v4" in repo_name:
                    dest_base = DOCS_SITE / "docs" / "thuis-v4"
                elif "thuis-v5" in repo_name:
                    dest_base = DOCS_SITE / "docs" / "thuis-v5"
                elif "thuis-v3" in repo_name:
                    dest_base = DOCS_SITE / "docs" / "thuis-v3"
                else:
                    dest_base = DOCS_SITE / "docs" / "thuis"
            elif repo_name == "06-apps-clock":
                dest_base = DOCS_SITE / "docs" / "clock"
            elif repo_name == "06-apps-radio-community":
                dest_base = DOCS_SITE / "docs" / "radio-community"
            elif repo_name == "06-apps-wordpress-stantonius":
                dest_base = DOCS_SITE / "docs" / "wordpress-stantonius"
            else:
                # Generic handling
                dest_base = DOCS_SITE / "docs" / repo_name.replace("06-apps-", "")
            
            dest_path = dest_base / rel_file
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                # Copy the file
                import shutil
                shutil.copy2(src_path, dest_path)
                print(f"  Integrated: {repo_name}/{rel_file}")
                
                # Update state
                file_id = f"{repo_name}:{rel_file}"
                self.state[file_id] = {
                    'hash': change['new_hash'],
                    'integrated_at': datetime.now().isoformat(),
                    'size': src_path.stat().st_size
                }
                
                integrated = True
                
            except Exception as e:
                print(f"  Error integrating {repo_name}/{rel_file}: {e}")
        
        if integrated:
            self.save_state()
            print("Documentation changes integrated successfully")
            
            # Trigger site rebuild if significant changes
            # In a full implementation, we'd check if changes warrant rebuild
            # and trigger mkdocs build
            
        return integrated
    
    def run_once(self):
        """Run one scan and integration cycle"""
        print(f"Starting documentation scan at {datetime.now()}")
        changes = self.scan_all_repositories()
        if changes:
            self.integrate_changes(changes)
        else:
            print("No changes detected")
        print(f"Scan completed at {datetime.now()}")
    
    def run_daemon(self):
        """Run as a daemon, scanning periodically"""
        print(f"Starting documentation watcher daemon (checking every {CHECK_INTERVAL}s)")
        try:
            while True:
                self.run_once()
                print(f"Waiting {CHECK_INTERVAL} seconds until next check...")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopping documentation watcher")
        except Exception as e:
            print(f"Watcher error: {e}")

def main():
    import sys
    
    watcher = DocWatcher()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        watcher.run_daemon()
    else:
        watcher.run_once()

if __name__ == "__main__":
    main()
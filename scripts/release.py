#!/usr/bin/env python3
"""
Release helper script for bilibili-downloader
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

def get_current_version():
    """Get current version from __init__.py"""
    init_file = Path("bilibili_downloader/__init__.py")
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in __init__.py")

def update_version(new_version):
    """Update version in all relevant files"""
    files_to_update = [
        ("bilibili_downloader/__init__.py", r'__version__\s*=\s*["\'][^"\']+["\']', f'__version__ = "{new_version}"'),
        ("setup.py", r'version\s*=\s*["\'][^"\']+["\']', f'version="{new_version}"'),
        ("pyproject.toml", r'version\s*=\s*["\'][^"\']+["\']', f'version = "{new_version}"'),
    ]
    
    for filepath, pattern, replacement in files_to_update:
        path = Path(filepath)
        if path.exists():
            content = path.read_text()
            updated_content = re.sub(pattern, replacement, content)
            path.write_text(updated_content)
            print(f"Updated {filepath}")

def create_git_tag(version, message=None):
    """Create and push git tag"""
    tag_name = f"v{version}"
    
    # Check if tag already exists
    result = subprocess.run(["git", "tag", "-l", tag_name], capture_output=True, text=True)
    if result.stdout.strip():
        print(f"Tag {tag_name} already exists!")
        return False
    
    # Create tag
    if message:
        subprocess.run(["git", "tag", "-a", tag_name, "-m", message], check=True)
    else:
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release version {version}"], check=True)
    
    print(f"Created tag {tag_name}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Release helper for bilibili-downloader")
    parser.add_argument("version", help="New version number (e.g., 1.0.1)")
    parser.add_argument("-m", "--message", help="Tag message")
    parser.add_argument("--no-tag", action="store_true", help="Don't create git tag")
    parser.add_argument("--push", action="store_true", help="Push tag to remote")
    
    args = parser.parse_args()
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', args.version):
        print("Error: Version must be in format X.Y.Z")
        sys.exit(1)
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    print(f"New version: {args.version}")
    
    # Update version
    update_version(args.version)
    
    # Git operations
    print("\nGit status:")
    subprocess.run(["git", "status", "--short"])
    
    if not args.no_tag:
        # Add changes
        subprocess.run(["git", "add", "-A"], check=True)
        
        # Commit
        commit_message = f"Bump version to {args.version}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"Committed: {commit_message}")
        
        # Create tag
        if create_git_tag(args.version, args.message):
            if args.push:
                print("\nPushing to remote...")
                subprocess.run(["git", "push"], check=True)
                subprocess.run(["git", "push", "--tags"], check=True)
                print("Pushed commits and tags to remote")
            else:
                print("\nTo push changes and trigger release:")
                print("  git push")
                print("  git push --tags")

if __name__ == "__main__":
    main()
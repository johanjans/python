#!/usr/bin/env python3
"""
incrementalBuild.py - Incremental Quarto Book Builder

Intelligently builds only changed files in a Quarto book project.
- If _quarto.yml or auxiliary files changed → full rebuild
- If only source files changed → render only those files
- Always runs post-processing on all files (required for sidebar consistency)

Alias: publish
"""

import yaml
import subprocess
import sys
import argparse
import os
from pathlib import Path
from typing import List, Optional, TextIO
from datetime import datetime

__version__ = "1.0.0"

# Constants
PROJECT_ROOT = Path(__file__).parent.resolve()
QUARTO_YML = PROJECT_ROOT / "_quarto.yml"
BOOK_DIR = PROJECT_ROOT / "_book"
DEPLOY_DIR = Path("/var/www/python/")
LOG_FILE = PROJECT_ROOT / "build.log"
DEFAULT_SSH_KEY = Path.home() / ".ssh" / "ed25519_mechanics"

# Global log file handle
_log_file: Optional[TextIO] = None

# Auxiliary files that trigger full rebuild when changed
AUXILIARY_FILES = [
    "custom.scss",
    "dark.scss",
    "light.scss",
    "footer.html",
    "hint.lua",
    "color-emphasis.lua",
    "lastModified.lua",
    "references.bib",
]


def log(message: str):
    """Print timestamped log message to console and log file."""
    global _log_file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    if _log_file:
        _log_file.write(line + "\n")
        _log_file.flush()


def parse_quarto_yml() -> dict:
    """Load and parse _quarto.yml."""
    with open(QUARTO_YML, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_book_files(config: dict) -> List[Path]:
    """Extract all source files from chapters structure in _quarto.yml."""
    chapters = config.get('book', {}).get('chapters', [])
    files = []

    def extract(items):
        for item in items:
            if isinstance(item, str):
                files.append(PROJECT_ROOT / item)
            elif isinstance(item, dict):
                if 'chapters' in item:
                    extract(item['chapters'])

    extract(chapters)
    return files


def source_to_output(source: Path) -> Path:
    """Map source file (.qmd/.ipynb) to HTML output path in _book/."""
    relative = source.relative_to(PROJECT_ROOT)
    return BOOK_DIR / relative.with_suffix('.html')


def get_mtime(path: Path) -> float:
    """Get modification time, return 0 if file doesn't exist."""
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return 0


def needs_full_rebuild(book_files: List[Path]) -> tuple[bool, str]:
    """
    Check if full rebuild is needed.
    Returns (needs_rebuild, reason).
    """
    # No output directory = needs full rebuild
    if not BOOK_DIR.exists():
        return True, "No _book/ directory found"

    # Get oldest output file mtime
    output_mtimes = []
    for source in book_files:
        output = source_to_output(source)
        if output.exists():
            output_mtimes.append(get_mtime(output))

    if not output_mtimes:
        return True, "No output files found in _book/"

    oldest_output_mtime = min(output_mtimes)

    # Check if _quarto.yml is newer than oldest output
    if get_mtime(QUARTO_YML) > oldest_output_mtime:
        return True, "_quarto.yml has been modified"

    # Check auxiliary files
    for aux_name in AUXILIARY_FILES:
        aux_path = PROJECT_ROOT / aux_name
        if aux_path.exists() and get_mtime(aux_path) > oldest_output_mtime:
            return True, f"{aux_name} has been modified"

    return False, ""


def find_changed_files(book_files: List[Path]) -> List[Path]:
    """Find source files newer than their HTML output."""
    changed = []
    for source in book_files:
        if not source.exists():
            log(f"Warning: Source file not found: {source.relative_to(PROJECT_ROOT)}")
            continue
        output = source_to_output(source)
        if get_mtime(source) > get_mtime(output):
            changed.append(source)
    return changed


def render_full() -> bool:
    """Execute full quarto render."""
    log("Running full Quarto render...")
    result = subprocess.run(
        ['quarto', 'render', '--to', 'html'],
        cwd=PROJECT_ROOT
    )
    return result.returncode == 0


def render_files(files: List[Path]) -> bool:
    """Render specific files incrementally."""
    success = True
    for source in files:
        relative = source.relative_to(PROJECT_ROOT)
        log(f"Rendering: {relative}")
        result = subprocess.run(
            ['quarto', 'render', str(relative), '--to', 'html'],
            cwd=PROJECT_ROOT
        )
        if result.returncode != 0:
            log(f"ERROR: Failed to render {relative}")
            success = False
    return success


def run_post_processing() -> bool:
    """Run postProcessing.py to fix chapter numbering."""
    log("Running post-processing (fixing chapter numbers)...")
    result = subprocess.run(
        [sys.executable, 'postProcessing.py'],
        cwd=PROJECT_ROOT
    )
    return result.returncode == 0


def set_permissions() -> bool:
    """Set group ownership to www-data."""
    log("Setting permissions (chgrp www-data)...")
    result = subprocess.run(
        ['sudo', 'chgrp', '-R', 'www-data', str(BOOK_DIR)]
    )
    return result.returncode == 0


def deploy() -> bool:
    """Rsync to deployment directory."""
    log(f"Deploying to {DEPLOY_DIR}...")
    result = subprocess.run(
        ['sudo', 'rsync', '-vart', '--delete',
         str(BOOK_DIR) + '/', str(DEPLOY_DIR)]
    )
    return result.returncode == 0


def git_push(ssh_key: Path) -> bool:
    """Push to git remote using specified SSH key."""
    if not ssh_key.exists():
        log(f"ERROR: SSH key not found: {ssh_key}")
        return False

    log("Pushing to git remote...")

    # Set up SSH command with the specific key
    git_ssh_command = f"ssh -i {ssh_key} -o IdentitiesOnly=yes"
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = git_ssh_command

    # Run git push
    result = subprocess.run(
        ["git", "push"],
        cwd=PROJECT_ROOT,
        env=env
    )
    return result.returncode == 0


def main():
    global _log_file

    parser = argparse.ArgumentParser(
        prog='publish',
        description='Incremental Quarto book builder - builds only changed files and deploys to server.',
        epilog='Examples:\n'
               '  publish              Build changed files and deploy\n'
               '  publish --full       Force full rebuild\n'
               '  publish --dry-run    Show what would be built\n'
               '  publish --git        Build, deploy, and push to git',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version', action='version',
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '--full', action='store_true',
        help='Force full rebuild regardless of changes'
    )
    parser.add_argument(
        '--no-deploy', action='store_true',
        help='Skip deployment step (build only)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be built without actually building'
    )
    parser.add_argument(
        '--git', action='store_true',
        help='Push to git remote after successful build'
    )
    parser.add_argument(
        '--ssh-key', type=Path,
        default=DEFAULT_SSH_KEY,
        help=f'SSH key for git push (default: {DEFAULT_SSH_KEY})'
    )
    args = parser.parse_args()

    # Open log file
    _log_file = open(LOG_FILE, 'a', encoding='utf-8')

    try:
        log("=" * 60)
        log("Incremental Quarto Build")
        log("=" * 60)

        # Parse configuration
        config = parse_quarto_yml()
        book_files = get_book_files(config)
        log(f"Found {len(book_files)} book files in _quarto.yml")

        # Determine build strategy
        if args.full:
            do_full_rebuild = True
            reason = "Forced via --full flag"
        else:
            do_full_rebuild, reason = needs_full_rebuild(book_files)

        if do_full_rebuild:
            log(f"Full rebuild needed: {reason}")
            if args.dry_run:
                log("DRY RUN: Would run full quarto render")
            else:
                # Prompt for sudo password upfront
                if not args.no_deploy:
                    subprocess.run(['sudo', '-v'])
                if not render_full():
                    log("ERROR: Full render failed!")
                    sys.exit(1)
        else:
            changed = find_changed_files(book_files)
            if not changed:
                log("No changes detected - nothing to build")
                if args.git:
                    if not git_push(args.ssh_key):
                        log("ERROR: Git push failed!")
                        sys.exit(1)
                return
            else:
                log(f"Found {len(changed)} changed file(s):")
                for f in changed:
                    log(f"  - {f.relative_to(PROJECT_ROOT)}")

                if args.dry_run:
                    log("DRY RUN: Would render only the above files")
                else:
                    # Prompt for sudo password upfront
                    if not args.no_deploy:
                        subprocess.run(['sudo', '-v'])
                    if not render_files(changed):
                        log("ERROR: Incremental render failed!")
                        sys.exit(1)

        if args.dry_run:
            log("DRY RUN: Would run post-processing, set permissions, and deploy")
            return

        # Post-processing (always on all files for sidebar consistency)
        if not run_post_processing():
            log("ERROR: Post-processing failed!")
            sys.exit(1)

        if args.no_deploy:
            log("Build complete (deployment skipped via --no-deploy)")
            return

        # Set permissions and deploy
        if not set_permissions():
            log("ERROR: Failed to set permissions!")
            sys.exit(1)

        if not deploy():
            log("ERROR: Deployment failed!")
            sys.exit(1)

        # Git push if requested
        if args.git:
            if not git_push(args.ssh_key):
                log("ERROR: Git push failed!")
                sys.exit(1)

        log("=" * 60)
        log("Build and deployment complete!")
        log("=" * 60)

    finally:
        _log_file.close()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
publish.py - Incremental Quarto Book Builder for Scientific Programming

This is a thin wrapper around quarto_shared that provides project-specific
configuration. The shared build logic lives in ~/quarto-shared/quarto_shared/.

Usage:
    ./publish.py              Build changed files and deploy
    ./publish.py --full       Force full rebuild
    ./publish.py --deploy-only  Deploy existing _book/ (useful after quarto preview)
    ./publish.py --no-render  Post-process and deploy only (skip quarto)
    ./publish.py --dry-run    Show what would be built
    ./publish.py --git        Build, deploy, and push to git
    ./publish.py --sync       Sync theme files from quarto-shared
"""

import sys
import argparse
from pathlib import Path

# Add quarto-shared to path
QUARTO_SHARED = Path.home() / "quarto-shared"
if not QUARTO_SHARED.exists():
    print(f"ERROR: quarto-shared not found at {QUARTO_SHARED}")
    print("Please clone the quarto-shared repository:")
    print(f"  git clone <repo-url> {QUARTO_SHARED}")
    sys.exit(1)

sys.path.insert(0, str(QUARTO_SHARED))

from quarto_shared import sync, build

__version__ = "2.0.0"

# Project-specific configuration
PROJECT_ROOT = Path(__file__).parent.resolve()
DEPLOY_DIR = Path("/var/www/python/")
SSH_KEY = Path.home() / ".ssh" / "ed25519_mechanics"


def main():
    parser = argparse.ArgumentParser(
        prog='publish',
        description='Incremental Quarto book builder - builds only changed files and deploys to server.',
        epilog='Examples:\n'
               '  publish              Build changed files and deploy\n'
               '  publish --full       Force full rebuild\n'
               '  publish --deploy-only  Deploy existing _book/ (after quarto preview)\n'
               '  publish --no-render  Post-process and deploy only (skip quarto)\n'
               '  publish --dry-run    Show what would be built\n'
               '  publish --git        Build, deploy, and push to git\n'
               '  publish --sync       Sync theme files only (no build)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version', action='version',
        version=f'%(prog)s {__version__} (quarto_shared {build.__version__})'
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
        '--no-render', action='store_true',
        help='Skip quarto render, only run post-processing and deploy'
    )
    parser.add_argument(
        '--deploy-only', action='store_true',
        help='Deploy existing _book/ without rendering (useful after quarto preview)'
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
        default=SSH_KEY,
        help=f'SSH key for git push (default: {SSH_KEY})'
    )
    parser.add_argument(
        '--sync', action='store_true',
        help='Sync theme files from quarto-shared (no build)'
    )
    parser.add_argument(
        '--no-sync-check', action='store_true',
        help='Skip the sync check before building'
    )
    args = parser.parse_args()

    # Sync-only mode
    if args.sync:
        if sync.has_changes(PROJECT_ROOT):
            sync.print_diff_summary(PROJECT_ROOT)
            sync.apply(PROJECT_ROOT)
            print("\nTheme files synced.")
        else:
            print("All theme files are already in sync.")
        return

    # Check for theme updates before building (unless --no-sync-check)
    if not args.no_sync_check and sync.has_changes(PROJECT_ROOT):
        if not sync.interactive_sync(PROJECT_ROOT):
            # User declined sync, continue with build anyway
            pass

    # Configure build
    config = build.BuildConfig(
        project_root=PROJECT_ROOT,
        deploy_dir=DEPLOY_DIR,
        ssh_key=args.ssh_key,
    )

    options = build.BuildOptions(
        full=args.full,
        no_deploy=args.no_deploy,
        no_render=args.no_render,
        dry_run=args.dry_run,
        git=args.git,
        deploy_only=args.deploy_only,
    )

    # Run build
    success = build.run(config, options)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Claude Code Shell Snapshot Cleanup Script
Manages shell snapshot files to prevent accumulation and disk space issues.
Implements configurable retention policies with safety guards.
Usage:
    python cleanup-shell-snapshots.py [--dry-run] [--max-files N]
        [--max-age-days N] [--verbose]

Default Policy:
    - Keep most recent 30 snapshots
    - Delete snapshots older than 7 days
        - Always keep at least 5 most recent snapshots
            as safety guard
"""

import argparse
import datetime
import logging
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from claude_utils import get_claude_dir

# Configuration constants
DEFAULT_MAX_FILES = 30
DEFAULT_MAX_AGE_DAYS = 7
MIN_FILES_TO_KEEP = 5  # Safety guard - always keep at least this many


class SnapshotCleanupError(Exception):
    """Raised when shell snapshot cleanup encounters a critical error."""
    pass


class ShellSnapshotCleaner:
    """Shell snapshot cleanup manager."""

    def __init__(
        self,
        snapshots_dir: Optional[Path] = None,
        max_files: int = DEFAULT_MAX_FILES,
        max_age_days: int = DEFAULT_MAX_AGE_DAYS
    ) -> None:
        """Initialize shell snapshot cleaner.

        Args:
            snapshots_dir: Path to shell-snapshots directory.
                          Defaults to CLAUDE_DIR/shell-snapshots
            max_files: Maximum number of snapshots to keep
            max_age_days: Maximum age in days before deletion
        """
        claude_dir = get_claude_dir()
        self.snapshots_dir = snapshots_dir or (claude_dir / "shell-snapshots")
        self.max_files = max_files
        self.max_age_days = max_age_days
        self.logger = logging.getLogger(__name__)

    def get_snapshot_files(self) -> List[Tuple[Path, datetime.datetime]]:
        """Get list of snapshot files with their modification times.

        Returns:
            List of (path, modification_time) tuples
            sorted by modification time (newest first)

        Raises:
            SnapshotCleanupError: If snapshots directory cannot be accessed
        """
        if not self.snapshots_dir.exists():
            self.logger.info(
                f"Snapshots directory does not exist: {self.snapshots_dir}"
            )
            return []

        try:
            snapshot_files: list[tuple[Path, datetime.datetime]] = []
            for file_path in self.snapshots_dir.glob("snapshot-bash-*.sh"):
                if file_path.is_file():
                    mod_time = datetime.datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    )
                    snapshot_files.append((file_path, mod_time))

            # Sort by modification time (newest first)
            snapshot_files.sort(key=lambda x: x[1], reverse=True)
            return snapshot_files

        except OSError as e:
            raise SnapshotCleanupError(
                f"Cannot access snapshots directory: {e}"
            ) from e

    def identify_files_for_cleanup(
        self,
        snapshot_files: List[Tuple[Path, datetime.datetime]]
    ) -> List[Path]:
        """Identify snapshot files that should be cleaned up.
        
        Args:
            snapshot_files: List of (path, modification_time) tuples
            
        Returns:
            List of file paths to delete
        """
        if not snapshot_files:
            return []
            
        files_to_delete: list[Path] = []
        cutoff_date = (
            datetime.datetime.now()
            - datetime.timedelta(days=self.max_age_days)
        )

        # Apply file count limit (but respect MIN_FILES_TO_KEEP)
        if len(snapshot_files) > self.max_files:
            files_over_limit = snapshot_files[
                max(self.max_files, MIN_FILES_TO_KEEP):
            ]
            files_to_delete.extend([path for path, _ in files_over_limit])
            self.logger.debug(
                f"Found {len(files_over_limit)} files over count limit"
            )

        # Apply age limit (but respect MIN_FILES_TO_KEEP)
        files_by_age = [
            path for path, mod_time in snapshot_files
            if mod_time < cutoff_date
        ]

        # Only delete aged files if we would still keep MIN_FILES_TO_KEEP
        if len(snapshot_files) - len(files_by_age) >= MIN_FILES_TO_KEEP:
            files_to_delete.extend(files_by_age)
            self.logger.debug(
                f"Found {len(files_by_age)} files over age limit"
            )
        else:
            self.logger.info(
                f"Skipping age-based cleanup to maintain minimum "
                f"{MIN_FILES_TO_KEEP} files"
            )

        # Remove duplicates while preserving order
        files_to_delete = list(dict.fromkeys(files_to_delete))

        return files_to_delete
    
    def cleanup_snapshots(self, dry_run: bool = False) -> Tuple[int, int]:
        """Perform snapshot cleanup based on configured policies.
        
        Args:
            dry_run: If True, only identify files but don't delete them
            
        Returns:
            Tuple of (files_deleted, total_size_freed_mb)
            
        Raises:
            SnapshotCleanupError: If cleanup encounters critical error
        """
        self.logger.info(
            f"Starting shell snapshot cleanup (dry_run={dry_run})"
        )
        print("🧹 Shell Snapshot Cleanup")
        print("=" * 40)
        
        # Get all snapshot files
        snapshot_files = self.get_snapshot_files()
        total_files = len(snapshot_files)
        
        if not snapshot_files:
            print("📂 No snapshot files found")
            return 0, 0
        
        print(f"📊 Found {total_files} snapshot files")
        print(
            f"📋 Policy: Keep max {self.max_files} files, "
            f"max {self.max_age_days} days old"
        )
        print(
            f"🛡️  Safety: Always keep at least {MIN_FILES_TO_KEEP} "
            f"most recent files"
        )
        
        # Identify files for cleanup
        files_to_delete = self.identify_files_for_cleanup(snapshot_files)
        
        if not files_to_delete:
            print("✅ No cleanup needed - all files within policy limits")
            return 0, 0
        
        # Calculate total size of files to delete
        total_size_bytes = 0
        for file_path in files_to_delete:
            try:
                total_size_bytes += file_path.stat().st_size
            except OSError:
                self.logger.warning(f"Cannot get size of {file_path}")
        
        total_size_mb = total_size_bytes / (1024 * 1024)
        
        print(f"🗑️  {len(files_to_delete)} files marked for cleanup")
        print(f"💾 Total size to free: {total_size_mb:.2f} MB")
        
        if dry_run:
            print("🔍 DRY RUN - Files that would be deleted:")
            for file_path in files_to_delete[:10]:  # Show first 10
                print(f"   • {file_path.name}")
            if len(files_to_delete) > 10:
                print(f"   ... and {len(files_to_delete) - 10} more")
            return len(files_to_delete), int(total_size_mb)
        
        # Perform actual deletion
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                deleted_count += 1
                self.logger.debug(f"Deleted: {file_path.name}")
            except OSError as e:
                self.logger.error(f"Failed to delete {file_path}: {e}")

        print("✅ Cleanup completed:")
        print(f"   • {deleted_count} files deleted")
        print(f"   • {total_size_mb:.2f} MB freed")
        print(f"   • {total_files - deleted_count} files remaining")

        return deleted_count, int(total_size_mb)


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration.

    Args:
        verbose: Enable debug logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Shell Snapshot Cleanup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting files"
    )
    
    parser.add_argument(
        "--max-files",
        type=int,
        default=DEFAULT_MAX_FILES,
        help=(
            "Maximum number of snapshots to keep "
            f"(default: {DEFAULT_MAX_FILES})"
        )
    )
    
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=DEFAULT_MAX_AGE_DAYS,
        help=(
            "Maximum age in days before deletion "
            f"(default: {DEFAULT_MAX_AGE_DAYS})"
        )
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point.
    
    Returns:
        Exit code: 0 for success, 1 for cleanup failure, 2 for critical error
    """
    args = parse_arguments()
    setup_logging(args.verbose)
    
    try:
        cleaner = ShellSnapshotCleaner(
            max_files=args.max_files,
            max_age_days=args.max_age_days
        )
        cleaner.cleanup_snapshots(args.dry_run)
        # Return success
        return 0
    except SnapshotCleanupError as e:
        logging.getLogger(__name__).critical(f"Critical cleanup error: {e}")
        print(f"❌ Critical error: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\n⚠️  Cleanup interrupted by user", file=sys.stderr)
        return 2
    except Exception as e:
        logging.getLogger(__name__).critical(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

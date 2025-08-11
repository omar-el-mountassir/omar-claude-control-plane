#!/usr/bin/env python3
"""
Claude Code Configuration Backup Script

A comprehensive backup tool for Claude Code global configuration.
Creates timestamped backups with size reporting and comprehensive error handling.

Usage:
    python backup-config.py [--source-dir PATH] [--backup-dir PATH] [--verbose] [--quiet] [--dry-run]

Returns:
    0 if backup succeeds, 1 if backup fails, 2 if critical error
"""

import argparse
import datetime
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Optional, List, Tuple

# Add path for shared utilities
sys.path.append(str(Path(__file__).parent.parent / "utils"))
from claude_utils import get_claude_dir, IGNORE_PATTERNS, BYTES_PER_MB

# Configuration constants
DEFAULT_SOURCE_DIR = get_claude_dir()
DEFAULT_BACKUP_BASE = Path.home() / ".claude-backups"


class BackupError(Exception):
    """Raised when backup encounters a critical error."""
    pass


class ConfigurationBackup:
    """Claude Code configuration backup manager."""
    
    def __init__(
        self, 
        source_dir: Optional[Path] = None, 
        backup_base: Optional[Path] = None
    ) -> None:
        """Initialize backup manager.
        
        Args:
            source_dir: Path to source configuration directory.
                       Defaults to ~/.claude
            backup_base: Path to backup base directory.
                        Defaults to ~/.claude-backups
        """
        self.source_dir = source_dir or DEFAULT_SOURCE_DIR
        self.backup_base = backup_base or DEFAULT_BACKUP_BASE
        self.logger = logging.getLogger(__name__)
        
    def validate_source_directory(self) -> bool:
        """Validate that source directory exists and is readable.
        
        Returns:
            True if source directory is valid, False otherwise
        """
        if not self.source_dir.exists():
            self.logger.error(f"Source directory does not exist: {self.source_dir}")
            return False
            
        if not self.source_dir.is_dir():
            self.logger.error(f"Source path is not a directory: {self.source_dir}")
            return False
            
        if not os.access(self.source_dir, os.R_OK):
            self.logger.error(f"Source directory is not readable: {self.source_dir}")
            return False
            
        return True
    
    def prepare_backup_directory(self, timestamp: str) -> Path:
        """Prepare backup directory with timestamp.
        
        Args:
            timestamp: Timestamp string for backup directory name
            
        Returns:
            Path to created backup directory
            
        Raises:
            BackupError: If backup directory cannot be created
        """
        backup_dir = self.backup_base / f"backup_{timestamp}"
        
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created backup directory: {backup_dir}")
            return backup_dir
        except OSError as e:
            raise BackupError(f"Cannot create backup directory {backup_dir}: {e}") from e
    
    def calculate_directory_size(self, path: Path) -> float:
        """Calculate directory size in megabytes.
        
        Args:
            path: Directory path to calculate size for
            
        Returns:
            Size in megabytes
            
        Raises:
            BackupError: If size calculation fails
        """
        try:
            total_bytes = 0
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        total_bytes += file_path.stat().st_size
                    except OSError as e:
                        self.logger.warning(f"Cannot stat file {file_path}: {e}")
                        # Continue calculating, don't fail entire operation
                        
            return total_bytes / BYTES_PER_MB
            
        except Exception as e:
            raise BackupError(f"Cannot calculate directory size for {path}: {e}") from e
    
    def copy_configuration(self, backup_dir: Path, dry_run: bool = False) -> Path:
        """Copy configuration to backup directory.
        
        Args:
            backup_dir: Target backup directory
            dry_run: If True, only simulate the copy operation
            
        Returns:
            Path to copied configuration directory
            
        Raises:
            BackupError: If copy operation fails
        """
        target_dir = backup_dir / ".claude"
        
        if dry_run:
            self.logger.info(f"DRY RUN: Would copy {self.source_dir} to {target_dir}")
            print(f"🔍 DRY RUN: Would copy {self.source_dir} to {target_dir}")
            return target_dir
        
        try:
            self.logger.info(f"Copying {self.source_dir} to {target_dir}")
            shutil.copytree(
                self.source_dir, 
                target_dir,
                ignore=shutil.ignore_patterns(*IGNORE_PATTERNS)
            )
            self.logger.debug(f"Successfully copied configuration to {target_dir}")
            return target_dir
            
        except shutil.Error as e:
            # shutil.Error contains multiple error details
            error_details = []
            for src, dst, error in e.args[0]:
                error_details.append(f"{src} -> {dst}: {error}")
            error_msg = f"Multiple copy errors: {'; '.join(error_details)}"
            raise BackupError(error_msg) from e
            
        except OSError as e:
            raise BackupError(f"Cannot copy configuration to {target_dir}: {e}") from e
    
    def create_backup(self, dry_run: bool = False) -> Optional[Path]:
        """Create complete configuration backup.
        
        Args:
            dry_run: If True, only simulate the backup operation
            
        Returns:
            Path to backup directory if successful, None if failed
            
        Raises:
            BackupError: If critical error prevents backup
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        self.logger.info(f"Starting backup of {self.source_dir}")
        print("🔄 Starting Claude Code configuration backup")
        
        # Validation phase
        if not self.validate_source_directory():
            self.logger.error("Source directory validation failed")
            print("❌ Source directory validation failed")
            return None
        
        try:
            # Prepare backup directory
            backup_dir = self.prepare_backup_directory(timestamp)
            print(f"📁 Backup directory: {backup_dir}")
            
            # Copy configuration
            target_dir = self.copy_configuration(backup_dir, dry_run)
            
            if not dry_run:
                # Calculate and report size
                backup_size = self.calculate_directory_size(backup_dir)
                print(f"✅ Backup completed: {backup_dir}")
                print(f"📊 Backup size: {backup_size:.1f}MB")
                self.logger.info(f"Backup completed successfully: {backup_dir} ({backup_size:.1f}MB)")
            else:
                print("✅ DRY RUN completed successfully")
                self.logger.info("Dry run completed successfully")
            
            return backup_dir
            
        except BackupError:
            # Re-raise backup errors
            raise
        except Exception as e:
            # Convert unexpected errors to BackupError
            raise BackupError(f"Unexpected error during backup: {e}") from e
    
    def list_existing_backups(self) -> List[Tuple[Path, datetime.datetime, float]]:
        """List existing backups with metadata.
        
        Returns:
            List of tuples containing (path, timestamp, size_mb)
        """
        backups = []
        
        if not self.backup_base.exists():
            return backups
        
        try:
            for backup_dir in self.backup_base.iterdir():
                if backup_dir.is_dir() and backup_dir.name.startswith("backup_"):
                    # Extract timestamp from directory name
                    timestamp_str = backup_dir.name.replace("backup_", "")
                    try:
                        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
                        size_mb = self.calculate_directory_size(backup_dir)
                        backups.append((backup_dir, timestamp, size_mb))
                    except (ValueError, BackupError) as e:
                        self.logger.warning(f"Cannot process backup directory {backup_dir}: {e}")
                        
        except OSError as e:
            self.logger.warning(f"Cannot list backup directories: {e}")
            
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x[1], reverse=True)
        return backups


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Setup logging configuration.
    
    Args:
        verbose: Enable debug logging
        quiet: Suppress all but critical logging
    """
    if quiet:
        level = logging.CRITICAL
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
        
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
        description="Claude Code Configuration Backup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--source-dir",
        type=Path,
        help="Path to source configuration directory (default: ~/.claude)"
    )
    
    parser.add_argument(
        "--backup-dir", 
        type=Path,
        help="Path to backup base directory (default: ~/.claude-backups)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress all output except results and critical errors"
    )
    
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Perform a trial run with no changes made"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List existing backups and exit"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point.
    
    Returns:
        Exit code: 0 for success, 1 for backup failure, 2 for critical error
    """
    args = parse_arguments()
    setup_logging(args.verbose, args.quiet)
    
    try:
        backup_manager = ConfigurationBackup(args.source_dir, args.backup_dir)
        
        # List existing backups if requested
        if args.list:
            backups = backup_manager.list_existing_backups()
            if backups:
                print("📋 Existing Backups:")
                for backup_path, timestamp, size_mb in backups:
                    print(f"  📁 {backup_path.name} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({size_mb:.1f}MB)")
            else:
                print("📋 No existing backups found")
            return 0
        
        # Create backup
        backup_dir = backup_manager.create_backup(args.dry_run)
        return 0 if backup_dir else 1
        
    except BackupError as e:
        logging.getLogger(__name__).critical(f"Critical backup error: {e}")
        if not args.quiet:
            print(f"❌ Critical error: {e}", file=sys.stderr)
        return 2
        
    except KeyboardInterrupt:
        if not args.quiet:
            print("\n⚠️  Backup interrupted by user", file=sys.stderr)
        return 2
        
    except Exception as e:
        logging.getLogger(__name__).critical(f"Unexpected error: {e}")
        if not args.quiet:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
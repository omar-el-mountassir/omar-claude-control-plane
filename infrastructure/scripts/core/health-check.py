#!/usr/bin/env python3
"""
Claude Code Configuration Health Check

A comprehensive health validation tool for Claude Code architecture integrity.
Validates directory structure, @ reference resolution, version consistency,
and core script availability.

Usage:
    python health-check.py [--verbose] [--config-dir PATH] [--quiet]

Returns:
    0 if all checks pass, 1 if issues found, 2 if critical error
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Add path for shared utilities
sys.path.append(str(Path(__file__).parent.parent / "utils"))
from claude_utils import get_claude_dir, REQUIRED_DIRECTORIES, CORE_SCRIPTS, EXPECTED_VERSION


class HealthCheckError(Exception):
    """Raised when health check encounters a critical error."""
    pass


class HealthChecker:
    """Claude Code configuration health checker."""
    
    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize health checker.
        
        Args:
            config_dir: Path to Claude configuration directory.
                       Defaults to CLAUDE_DIR environment variable or ~/.claude
        """
        self.config_dir = config_dir or get_claude_dir()
        self.issues: List[str] = []
        self.logger = logging.getLogger(__name__)
        
    def check_directory_structure(self) -> bool:
        """Validate required directory structure exists.
        
        Returns:
            True if all directories exist, False otherwise
        """
        self.logger.info("Checking directory structure")
        print("\n📁 Directory Structure Check:")
        
        all_exist = True
        for dir_path in REQUIRED_DIRECTORIES:
            full_path = self.config_dir / dir_path
            if full_path.exists() and full_path.is_dir():
                print(f"  ✅ {dir_path}")
                self.logger.debug(f"Directory exists: {dir_path}")
            else:
                print(f"  ❌ {dir_path} - MISSING")
                issue = f"Missing directory: {dir_path}"
                self.issues.append(issue)
                self.logger.warning(issue)
                all_exist = False
                
        return all_exist
    
    def check_claude_md_references(self) -> bool:
        """Validate @ references in CLAUDE.md resolve correctly.
        
        Returns:
            True if all references resolve, False otherwise
            
        Raises:
            HealthCheckError: If CLAUDE.md cannot be read
        """
        self.logger.info("Checking @ references in CLAUDE.md")
        print("\n🔗 @ Reference Check:")
        
        claude_md = self.config_dir / "CLAUDE.md"
        if not claude_md.exists():
            issue = "CLAUDE.md missing"
            print(f"  ❌ {issue}")
            self.issues.append(issue)
            self.logger.error(issue)
            return False
            
        try:
            content = claude_md.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError) as e:
            raise HealthCheckError(f"Cannot read CLAUDE.md: {e}") from e
        
        # Extract @ references using regex
        references = re.findall(r'@([^\s]+)', content)
        if not references:
            self.logger.warning("No @ references found in CLAUDE.md")
            print("  ⚠️  No @ references found")
            return True
            
        all_valid = True
        for ref in references:
            ref_path = self.config_dir / ref
            if ref_path.exists():
                print(f"  ✅ @{ref}")
                self.logger.debug(f"Reference valid: @{ref}")
            else:
                print(f"  ❌ @{ref} - BROKEN")
                issue = f"Broken @ reference: @{ref}"
                self.issues.append(issue)
                self.logger.warning(issue)
                all_valid = False
                
        return all_valid
    
    def check_version_consistency(self) -> bool:
        """Validate version consistency in CLAUDE.md.
        
        Returns:
            True if version is consistent, False otherwise
            
        Raises:
            HealthCheckError: If CLAUDE.md cannot be read
        """
        self.logger.info(f"Checking version consistency (expected: {EXPECTED_VERSION})")
        print("\n📋 Version Check:")
        
        claude_md = self.config_dir / "CLAUDE.md"
        if not claude_md.exists():
            # Already reported in reference check
            return False
            
        try:
            content = claude_md.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError) as e:
            raise HealthCheckError(f"Cannot read CLAUDE.md for version check: {e}") from e
            
        version_pattern = f"version: {EXPECTED_VERSION}"
        if version_pattern in content:
            print(f"  ✅ Version {EXPECTED_VERSION} confirmed")
            self.logger.debug(f"Version {EXPECTED_VERSION} found")
            return True
        else:
            print(f"  ❌ Version not {EXPECTED_VERSION}")
            issue = f"Version inconsistency in CLAUDE.md (expected: {EXPECTED_VERSION})"
            self.issues.append(issue)
            self.logger.warning(issue)
            return False
    
    def check_core_scripts(self) -> bool:
        """Validate core scripts exist.
        
        Returns:
            True if all core scripts exist, False otherwise
        """
        self.logger.info("Checking core scripts")
        print("\n🔧 Core Scripts Check:")
        
        all_exist = True
        for script in CORE_SCRIPTS:
            script_path = self.config_dir / script
            if script_path.exists() and script_path.is_file():
                print(f"  ✅ {script}")
                self.logger.debug(f"Core script exists: {script}")
            else:
                print(f"  ❌ {script} - MISSING")
                issue = f"Missing core script: {script}"
                self.issues.append(issue)
                self.logger.warning(issue)
                all_exist = False
                
        return all_exist
    
    def run_health_check(self) -> bool:
        """Run complete health check.
        
        Returns:
            True if all checks pass, False if issues found
            
        Raises:
            HealthCheckError: If critical error prevents health check
        """
        self.logger.info(f"Starting health check for {self.config_dir}")
        print("🔍 Claude Code Configuration Health Check")
        print("=" * 50)
        
        # Clear any previous issues
        self.issues.clear()
        
        # Run all checks
        try:
            checks = [
                self.check_directory_structure(),
                self.check_claude_md_references(), 
                self.check_version_consistency(),
                self.check_core_scripts()
            ]
        except HealthCheckError:
            # Re-raise critical errors
            raise
        except Exception as e:
            # Convert unexpected errors to HealthCheckError
            raise HealthCheckError(f"Unexpected error during health check: {e}") from e
        
        # Report results
        print("\n📊 Health Check Results:")
        if not self.issues:
            print("🎉 All checks passed! Architecture is healthy.")
            self.logger.info("Health check passed")
            return True
        else:
            print(f"⚠️  {len(self.issues)} issues found:")
            for issue in self.issues:
                print(f"   • {issue}")
            self.logger.warning(f"Health check failed with {len(self.issues)} issues")
            return False


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
        description="Claude Code Configuration Health Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--config-dir",
        type=Path,
        help="Path to Claude configuration directory (default: ~/.claude)"
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
    
    return parser.parse_args()


def main() -> int:
    """Main entry point.
    
    Returns:
        Exit code: 0 for success, 1 for health check failure, 2 for critical error
    """
    args = parse_arguments()
    setup_logging(args.verbose, args.quiet)
    
    try:
        checker = HealthChecker(args.config_dir)
        success = checker.run_health_check()
        return 0 if success else 1
        
    except HealthCheckError as e:
        logging.getLogger(__name__).critical(f"Critical health check error: {e}")
        if not args.quiet:
            print(f"❌ Critical error: {e}", file=sys.stderr)
        return 2
        
    except KeyboardInterrupt:
        if not args.quiet:
            print("\n⚠️  Health check interrupted by user", file=sys.stderr)
        return 2
        
    except Exception as e:
        logging.getLogger(__name__).critical(f"Unexpected error: {e}")
        if not args.quiet:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())